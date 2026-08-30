import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(__file__)
HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")
REVIEWS_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/reviews_cleaned.csv")
USERS_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/users.csv")
INTERACTIONS_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/interactions.csv")

STATS_MD_PATH = os.path.join(SCRIPT_DIR, "../../research/reports/dataset_statistics.md")
QUALITY_MD_PATH = os.path.join(SCRIPT_DIR, "../../research/reports/data_quality_report.md")

def generate_validation_reports():
    df_h = pd.read_csv(HOTELS_PATH)
    df_r = pd.read_csv(REVIEWS_PATH)
    df_u = pd.read_csv(USERS_PATH)
    df_i = pd.read_csv(INTERACTIONS_PATH)

    os.makedirs(os.path.dirname(STATS_MD_PATH), exist_ok=True)
    
    # 1. Dataset Statistics
    with open(STATS_MD_PATH, 'w') as f:
        f.write("# Dataset Statistics\n\n")
        f.write(f"- **Total Unique Hotels**: {len(df_h)}\n")
        f.write(f"- **Total Cleaned Reviews**: {len(df_r)}\n")
        f.write(f"- **Total Synthetic Users**: {len(df_u)}\n")
        f.write(f"- **Total Synthetic Interactions**: {len(df_i)}\n")
        
    # 2. Data Quality Report
    with open(QUALITY_MD_PATH, 'w') as f:
        f.write("# Data Quality Report\n\n")
        
        f.write("## 1. Missing Values Analysis (Hotels)\n")
        missing = df_h.isna().sum()
        for col, val in missing.items():
            if val > 0:
                f.write(f"- `{col}`: {val} missing ({(val/len(df_h))*100:.2f}%)\n")
                
        f.write("\n## 2. Duplicate Analysis\n")
        dup_h = df_h.duplicated(subset=['google_place_id']).sum()
        dup_r = df_r.duplicated(subset=['review_id']).sum()
        f.write(f"- Hotel Duplicates: {dup_h}\n")
        f.write(f"- Review Duplicates: {dup_r}\n")
        
    print(f"Validation reports generated in {os.path.abspath(os.path.dirname(STATS_MD_PATH))}")

if __name__ == "__main__":
    generate_validation_reports()
