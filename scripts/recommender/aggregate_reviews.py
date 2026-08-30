import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(__file__)
REVIEW_FEATURES_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/review_features.csv")
HOTEL_SUMMARY_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/hotel_review_summary.csv")

def aggregate_reviews():
    if not os.path.exists(REVIEW_FEATURES_PATH):
        raise FileNotFoundError(f"Could not find {REVIEW_FEATURES_PATH}")

    df = pd.read_csv(REVIEW_FEATURES_PATH)
    print(f"Loaded {len(df)} review features for aggregation.")

    # Group by hotel
    grouped = df.groupby('google_place_id')

    summary_data = []

    for place_id, group in grouped:
        review_volume = len(group)
        average_sentiment = group['positive_probability'].mean()
        
        positive_count = (group['sentiment_label'] == 'POSITIVE').sum()
        negative_count = (group['sentiment_label'] == 'NEGATIVE').sum()
        
        positive_review_ratio = positive_count / review_volume
        negative_review_ratio = negative_count / review_volume

        summary_data.append({
            'google_place_id': place_id,
            'review_volume': review_volume,
            'average_sentiment': average_sentiment,
            'positive_review_ratio': positive_review_ratio,
            'negative_review_ratio': negative_review_ratio
        })

    df_summary = pd.DataFrame(summary_data)
    
    os.makedirs(os.path.dirname(HOTEL_SUMMARY_PATH), exist_ok=True)
    df_summary.to_csv(HOTEL_SUMMARY_PATH, index=False)
    print(f"Aggregation complete. Saved {len(df_summary)} hotel summaries to {os.path.abspath(HOTEL_SUMMARY_PATH)}")

if __name__ == "__main__":
    aggregate_reviews()
