import nbformat as nbf
import pandas as pd
import numpy as np
import os
import sys

nb = nbf.v4.new_notebook()
cells = []

# Cell 0: Imports
cells.append(nbf.v4.new_markdown_cell("# Stage A.1: Interaction Quality Audit\nThis notebook evaluates the new `interactions_v2.csv` synthetic dataset to ensure strict user preference alignment and long-tail user activity distribution."))

code_imports = """
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

DATA_DIR = '../../data'
"""
cells.append(nbf.v4.new_code_cell(code_imports))

# Cell 1: Load Data
code_data = """
df_int = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/interactions_v2.csv'))
df_users = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv'))
df_hotels = pd.read_csv(os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv'))

print(f"Total Interactions: {len(df_int)}")
"""
cells.append(nbf.v4.new_code_cell(code_data))

# Cell 2: User Activity Distribution
code_activity = """
user_counts = df_int['user_id'].value_counts()

plt.figure(figsize=(10, 5))
sns.histplot(user_counts, bins=30, kde=True)
plt.title('User Activity Distribution (Interactions per User)')
plt.xlabel('Number of Interactions')
plt.ylabel('Number of Users')
plt.show()

print("Activity Quantiles:")
print(user_counts.quantile([0.25, 0.5, 0.75, 0.9, 0.95]))
"""
cells.append(nbf.v4.new_markdown_cell("## 1. User Activity Distribution"))
cells.append(nbf.v4.new_code_cell(code_activity))

# Cell 3: Hotel Popularity
code_pop = """
hotel_counts = df_int['google_place_id'].value_counts().values
plt.figure(figsize=(10, 5))
plt.plot(hotel_counts)
plt.title('Hotel Popularity (Long Tail)')
plt.xlabel('Hotel Rank')
plt.ylabel('Number of Interactions')
plt.show()
"""
cells.append(nbf.v4.new_markdown_cell("## 2. Hotel Popularity Distribution"))
cells.append(nbf.v4.new_code_cell(code_pop))

# Cell 4: Alignment Calculation
code_align = """
merged = df_int.merge(df_users, on='user_id', how='left').merge(df_hotels, on='google_place_id', how='left')

# 1. Area Alignment
area_match = (merged['preferred_area'] == merged['area']).mean()

# 2. Budget Alignment
budget_match = (merged['budget_preference'] == merged['budget_category']).mean()

# 3. Amenity Alignment
def amenity_match(row):
    u_amenities = row.get('amenity_preferences', '')
    h_amenities = row.get('amenities', '')
    if pd.isna(u_amenities) or pd.isna(h_amenities):
        return 0
    if not isinstance(u_amenities, str) or not isinstance(h_amenities, str):
        return 0
    u_list = [a.strip() for a in u_amenities.split('|')]
    matches = sum(1 for a in u_list if a in h_amenities)
    return matches / len(u_list) if len(u_list) > 0 else 0

merged['amenity_match_ratio'] = merged.apply(amenity_match, axis=1)
amenity_match_rate = (merged['amenity_match_ratio'] > 0).mean()

print(f"Area Alignment Rate: {area_match * 100:.2f}%")
print(f"Budget Alignment Rate: {budget_match * 100:.2f}%")
print(f"Amenity Alignment Rate: {amenity_match_rate * 100:.2f}%")

labels = ['Area Alignment', 'Budget Alignment', 'Amenity Alignment']
rates = [area_match, budget_match, amenity_match_rate]

plt.figure(figsize=(8, 5))
sns.barplot(x=labels, y=rates, palette='viridis')
plt.axhline(0.70, color='r', linestyle='--', label='Area Threshold (70%)')
plt.axhline(0.80, color='b', linestyle='--', label='Budget Threshold (80%)')
plt.axhline(0.60, color='g', linestyle='--', label='Amenity Threshold (60%)')
plt.ylim(0, 1.0)
plt.title('Preference Alignment Rates')
plt.legend()
plt.show()
"""
cells.append(nbf.v4.new_markdown_cell("## 3. Preference Alignment Audit"))
cells.append(nbf.v4.new_code_cell(code_align))

nb.cells = cells

nbf.write(nb, 'D:/Side_Projects/0_Independent_Project/TrustLayer-AI/research/notebooks/10_interaction_quality_audit.ipynb')

# Calculate the actual values here and print to stdout so agent can write the report
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')

df_int = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/interactions_v2.csv'))
df_users = pd.read_csv(os.path.join(DATA_DIR, 'raw/synthetic_users/users.csv'))
df_hotels = pd.read_csv(os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv'))

merged = df_int.merge(df_users, on='user_id', how='left').merge(df_hotels, on='google_place_id', how='left')
area_match = (merged['preferred_area'] == merged['area']).mean()
budget_match = (merged['budget_preference'] == merged['budget_category']).mean()

def amenity_match(row):
    u_amenities = row.get('amenity_preferences', '')
    h_amenities = row.get('amenities', '')
    if pd.isna(u_amenities) or pd.isna(h_amenities):
        return 0
    if not isinstance(u_amenities, str) or not isinstance(h_amenities, str):
        return 0
    u_list = [a.strip() for a in u_amenities.split('|')]
    matches = sum(1 for a in u_list if a in h_amenities)
    return matches / len(u_list) if len(u_list) > 0 else 0

merged['amenity_match_ratio'] = merged.apply(amenity_match, axis=1)
amenity_match_rate = (merged['amenity_match_ratio'] > 0).mean()

print(f"Total Interactions: {len(df_int)}")
print(f"Area Alignment: {area_match*100:.2f}%")
print(f"Budget Alignment: {budget_match*100:.2f}%")
print(f"Amenity Alignment: {amenity_match_rate*100:.2f}%")