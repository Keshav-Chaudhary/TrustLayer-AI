import pandas as pd
import numpy as np
import os
import pickle
from tqdm import tqdm
import json
from collections import defaultdict

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from scripts.recommender.baseline import PopularityBaselineRecommender
from scripts.recommender.content_based import ContentBasedRecommender
from scripts.recommender.collaborative import CollaborativeFilteringSVD
from scripts.recommender.hybrid import HybridRecommender
from scripts.explainability.explainer import RecommendationExplainer

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
MODELS_DIR = os.path.join(SCRIPT_DIR, '../../data/models')
REPORTS_DIR = os.path.join(SCRIPT_DIR, '../../research/reports')

INTERACTIONS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/interactions_v2.csv')
USERS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv')
HOTELS_PATH = os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv')
REPORT_PATH = os.path.join(REPORTS_DIR, 'explainability_audit_b1.md')

def load_data():
    df_int = pd.read_csv(INTERACTIONS_PATH)
    df_users = pd.read_csv(USERS_PATH)
    df_hotels = pd.read_csv(HOTELS_PATH)
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
    df_train = pd.concat(train_list).reset_index(drop=True)
    df_val = pd.concat(val_list).reset_index(drop=True)
    df_test = pd.concat(test_list).reset_index(drop=True)
    return df_train, df_val, df_test

def get_hybrid_rankings(hybrid_model, user_row, all_hotels, df_train, u_vec=None):
    cb = hybrid_model.cb_model
    cf = hybrid_model.cf_model
    k = hybrid_model.k
    
    if u_vec is None:
        u_vec = cb._get_user_vector(user_row, df_train)
        
    cb_scores = []
    cf_scores = []
    uid = user_row['user_id']
    
    for hid in all_hotels:
        cb_scores.append(cb.predict_score(user_row, hid, precomputed_u_vec=u_vec))
        cf_scores.append(cf.predict_score(uid, hid))
        
    cb_scores = np.array(cb_scores)
    cf_scores = np.array(cf_scores)
    
    cb_ranks = {all_hotels[idx]: rank + 1 for rank, idx in enumerate(np.argsort(cb_scores)[::-1])}
    cf_ranks = {all_hotels[idx]: rank + 1 for rank, idx in enumerate(np.argsort(cf_scores)[::-1])}
    
    user_ints = df_train[df_train['user_id'] == uid] if len(df_train) > 0 else []
    is_cold = len(user_ints) <= 5
    
    hybrid_scores = {}
    for hid in all_hotels:
        if is_cold:
            hybrid_scores[hid] = 1.0 / (k + cb_ranks[hid])
        else:
            hybrid_scores[hid] = 1.0 / (k + cb_ranks[hid]) + 1.0 / (k + cf_ranks[hid])
            
    sorted_recs = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    ranks = {item[0]: rank + 1 for rank, item in enumerate(sorted_recs)}
    scores = hybrid_scores
    return ranks, scores

def compute_jaccard(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    if not s1 and not s2:
        return 1.0
    return len(s1.intersection(s2)) / len(s1.union(s2))

def main():
    print("Loading data...")
    df_int, df_users, df_hotels = load_data()
    all_hotels = df_hotels['google_place_id'].tolist()
    
    df_train, _, df_test = chronological_split(df_int)
    
    print("Loading models...")
    with open(os.path.join(MODELS_DIR, 'content_based/model.pkl'), 'rb') as f:
        cb_model = pickle.load(f)
    with open(os.path.join(MODELS_DIR, 'collaborative/model.pkl'), 'rb') as f:
        cf_model = pickle.load(f)
        
    hybrid_model = HybridRecommender(cb_model, cf_model, k=60)
    explainer = RecommendationExplainer(hybrid_model)
    
    test_users = df_test['user_id'].unique()
    rng = np.random.default_rng(42)
    sample_users = rng.choice(test_users, size=min(100, len(test_users)), replace=False)
    
    explanations = []
    
    # Fidelity Tracking
    fidelity_stats = defaultdict(lambda: {'count': 0, 'drops': 0, 'rank_changes': [], 'score_changes': [], 'evictions': 0})
    
    # RRF Tracking
    rrf_correct = 0
    rrf_total = 0
    
    # Confidence Tracking
    conf_stats = {'High': [], 'Medium': [], 'Low': []}
    
    # Diversity Tracking
    templates = set()
    factor_combos = set()
    user_diversity = []
    
    print("Running audit...")
    for uid in tqdm(sample_users):
        user_row = df_users[df_users['user_id'] == uid].iloc[0]
        
        # Interactions
        user_ints = df_train[df_train['user_id'] == uid]
        int_count = len(user_ints)
        
        # Original vectors
        orig_u_vec = cb_model._get_user_vector(user_row, df_train)
        orig_ranks, orig_scores = get_hybrid_rankings(hybrid_model, user_row, all_hotels, df_train, orig_u_vec)
        
        # Top 10
        top10 = [h for h, r in orig_ranks.items() if r <= 10]
        
        user_factors_list = []
        
        for idx, hid in enumerate(top10):
            exp = explainer.explain(user_row, hid, all_hotels, train_interactions=df_train)
            explanations.append(exp)
            
            # Record diversity
            nlg_template = exp['nlg_text'].split("Confidence:")[0].strip()
            templates.add(nlg_template)
            factor_combo = tuple(sorted(exp['top_factors']))
            factor_combos.add(factor_combo)
            user_factors_list.append(factor_combo)
            
            # Confidence
            conf_stats[exp['confidence']].append({'int_count': int_count, 'rank': orig_ranks[hid]})
            
            # RRF Accuracy Check
            rrf_total += 1
            cb_c = 1.0 / (60 + exp['cb_rank'])
            cf_c = 1.0 / (60 + exp['cf_rank'])
            tot = cb_c + cf_c if int_count > 5 else cb_c
            if int_count <= 5:
                cb_pct = 1.0
                cf_pct = 0.0
            else:
                cb_pct = cb_c / tot
                cf_pct = cf_c / tot
                
            expected_type = "balanced_hybrid"
            if cb_pct > 0.6: expected_type = "cb_dominant"
            elif cf_pct > 0.6: expected_type = "cf_dominant"
            
            if expected_type == exp['explanation_type']:
                rrf_correct += 1
                
            # Fidelity Ablation
            # Only ablate for rank 1-3 to save time, or randomly
            if idx < 3:
                for factor in exp['top_factors']:
                    if factor in ["popularity_fallback", "similar_to_past_view"]:
                        continue # these aren't explicit CB features to zero out
                        
                    ablated_vec = orig_u_vec.copy()
                    if factor == "area_match":
                        ablated_vec[explainer.area_start:explainer.area_end] = 0
                    elif factor == "budget_match":
                        ablated_vec[explainer.budget_start:explainer.budget_end] = 0
                    elif factor == "high_trust_score":
                        ablated_vec[5] = 0 # trust score index
                    elif "_sentiment" in factor:
                        sentiment_name = factor.split("_sentiment")[0] + "_score"
                        if sentiment_name in explainer.aspects:
                            s_idx = explainer.aspects.index(sentiment_name)
                            ablated_vec[s_idx] = 0
                            
                    # Recompute ranks
                    new_ranks, new_scores = get_hybrid_rankings(hybrid_model, user_row, all_hotels, df_train, ablated_vec)
                    
                    orig_r = orig_ranks[hid]
                    new_r = new_ranks[hid]
                    orig_s = orig_scores[hid]
                    new_s = new_scores[hid]
                    
                    rank_change = new_r - orig_r # Positive means rank dropped (e.g. 1 -> 5)
                    score_change = new_s - orig_s # Negative means score dropped
                    
                    fidelity_stats[factor]['count'] += 1
                    fidelity_stats[factor]['rank_changes'].append(rank_change)
                    fidelity_stats[factor]['score_changes'].append(score_change)
                    if rank_change > 0:
                        fidelity_stats[factor]['drops'] += 1
                    if orig_r <= 10 and new_r > 10:
                        fidelity_stats[factor]['evictions'] += 1
                        
        # Intra-user diversity/consistency
        # Compute average Jaccard between all pairs of top factors for this user
        jaccards = []
        for i in range(len(user_factors_list)):
            for j in range(i+1, len(user_factors_list)):
                jaccards.append(compute_jaccard(user_factors_list[i], user_factors_list[j]))
        if jaccards:
            user_diversity.append(1.0 - np.mean(jaccards)) # 1 - similarity = diversity
            
    # Intra-User Consistency
    # Jaccard similarities already computed in user_diversity
    avg_intra_consistency = 1.0 - np.mean(user_diversity) if user_diversity else 0.0

    # Write report
    print("Writing report...")
    with open(REPORT_PATH, 'w') as f:
        f.write("# Stage B.1: Explainability Validation Audit Report\n\n")
        
        f.write("## 1. Fidelity Breakdown\n")
        f.write("| Factor | Frequency | Drop Frequency | Drop % | Mean Rank Change | Median Rank Change | Score Change | Top-10 Eviction % |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for factor, stats in fidelity_stats.items():
            if stats['count'] == 0: continue
            drop_pct = (stats['drops'] / stats['count']) * 100
            evict_pct = (stats['evictions'] / stats['count']) * 100
            mean_rc = np.mean(stats['rank_changes'])
            med_rc = np.median(stats['rank_changes'])
            mean_sc = np.mean(stats['score_changes'])
            f.write(f"| {factor} | {stats['count']} | {stats['drops']} | {drop_pct:.2f}% | {mean_rc:.2f} | {med_rc:.1f} | {mean_sc:.4f} | {evict_pct:.2f}% |\n")
            
        f.write("\n## 2. Expanded RRF Validation\n")
        f.write(f"- Explanations Evaluated: {rrf_total}\n")
        f.write(f"- Classification Accuracy: {(rrf_correct / rrf_total * 100) if rrf_total else 0:.2f}%\n")
        
        f.write("\n## 3. Explanation-Type Distribution\n")
        type_counts = defaultdict(int)
        for exp in explanations:
            # Check for fallback
            if len(exp['top_factors']) == 1 and exp['top_factors'][0] == "popularity_fallback":
                type_counts['fallback'] += 1
            else:
                type_counts[exp['explanation_type']] += 1
                
        f.write("| Type | Count | Percentage |\n")
        f.write("|---|---|---|\n")
        for t, c in type_counts.items():
            f.write(f"| {t} | {c} | {(c / len(explanations) * 100):.2f}% |\n")
            
        f.write("\n## 4. Confidence Calibration\n")
        f.write("| Confidence | Count | Avg Training Interactions | Avg Final Rank |\n")
        f.write("|---|---|---|---|\n")
        for conf, data in conf_stats.items():
            if not data: continue
            avg_int = np.mean([d['int_count'] for d in data])
            avg_rank = np.mean([d['rank'] for d in data])
            f.write(f"| {conf} | {len(data)} | {avg_int:.2f} | {avg_rank:.2f} |\n")
            
        f.write("\n## 5. Explanation Diversity Audit\n")
        f.write(f"- **Unique Explanation Templates (NLG Strings)**: {len(templates)}\n")
        f.write(f"- **Unique Top-Factors Combinations**: {len(factor_combos)}\n")
        f.write(f"- **Average Explanation Diversity per User (1 - Jaccard)**: {np.mean(user_diversity) if user_diversity else 0:.4f}\n")
        
        f.write("\n## 6. Consistency Evaluation\n")
        f.write(f"- **Intra-User Consistency (Mean Jaccard)**: {avg_intra_consistency:.4f}\n")
        
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
