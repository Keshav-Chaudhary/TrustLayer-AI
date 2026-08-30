import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Cell 0: Imports
cells.append(nbf.v4.new_markdown_cell("# Stage A Recommender Diagnostics\nThis notebook investigates the failures observed during the offline evaluation of the Stage A recommendation models."))

code_imports = """
import os
import sys
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

sys.path.append('../../')
from scripts.recommender.baseline import PopularityBaselineRecommender
from scripts.recommender.content_based import ContentBasedRecommender
from scripts.recommender.collaborative import CollaborativeFilteringSVD
from scripts.recommender.hybrid import HybridRecommender

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

DATA_DIR = '../../data'
"""
cells.append(nbf.v4.new_code_cell(code_imports))

# Cell 1: Load Data & Split
code_data = """
# Load Data
df_int = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/interactions.csv'))
df_users = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv'))
df_hotels = pd.read_csv(os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv'))

# Chronological Split
def chronological_split(df_int):
    train_list, val_list, test_list = [], [], []
    df_int = df_int.sort_values('timestamp')
    for uid, group in df_int.groupby('user_id'):
        n = len(group)
        train_list.append(group.iloc[:int(0.70 * n)])
        val_list.append(group.iloc[int(0.70 * n):int(0.80 * n)])
        test_list.append(group.iloc[int(0.80 * n):])
    return pd.concat(train_list).reset_index(drop=True), pd.concat(val_list).reset_index(drop=True), pd.concat(test_list).reset_index(drop=True)

df_train, df_val, df_test = chronological_split(df_int)
all_hotels = df_hotels['google_place_id'].tolist()
print(f"Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")
"""
cells.append(nbf.v4.new_markdown_cell("## 1. Data Loading & Chronological Split"))
cells.append(nbf.v4.new_code_cell(code_data))

# Cell 2: Load Models
code_models = """
with open(os.path.join(DATA_DIR, 'models/baseline/model.pkl'), 'rb') as f:
    baseline_model = pickle.load(f)
with open(os.path.join(DATA_DIR, 'models/content_based/model.pkl'), 'rb') as f:
    cb_model = pickle.load(f)
with open(os.path.join(DATA_DIR, 'models/collaborative/model.pkl'), 'rb') as f:
    cf_model = pickle.load(f)
with open(os.path.join(DATA_DIR, 'models/hybrid/model.pkl'), 'rb') as f:
    hybrid_model = pickle.load(f)
    
print("Models loaded successfully.")
"""
cells.append(nbf.v4.new_markdown_cell("## 2. Load Trained Models"))
cells.append(nbf.v4.new_code_cell(code_models))

# Cell 3: Interaction Dataset Audit
code_interactions = """
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Interaction types
sns.countplot(data=df_int, x='interaction_type', order=['view', 'click', 'rating', 'booking'], ax=axes[0])
axes[0].set_title('Distribution of Interaction Types')

# Interactions per user
user_counts = df_int['user_id'].value_counts()
sns.histplot(user_counts, bins=20, ax=axes[1])
axes[1].set_title('Interactions per User')
plt.show()

# Hotel popularity (long tail)
hotel_counts = df_int['google_place_id'].value_counts().values
plt.figure(figsize=(10, 5))
plt.plot(hotel_counts)
plt.title('Hotel Popularity (Long Tail)')
plt.xlabel('Hotel Rank')
plt.ylabel('Number of Interactions')
plt.show()
"""
cells.append(nbf.v4.new_markdown_cell("## 3. Interaction Dataset Audit"))
cells.append(nbf.v4.new_code_cell(code_interactions))

# Cell 4: Matrix Sparsity & CF Audit
code_cf = """
n_users = df_int['user_id'].nunique()
n_items = df_hotels['google_place_id'].nunique()
n_interactions = len(df_int)
sparsity = 1.0 - (n_interactions / (n_users * n_items))

print(f"User-Item Matrix Sparsity: {sparsity * 100:.4f}%")

# Plot SVD Training Loss
if hasattr(cf_model, 'history') and 'loss' in cf_model.history:
    plt.figure(figsize=(8, 5))
    plt.plot(cf_model.history['loss'], marker='o')
    plt.title('SVD Training Loss (MSE) over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.show()
else:
    print("SVD model does not have loss history tracked.")
"""
cells.append(nbf.v4.new_markdown_cell("## 4. Collaborative Filtering Audit & Matrix Sparsity"))
cells.append(nbf.v4.new_code_cell(code_cf))

# Cell 5: Hybrid Calibration & Alpha Optimization
code_hybrid = """
# Test scores for a sample user
sample_user = df_users.iloc[0]
candidates = all_hotels[:200]

cb_u_vec = cb_model._get_user_vector(sample_user, df_train)
cb_scores = [cb_model.predict_score(sample_user, hid, precomputed_u_vec=cb_u_vec) for hid in candidates]
cf_scores = [cf_model.predict_score(sample_user['user_id'], hid) for hid in candidates]

plt.figure(figsize=(10, 5))
sns.histplot(cb_scores, color='blue', alpha=0.5, label='CB Scores (Cosine Sim)', kde=True)
sns.histplot(cf_scores, color='red', alpha=0.5, label='CF Scores (SVD Pred)', kde=True)
plt.title('Distribution of Raw Scores (CB vs CF)')
plt.legend()
plt.show()
"""
cells.append(nbf.v4.new_markdown_cell("## 5. Hybrid Failure Analysis (Score Calibration)"))
cells.append(nbf.v4.new_code_cell(code_hybrid))

# Cell 6: Recommendation Overlap
code_overlap = """
user_sample = df_users['user_id'].head(50).tolist()
user_meta_dict = df_users.set_index('user_id').to_dict('index')

recs_dict = {'Baseline': [], 'CB': [], 'CF': [], 'Hybrid': []}

for uid in tqdm(user_sample):
    u_row = user_meta_dict[uid]
    u_row['user_id'] = uid
    recs_dict['Baseline'].append(set(baseline_model.recommend(uid, top_n=10)))
    recs_dict['CB'].append(set(cb_model.recommend(u_row, train_interactions=df_train, top_n=10)))
    recs_dict['CF'].append(set(cf_model.recommend(uid, all_hotels, top_n=10)))
    recs_dict['Hybrid'].append(set(hybrid_model.recommend(u_row, all_hotels, train_interactions=df_train, top_n=10)))

# Compute pairwise Jaccard similarity
models = ['Baseline', 'CB', 'CF', 'Hybrid']
sim_matrix = np.zeros((4, 4))

def jaccard(s1, s2):
    return len(s1.intersection(s2)) / len(s1.union(s2)) if len(s1.union(s2)) > 0 else 0

for i, m1 in enumerate(models):
    for j, m2 in enumerate(models):
        avg_sim = np.mean([jaccard(recs_dict[m1][k], recs_dict[m2][k]) for k in range(len(user_sample))])
        sim_matrix[i, j] = avg_sim

plt.figure(figsize=(8, 6))
sns.heatmap(sim_matrix, annot=True, xticklabels=models, yticklabels=models, cmap='YlGnBu')
plt.title('Recommendation Overlap (Jaccard Similarity)')
plt.show()
"""
cells.append(nbf.v4.new_markdown_cell("## 6. Recommendation Overlap Analysis"))
cells.append(nbf.v4.new_code_cell(code_overlap))

# Cell 7: Cold-Start Audit
code_cold = """
train_counts = df_train['user_id'].value_counts()
test_users = df_test['user_id'].unique()
cold_start_users = [u for u in test_users if train_counts.get(u, 0) <= 1]

print(f"Total Test Users: {len(test_users)}")
print(f"Cold-Start Users (<=1 train interactions): {len(cold_start_users)}")

# Re-evaluating cold-start specifically
df_test_cold = df_test[df_test['user_id'].isin(cold_start_users)]
print(f"Interactions from cold-start users in Test set: {len(df_test_cold)}")

if len(df_test_cold) > 0:
    eval_grouped = df_test_cold.groupby('user_id')['google_place_id'].apply(set).to_dict()
    cold_uids = list(eval_grouped.keys())
    
    cb_hits = 0
    cf_hits = 0
    total_recs = len(cold_uids)
    
    for uid in cold_uids:
        gt = eval_grouped[uid]
        u_row = user_meta_dict[uid]
        u_row['user_id'] = uid
        
        cb_recs = cb_model.recommend(u_row, train_interactions=df_train, top_n=10)
        cf_recs = cf_model.recommend(uid, all_hotels, top_n=10)
        
        if any(r in gt for r in cb_recs): cb_hits += 1
        if any(r in gt for r in cf_recs): cf_hits += 1
        
    print(f"CB Cold-Start HitRate@10: {cb_hits / total_recs:.4f}")
    print(f"CF Cold-Start HitRate@10: {cf_hits / total_recs:.4f}")
else:
    print("No cold start interactions found to evaluate.")
"""
cells.append(nbf.v4.new_markdown_cell("## 7. Cold-Start Audit"))
cells.append(nbf.v4.new_code_cell(code_cold))

nb.cells = cells
with open('D:/Side_Projects/0_Independent_Project/TrustLayer-AI/scripts/evaluation/generate_diagnostics_nb.py', 'w') as f:
    f.write('import nbformat as nbf\\nnb = nbf.v4.new_notebook()\\n') # Skip writing itself, just save directly

# Just directly write the nb object
nbf.write(nb, 'D:/Side_Projects/0_Independent_Project/TrustLayer-AI/research/notebooks/09_recommender_diagnostics.ipynb')
