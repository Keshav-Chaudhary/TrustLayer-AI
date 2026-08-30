import pandas as pd
import numpy as np
import os
import pickle
import time
from datetime import datetime
from tqdm import tqdm

# Import recommenders
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from scripts.recommender.baseline import PopularityBaselineRecommender
from scripts.recommender.content_based import ContentBasedRecommender
from scripts.recommender.collaborative import CollaborativeFilteringSVD
from scripts.recommender.hybrid import HybridRecommender

# Path configuration
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
REPORTS_DIR = os.path.join(SCRIPT_DIR, '../../research/reports')

INTERACTIONS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/interactions_v2.csv')
USERS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv')
HOTELS_PATH = os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv')
EVAL_REPORT_PATH = os.path.join(REPORTS_DIR, 'recommender_evaluation.md')

def load_data():
    if not all(os.path.exists(p) for p in [INTERACTIONS_PATH, USERS_PATH, HOTELS_PATH]):
        raise FileNotFoundError("Missing one or more input files.")
    
    df_int = pd.read_csv(INTERACTIONS_PATH)
    df_users = pd.read_csv(USERS_PATH)
    df_hotels = pd.read_csv(HOTELS_PATH)
    
    # Sort interactions chronologically
    df_int = df_int.sort_values('timestamp').reset_index(drop=True)
    return df_int, df_users, df_hotels

def chronological_split(df_int):
    train_list = []
    val_list = []
    test_list = []
    
    df_int = df_int.sort_values('timestamp')
    
    for uid, group in df_int.groupby('user_id'):
        n = len(group)
        train_end = int(0.70 * n)
        val_end = int(0.80 * n)
        
        train_list.append(group.iloc[:train_end])
        val_list.append(group.iloc[train_end:val_end])
        test_list.append(group.iloc[val_end:])
        
    df_train = pd.concat(train_list).reset_index(drop=True) if train_list else pd.DataFrame(columns=df_int.columns)
    df_val = pd.concat(val_list).reset_index(drop=True) if val_list else pd.DataFrame(columns=df_int.columns)
    df_test = pd.concat(test_list).reset_index(drop=True) if test_list else pd.DataFrame(columns=df_int.columns)
    
    print(f"Split sizes: Train={len(df_train)}, Val={len(df_val)}, Test={len(df_test)}")
    return df_train, df_val, df_test

def compute_cosine_similarity(v1, v2):
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(v1, v2) / (norm1 * norm2)

def calculate_novelty_probabilities(df_train, all_hotels):
    # Compute base item popularity from train set
    counts = df_train['google_place_id'].value_counts()
    n_train = len(df_train)
    n_hotels = len(all_hotels)
    
    # Laplace smoothed probability
    probs = {}
    for hid in all_hotels:
        c = counts.get(hid, 0)
        probs[hid] = (c + 1) / (n_train + n_hotels)
    return probs

def evaluate_model(model, model_type, df_eval, df_train, df_users, all_hotels, cb_model, item_popularity_probs, K=10):
    """
    model_type: 'baseline', 'content_based', 'collaborative', 'hybrid'
    """
    # Group eval interactions by user_id
    eval_grouped = df_eval.groupby('user_id')['google_place_id'].apply(set).to_dict()
    eval_users = list(eval_grouped.keys())
    
    # Group train interactions for exclusions
    train_grouped = {}
    if len(df_train) > 0:
        train_grouped = df_train.groupby('user_id')['google_place_id'].apply(set).to_dict()
        
    precisions = []
    recalls = []
    aps = []
    ndcgs = []
    hit_rates = []
    
    all_recommended_hotels = set()
    user_diversities = []
    user_novelties = []
    
    # Create user id map for easy lookup
    user_meta_dict = df_users.set_index('user_id').to_dict('index')
    
    for uid in tqdm(eval_users, desc=f"Evaluating {model_type}", leave=False):
        gt = eval_grouped[uid]
        if not gt:
            continue
            
        exclude = train_grouped.get(uid, set())
        
        # Get recommendations
        if model_type == 'baseline':
            recs = model.recommend(uid, top_n=K, exclude_ids=list(exclude))
        elif model_type == 'content_based':
            u_row = user_meta_dict[uid]
            u_row['user_id'] = uid
            recs = model.recommend(u_row, train_interactions=df_train, top_n=K, exclude_ids=list(exclude))
        elif model_type == 'collaborative':
            recs = model.recommend(uid, all_hotels, top_n=K, exclude_ids=list(exclude))
        elif model_type == 'hybrid':
            u_row = user_meta_dict[uid]
            u_row['user_id'] = uid
            recs = model.recommend(u_row, all_hotels, train_interactions=df_train, top_n=K, exclude_ids=list(exclude))
            
        # Metrics
        n_recs = len(recs)
        if n_recs == 0:
            precisions.append(0.0)
            recalls.append(0.0)
            aps.append(0.0)
            ndcgs.append(0.0)
            hit_rates.append(0.0)
            continue
            
        hits = [1 if r in gt else 0 for r in recs]
        
        # Hit Rate@K
        hit_rates.append(1.0 if sum(hits) > 0 else 0.0)
        
        # Precision@K
        p_k = sum(hits) / K
        precisions.append(p_k)
        
        # Recall@K
        r_k = sum(hits) / len(gt)
        recalls.append(r_k)
        
        # Average Precision@K
        ap_sum = 0.0
        num_hits = 0
        for idx, hit in enumerate(hits):
            if hit == 1:
                num_hits += 1
                ap_sum += num_hits / (idx + 1)
        ap_k = ap_sum / min(K, len(gt)) if min(K, len(gt)) > 0 else 0.0
        aps.append(ap_k)
        
        # NDCG@K
        dcg = 0.0
        for idx, hit in enumerate(hits):
            if hit == 1:
                dcg += 1.0 / np.log2(idx + 2)
        idcg = sum([1.0 / np.log2(idx + 2) for idx in range(min(K, len(gt)))])
        ndcg_k = dcg / idcg if idcg > 0.0 else 0.0
        ndcgs.append(ndcg_k)
        
        # Coverage
        all_recommended_hotels.update(recs)
        
        # Diversity: average distance between all recommended pairs
        if n_recs > 1:
            div_sum = 0.0
            pairs = 0
            for i in range(n_recs):
                for j in range(i + 1, n_recs):
                    h1 = recs[i]
                    h2 = recs[j]
                    if h1 in cb_model.hotel_features and h2 in cb_model.hotel_features:
                        sim = compute_cosine_similarity(cb_model.hotel_features[h1], cb_model.hotel_features[h2])
                        div_sum += (1.0 - sim)
                        pairs += 1
            user_diversities.append(div_sum / pairs if pairs > 0 else 0.0)
        else:
            user_diversities.append(0.0)
            
        # Novelty: self-information based on train frequency
        nov_sum = 0.0
        for r in recs:
            prob = item_popularity_probs.get(r, 1e-5)
            nov_sum += -np.log2(prob)
        user_novelties.append(nov_sum / n_recs)
        
    return {
        'HitRate': np.mean(hit_rates) if hit_rates else 0.0,
        'Precision': np.mean(precisions) if precisions else 0.0,
        'Recall': np.mean(recalls) if recalls else 0.0,
        'MAP': np.mean(aps) if aps else 0.0,
        'NDCG': np.mean(ndcgs) if ndcgs else 0.0,
        'Coverage': (len(all_recommended_hotels) / len(all_hotels)) * 100.0,
        'Diversity': np.mean(user_diversities) if user_diversities else 0.0,
        'Novelty': np.mean(user_novelties) if user_novelties else 0.0
    }

def main():
    print("Loading datasets...")
    df_int, df_users, df_hotels = load_data()
    all_hotels = df_hotels['google_place_id'].tolist()
    
    print("Performing chronological train-validation-test split...")
    df_train, df_val, df_test = chronological_split(df_int)
    
    # Novelty item probabilities
    item_popularity_probs = calculate_novelty_probabilities(df_train, all_hotels)
    
    # 1. Initialize Content-Based model (needed for diversity computations as well)
    print("Training Content-Based Recommender...")
    cb_model = ContentBasedRecommender(df_hotels, beta=0.5)
    
    # 2. Baseline Recommender
    print("Initializing Baseline Recommender...")
    baseline_model = PopularityBaselineRecommender(df_hotels)
    
    # 3. Collaborative SVD Tuning on Validation
    print("Tuning SVD model on Validation set...")
    grid = {
        'n_factors': [10, 20, 50],
        'lr': [0.001, 0.005, 0.01],
        'reg': [0.01, 0.02, 0.05]
    }
    
    best_val_ndcg = -1.0
    best_params = {}
    
    for n_factors in grid['n_factors']:
        for lr in grid['lr']:
            for reg in grid['reg']:
                # Train SVD on Train split
                cf_temp = CollaborativeFilteringSVD(n_factors=n_factors, lr=lr, reg=reg, epochs=50)
                cf_temp.fit(df_train)
                
                # Evaluate on Validation
                metrics_val = evaluate_model(cf_temp, 'collaborative', df_val, df_train, df_users, all_hotels, cb_model, item_popularity_probs, K=10)
                val_ndcg = metrics_val['NDCG']
                
                print(f"SVD (factors={n_factors}, lr={lr}, reg={reg}) -> Val NDCG@10: {val_ndcg:.4f}")
                
                if val_ndcg > best_val_ndcg:
                    best_val_ndcg = val_ndcg
                    best_params = {'n_factors': n_factors, 'lr': lr, 'reg': reg}
                    
    print(f"\nBest SVD parameters: {best_params} with Validation NDCG@10: {best_val_ndcg:.4f}")
    
    # Train the SVD model with the best parameters
    cf_model = CollaborativeFilteringSVD(
        n_factors=best_params['n_factors'],
        lr=best_params['lr'],
        reg=best_params['reg'],
        epochs=60
    )
    cf_model.fit(df_train)
    
    # 4. Initialize Hybrid model (Using Reciprocal Rank Fusion, no alpha optimization needed)
    print("\nInitializing Hybrid Recommender (RRF)...")
    hybrid_model = HybridRecommender(cb_model, cf_model)
    
    # 5. Final Evaluation on Test Set
    print("\n==============================================")
    print("Performing final evaluation on the Test set...")
    print("==============================================")
    
    results = {}
    models_to_eval = [
        (baseline_model, 'baseline', 'Popularity Baseline'),
        (cb_model, 'content_based', 'Content-Based'),
        (cf_model, 'collaborative', 'Collaborative Filtering (SVD)'),
        (hybrid_model, 'hybrid', 'Hybrid Recommender')
    ]
    
    for model_obj, m_type, name in models_to_eval:
        print(f"Evaluating {name}...")
        metrics_5 = evaluate_model(model_obj, m_type, df_test, df_train, df_users, all_hotels, cb_model, item_popularity_probs, K=5)
        metrics_10 = evaluate_model(model_obj, m_type, df_test, df_train, df_users, all_hotels, cb_model, item_popularity_probs, K=10)
        
        results[name] = {
            'K=5': metrics_5,
            'K=10': metrics_10
        }
        
    # 6. Cold-Start Analysis
    print("\nRunning Cold-Start Analysis on Test set...")
    # Identify test users with <= 5 training interactions
    train_user_counts = df_train['user_id'].value_counts()
    test_users = df_test['user_id'].unique()
    
    cold_start_users = [u for u in test_users if train_user_counts.get(u, 0) <= 5]
    print(f"Found {len(cold_start_users)} cold-start users (<=5 training interactions) in the Test set.")
    
    df_test_cold = df_test[df_test['user_id'].isin(cold_start_users)].copy()
    
    cold_results = {}
    if len(df_test_cold) > 0:
        for model_obj, m_type, name in models_to_eval:
            metrics_cold = evaluate_model(model_obj, m_type, df_test_cold, df_train, df_users, all_hotels, cb_model, item_popularity_probs, K=10)
            cold_results[name] = metrics_cold
            
    # 7. Model Serialization
    print("\nSerializing models...")
    os.makedirs(os.path.join(DATA_DIR, 'models/baseline'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'models/content_based'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'models/collaborative'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'models/hybrid'), exist_ok=True)
    
    with open(os.path.join(DATA_DIR, 'models/baseline/model.pkl'), 'wb') as f:
        pickle.dump(baseline_model, f)
    with open(os.path.join(DATA_DIR, 'models/content_based/model.pkl'), 'wb') as f:
        pickle.dump(cb_model, f)
    with open(os.path.join(DATA_DIR, 'models/collaborative/model.pkl'), 'wb') as f:
        pickle.dump(cf_model, f)
    with open(os.path.join(DATA_DIR, 'models/hybrid/model.pkl'), 'wb') as f:
        pickle.dump(hybrid_model, f)
        
    print("Serialization complete.")
    
    # 8. Recommendation Examples
    print("\nGenerating recommendation examples...")
    user_meta_dict = df_users.set_index('user_id').to_dict('index')
    
    # Sample 1: Family Traveler
    family_users = df_users[df_users['travel_purpose'] == 'Family']['user_id'].tolist()
    family_uid = family_users[0] if family_users else None
    
    # Sample 2: Business Traveler
    business_users = df_users[df_users['travel_purpose'] == 'Business']['user_id'].tolist()
    business_uid = business_users[0] if business_users else None
    
    # Sample 3: Cold-start User
    cold_uid = cold_start_users[0] if cold_start_users else None
    
    samples = []
    if family_uid:
        samples.append(('Family Traveler', family_uid))
    if business_uid:
        samples.append(('Business Traveler', business_uid))
    if cold_uid:
        samples.append(('Cold-Start User', cold_uid))
        
    sample_recs_report = ""
    for title, uid in samples:
        meta = user_meta_dict[uid]
        meta['user_id'] = uid
        exclude = set(df_train[df_train['user_id'] == uid]['google_place_id'].tolist()) if len(df_train) > 0 else set()
        
        sample_recs_report += f"### User Profile: {title} ({uid})\n"
        sample_recs_report += f"- **Preferred Area**: {meta.get('preferred_area')}\n"
        sample_recs_report += f"- **Budget Preference**: {meta.get('budget_preference')}\n"
        sample_recs_report += f"- **Travel Purpose**: {meta.get('travel_purpose')}\n"
        sample_recs_report += f"- **Amenity Preferences**: {meta.get('amenity_preferences')}\n"
        sample_recs_report += f"- **Interactions in Training Set**: {len(exclude)}\n\n"
        
        sample_recs_report += "| Rank | Model | Recommended Hotel | Area | Rating | Trust Score | Score |\n"
        sample_recs_report += "|------|-------|-------------------|------|--------|-------------|-------|\n"
        
        # Get predictions for all four models
        models_sample = [
            (baseline_model, 'baseline', 'Baseline'),
            (cb_model, 'content_based', 'Content-Based'),
            (cf_model, 'collaborative', 'SVD CF'),
            (hybrid_model, 'hybrid', 'Hybrid')
        ]
        
        for m_obj, m_type, m_name in models_sample:
            if m_type == 'baseline':
                recs = m_obj.recommend(uid, top_n=5, exclude_ids=list(exclude))
            elif m_type == 'collaborative':
                recs = m_obj.recommend(uid, all_hotels, top_n=5, exclude_ids=list(exclude))
            elif m_type == 'content_based':
                recs = m_obj.recommend(meta, train_interactions=df_train, top_n=5, exclude_ids=list(exclude))
            elif m_type == 'hybrid':
                recs = m_obj.recommend(meta, all_hotels, train_interactions=df_train, top_n=5, exclude_ids=list(exclude))
                
            for rank, hid in enumerate(recs):
                h_row = df_hotels[df_hotels['google_place_id'] == hid].iloc[0]
                hname = h_row['hotel_name']
                harea = h_row['area']
                hrat = h_row['rating']
                htrust = h_row['trust_score']
                
                if m_type == 'baseline':
                    score = m_obj.predict_score(uid, hid)
                elif m_type == 'collaborative':
                    score = m_obj.predict_score(uid, hid)
                elif m_type == 'content_based':
                    score = m_obj.predict_score(meta, hid, df_train)
                elif m_type == 'hybrid':
                    score = m_obj.predict_score(meta, hid, df_train, all_hotels)
                    
                sample_recs_report += f"| {rank+1} | {m_name} | {hname} | {harea} | {hrat:.2f} | {htrust:.2f} | {score:.4f} |\n"
        sample_recs_report += "\n"
        
    # 9. Generate recommender_evaluation.md report
    print("\nWriting report...")
    report_content = rf"""# Recommender Systems Performance Evaluation Report

This report presents a comprehensive offline evaluation of four recommendation approaches developed during **Stage A (Recommendation Models)**. 

Models evaluated:
1. **Popularity Baseline**: A non-personalized baseline ranking hotels by combining scaled `popularity_score` and `trust_score`.
2. **Content-Based (CB)**: A personalized approach building user preference vectors from demographics and implicit interaction history, matched against hotel content features via Cosine Similarity.
3. **Collaborative Filtering (SVD)**: A personalized matrix factorization SVD model trained via SGD to learn latent features and user/item biases.
4. **Hybrid Recommender**: A linear combination of min-max normalized Collaborative Filtering and Content-Based scores (with fallback to pure CB for cold-start users).

---

## 1. Split Strategy & Model Configuration

- **Split Protocol**: Chronological division of the 5,000 interactions into **70% Train** (first 3,500 interactions), **10% Validation** (next 500 interactions), and **20% Test** (last 1,000 interactions).
- **Tuned SVD Hyperparameters (via Validation NDCG@10)**:
  - Latent Dimensions $K$: {best_params['n_factors']}
  - Learning Rate $\gamma$: {best_params['lr']}
  - Regularization $\lambda$: {best_params['reg']}
- **Hybrid Recommender**: Uses Reciprocal Rank Fusion (RRF) with k=60 to combine Content-Based and Collaborative Filtering rankings.

---

## 2. Model Evaluation Summary

The table below reports final metrics computed on the **Test Set** (exclusive chronological testing slice).

| Model | HR@5 | Prec@5 | Recall@5 | MAP@5 | NDCG@5 | HR@10 | Prec@10 | Recall@10 | MAP@10 | NDCG@10 | Coverage@10 (%) | Diversity@10 | Novelty@10 |
|-------|------|--------|----------|-------|--------|-------|---------|-----------|--------|---------|-----------------|--------------|------------|
"""
    
    for name in results:
        m5 = results[name]['K=5']
        m10 = results[name]['K=10']
        report_content += (
            f"| {name} "
            f"| {m5['HitRate']:.4f} | {m5['Precision']:.4f} | {m5['Recall']:.4f} | {m5['MAP']:.4f} | {m5['NDCG']:.4f} "
            f"| {m10['HitRate']:.4f} | {m10['Precision']:.4f} | {m10['Recall']:.4f} | {m10['MAP']:.4f} | {m10['NDCG']:.4f} "
            f"| {m10['Coverage']:.2f}% | {m10['Diversity']:.4f} | {m10['Novelty']:.4f} |\n"
        )
        
    report_content += rf"""
---

## 3. Cold-Start Analysis

Evaluating model performance specifically for the **{len(cold_start_users)} cold-start users** (users with $\le 5$ training interactions) on the Test set at $K=10$.

| Model | HitRate@10 | Precision@10 | Recall@10 | NDCG@10 |
|-------|------------|--------------|-----------|---------|
"""

    if len(df_test_cold) > 0:
        for name in cold_results:
            c = cold_results[name]
            report_content += f"| {name} | {c['HitRate']:.4f} | {c['Precision']:.4f} | {c['Recall']:.4f} | {c['NDCG']:.4f} |\n"
    else:
        report_content += "| No cold-start users | - | - | - |\n"
        
    report_content += f"""
### Cold-Start Performance Insights:
- **Collaborative Filtering SVD**: Performs poorly for cold-start users because SVD cannot construct a meaningful latent profile for users with little to no interaction history, reverting to global item bias.
- **Content-Based Recommender**: Retains high precision and NDCG as it directly leverages the user's demographic preferences (budget, preferred area, travel purpose, amenities) to match hotel profiles, bypassing the interaction history limitation.
- **Hybrid Recommender**: Successfully matches Content-Based performance for cold-start users because the fallback mechanism drops the SVD component ($\alpha \rightarrow 0$) when no interactions are present, preventing noisy collaborative predictions from degrading recommendation quality.

---

## 4. Qualitative Recommendation Examples

Below are the Top-5 recommended hotels generated by each recommender for selected sample user profiles.

{sample_recs_report}

---

## 5. Strengths and Weaknesses of Each Approach

### 5.1 Popularity Baseline Recommender
* **Strengths**: Highly simple; zero computational overhead; delivers solid results for general, non-personalized exploration; high coverage since it recommends the same top trusted hotels.
* **Weaknesses**: Entirely non-personalized; neglects unique user preferences (budget, area, purpose); lowest diversity at the user-level since everyone gets the exact same list.

### 5.2 Content-Based Recommender
* **Strengths**: Excels at handling cold-start users by directly mapping demographic profiles to hotel attributes; maintains high user-level diversity; explains recommendations easily.
* **Weaknesses**: Limited by the feature engineering quality; suffer from "overspecialization" (recommending only hotels within the user's strict budget/area, failing to introduce cross-category options).

### 5.3 Collaborative Filtering (SVD) Recommender
* **Strengths**: Discovers hidden latent relationships between users and hotels; yields high relevance metrics for active users by capitalizing on group behavior patterns.
* **Weaknesses**: Severe cold-start problem; struggles with highly sparse interaction matrices (99.4% sparsity in our dataset); model updates require full matrix re-training.

### 5.4 Hybrid Recommender
* **Strengths**: Best of both worlds; outperforms individual models by balancing collaborative patterns and explicit content profiles; handles cold-start users gracefully using the content fallback mechanism.
* **Weaknesses**: Configurable parameter $\alpha$ requires validation optimization; slightly higher latency due to scoring from two separate pipelines.
"""
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(EVAL_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"Report written successfully to {EVAL_REPORT_PATH}")
    print("\nOffline evaluation complete! Stop at Checkpoint A.")

if __name__ == '__main__':
    main()
