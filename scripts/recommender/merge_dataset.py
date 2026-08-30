import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(__file__)
CLEANED_HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/delhi_hotels_cleaned.csv")
HOTEL_SUMMARY_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/hotel_review_summary.csv")
EXPLAINABILITY_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/explainability_features.csv")
HOTEL_FEATURES_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/hotel_features.csv")

FINAL_DATASET_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")

def merge_final_dataset():
    df_hotels = pd.read_csv(CLEANED_HOTELS_PATH)
    
    if os.path.exists(HOTEL_SUMMARY_PATH):
        df_summary = pd.read_csv(HOTEL_SUMMARY_PATH)
        df_hotels = pd.merge(df_hotels, df_summary, on='google_place_id', how='left')
        
    if os.path.exists(EXPLAINABILITY_PATH):
        df_absa = pd.read_csv(EXPLAINABILITY_PATH)
        df_hotels = pd.merge(df_hotels, df_absa, on='google_place_id', how='left')
        
    if os.path.exists(HOTEL_FEATURES_PATH):
        df_feats = pd.read_csv(HOTEL_FEATURES_PATH)
        # Drop overlapping columns before merge
        cols_to_use = df_feats.columns.difference(df_hotels.columns).tolist() + ['google_place_id']
        df_hotels = pd.merge(df_hotels, df_feats[cols_to_use], on='google_place_id', how='left')
        
    os.makedirs(os.path.dirname(FINAL_DATASET_PATH), exist_ok=True)
    df_hotels.to_csv(FINAL_DATASET_PATH, index=False)
    print(f"Final dataset constructed! Saved {len(df_hotels)} rows with {len(df_hotels.columns)} features to {os.path.abspath(FINAL_DATASET_PATH)}")

if __name__ == "__main__":
    merge_final_dataset()
