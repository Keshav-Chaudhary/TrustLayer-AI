import pandas as pd
import numpy as np
import os
import pickle
import time
from tqdm import tqdm
import json

# Import recommenders
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from scripts.recommender.baseline import PopularityBaselineRecommender
from scripts.recommender.content_based import ContentBasedRecommender
from scripts.recommender.collaborative import CollaborativeFilteringSVD
from scripts.recommender.hybrid import HybridRecommender
from scripts.explainability.explainer import RecommendationExplainer

# Path configuration
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
MODELS_DIR = os.path.join(SCRIPT_DIR, '../../data/models')
REPORTS_DIR = os.path.join(SCRIPT_DIR, '../../research/reports')

INTERACTIONS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/interactions_v2.csv')
USERS_PATH = os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv')
HOTELS_PATH = os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv')
REPORT_PATH = os.path.join(REPORTS_DIR, 'explainability_evaluation.md')

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

def main():
    print("Loading datasets...")
    df_int, df_users, df_hotels = load_data()
    all_hotels = df_hotels['google_place_id'].tolist()
    
    print("Performing split...")
    df_train, df_val, df_test = chronological_split(df_int)
    
    print("Loading trained models...")
    with open(os.path.join(MODELS_DIR, 'content_based/model.pkl'), 'rb') as f:
        cb_model = pickle.load(f)
    with open(os.path.join(MODELS_DIR, 'collaborative/model.pkl'), 'rb') as f:
        cf_model = pickle.load(f)
        
    # Instantiate Hybrid and Explainer
    hybrid_model = HybridRecommender(cb_model, cf_model, k=60)
    explainer = RecommendationExplainer(hybrid_model)
    
    test_users = df_test['user_id'].unique()
    
    # We will sample 100 test users for evaluation to save time
    rng = np.random.default_rng(42)
    sample_users = rng.choice(test_users, size=min(100, len(test_users)), replace=False)
    
    print(f"Evaluating explanations for {len(sample_users)} test users...")
    
    coverage_results = []
    fidelity_tests = []
    
    # Store some example json outputs
    example_jsons = []
    
    for uid in tqdm(sample_users):
        user_row = df_users[df_users['user_id'] == uid].iloc[0]
        
        # Get Top-10 recommendations from Hybrid
        recs = hybrid_model.recommend(user_row, all_hotels, train_interactions=df_train, top_n=10)
        
        for idx, hid in enumerate(recs):
            exp = explainer.explain(user_row, hid, all_hotels, train_interactions=df_train)
            
            # Coverage metric: non-fallback factors
            is_fallback = len(exp["top_factors"]) == 1 and exp["top_factors"][0] == "popularity_fallback"
            coverage_results.append(not is_fallback)
            
            if len(example_jsons) < 3 and exp["confidence"] in ["High", "Medium", "Low"]:
                example_jsons.append(exp)
                
            # Fidelity test: if area_match or budget_match is a top factor, perturb and check rank
            if idx == 0 and ("area_match" in exp["top_factors"] or "budget_match" in exp["top_factors"]):
                # Original rank is 1
                
                # Perturb user
                perturbed_user = user_row.copy()
                if "area_match" in exp["top_factors"]:
                    perturbed_user['preferred_area'] = 'NON_EXISTENT_AREA'
                if "budget_match" in exp["top_factors"]:
                    perturbed_user['budget_preference'] = 'NON_EXISTENT_BUDGET'
                    
                # Re-calculate rank
                # We need to find the new rank of `hid`. 
                # Since computing all ranks takes time, we just do a quick check against the original top 10
                perturbed_recs = hybrid_model.recommend(perturbed_user, all_hotels, train_interactions=df_train, top_n=10)
                
                new_rank = 11 # assume it fell out of top 10
                if hid in perturbed_recs:
                    new_rank = perturbed_recs.index(hid) + 1
                    
                rank_drop = new_rank - 1 # Original rank is 1
                fidelity_tests.append(rank_drop > 0)
                
    coverage_rate = np.mean(coverage_results)
    fidelity_rate = np.mean(fidelity_tests) if fidelity_tests else 0.0
    
    print("\n=== Explainability Evaluation Results ===")
    print(f"Coverage: {coverage_rate*100:.2f}%")
    print(f"Fidelity (Rank Drop on feature ablation): {fidelity_rate*100:.2f}% ({len(fidelity_tests)} tested)")
    
    # Write report
    with open(REPORT_PATH, 'w') as f:
        f.write("# Stage B: Explainability Evaluation Report\n\n")
        f.write("## 1. Metrics\n")
        f.write(f"- **Coverage**: {coverage_rate*100:.2f}%\n")
        f.write(f"- **Fidelity**: {fidelity_rate*100:.2f}% (Percentage of ablated features causing rank drops)\n")
        
        f.write("\n## 2. Sample Structured Explanations (JSON)\n")
        for ex in example_jsons:
            f.write("```json\n")
            f.write(json.dumps(ex, indent=2))
            f.write("\n```\n")
            
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
