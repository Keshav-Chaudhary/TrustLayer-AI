import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler

SCRIPT_DIR = os.path.dirname(__file__)
CLEANED_HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/delhi_hotels_cleaned.csv")
HOTEL_SUMMARY_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/hotel_review_summary.csv")
HOTEL_FEATURES_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/hotel_features.csv")

def engineer_features():
    df_hotels = pd.read_csv(CLEANED_HOTELS_PATH)
    
    if os.path.exists(HOTEL_SUMMARY_PATH):
        df_summary = pd.read_csv(HOTEL_SUMMARY_PATH)
        # Merge left so hotels without reviews still get baseline features
        df = pd.merge(df_hotels, df_summary, on='google_place_id', how='left')
    else:
        df = df_hotels.copy()

    # Handle NaNs from the merge
    df['review_volume'] = df['review_volume'].fillna(0)
    df['average_sentiment'] = df['average_sentiment'].fillna(0.5)
    
    scaler = MinMaxScaler()

    # 1. Popularity Score
    # Driven by log of review_count to handle heavy-tailed distributions
    df['log_review_count'] = np.log1p(df['review_count'].fillna(0))
    df['popularity_score'] = scaler.fit_transform(df[['log_review_count']])

    # 2. Rating Score
    # Baseline the missing ratings to the mean
    df['rating_score'] = df['rating'].fillna(df['rating'].mean())

    # 3. Sentiment Score
    df['sentiment_score'] = df['average_sentiment']

    # 4. Trust Score
    # A robust recommender system metric combining normalized rating, sentiment, and popularity volume.
    # Hotels with 4.5 rating but 1 review are less trusted than 4.2 rating with 5000 reviews.
    norm_rating = scaler.fit_transform(df[['rating_score']])
    trust_raw = (0.5 * norm_rating.flatten()) + (0.3 * df['sentiment_score']) + (0.2 * df['popularity_score'])
    df['trust_score'] = scaler.fit_transform(trust_raw.values.reshape(-1, 1)).flatten()

    # 5. Budget Category
    # Because price_level was missing from Google Places, we apply a heuristic on the hotel name
    def assign_budget(name):
        name = str(name).lower()
        if any(w in name for w in ['oyo', 'hostel', 'budget', 'inn', 'stay', 'pg']):
            return 'Budget'
        elif any(w in name for w in ['taj', 'oberoi', 'itc', 'leela', 'jw marriott', 'hyatt', 'radisson', 'resort', 'luxury', 'palace']):
            return 'Luxury'
        else:
            return 'Mid-Range'
            
    df['budget_category'] = df['hotel_name'].apply(assign_budget)

    # 6. Area Cluster
    # Group uncommon areas into 'Other' to limit feature sparsity
    top_areas = df['area'].value_counts().nlargest(20).index
    df['area_cluster'] = df['area'].apply(lambda x: x if x in top_areas else 'Other')

    # Keep only the requested output features plus identifiers
    final_cols = ['google_place_id', 'hotel_id', 'trust_score', 'popularity_score', 
                  'rating_score', 'sentiment_score', 'budget_category', 'area_cluster']
    
    df_features = df[final_cols]
    
    os.makedirs(os.path.dirname(HOTEL_FEATURES_PATH), exist_ok=True)
    df_features.to_csv(HOTEL_FEATURES_PATH, index=False)
    print(f"Feature engineering complete. Saved {len(df_features)} records to {os.path.abspath(HOTEL_FEATURES_PATH)}")

if __name__ == "__main__":
    engineer_features()
