import pandas as pd
import numpy as np
import os
import re

SCRIPT_DIR = os.path.dirname(__file__)
REVIEW_FEATURES_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/review_features.csv")
EXPLAINABILITY_FEATURES_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/explainability_features.csv")

# Keyword dictionaries for each explainability aspect
ASPECT_KEYWORDS = {
    'cleanliness': ['clean', 'dirty', 'hygiene', 'spotless', 'filthy', 'stain', 'dust', 'smell', 'washroom', 'bathroom'],
    'service': ['service', 'management', 'reception', 'desk', 'prompt', 'slow', 'wait', 'room service'],
    'location': ['location', 'near', 'distance', 'station', 'airport', 'market', 'far', 'accessible', 'view'],
    'value_for_money': ['value', 'money', 'price', 'cost', 'expensive', 'cheap', 'affordable', 'worth', 'budget'],
    'staff_behavior': ['staff', 'behavior', 'rude', 'polite', 'helpful', 'friendly', 'manager', 'arrogant', 'courteous']
}

def extract_absa():
    if not os.path.exists(REVIEW_FEATURES_PATH):
        raise FileNotFoundError(f"Could not find {REVIEW_FEATURES_PATH}")

    df = pd.read_csv(REVIEW_FEATURES_PATH)
    print(f"Loaded {len(df)} reviews for ABSA processing.")

    # Convert text to lowercase for keyword matching
    df['text_lower'] = df['review_text'].fillna("").str.lower()

    hotel_aspect_scores = []
    grouped = df.groupby('google_place_id')

    print("Extracting Aspect-Based Sentiment features...")
    
    for place_id, group in grouped:
        aspect_data = {'google_place_id': place_id}
        
        for aspect, keywords in ASPECT_KEYWORDS.items():
            # Find reviews explicitly mentioning this aspect
            pattern = '|'.join([rf'\b{kw}\b' for kw in keywords])
            mask = group['text_lower'].str.contains(pattern, regex=True)
            
            relevant_reviews = group[mask]
            
            if len(relevant_reviews) > 0:
                # Average positive probability of reviews mentioning the aspect
                aspect_score = relevant_reviews['positive_probability'].mean()
            else:
                # If no mentions, keep it neutral (NaN allows models to decide how to impute)
                aspect_score = np.nan
                
            aspect_data[f'{aspect}_score'] = aspect_score
            
        hotel_aspect_scores.append(aspect_data)

    df_absa = pd.DataFrame(hotel_aspect_scores)
    
    # Fill NaN with 0.5 (neutral sentiment) for baseline dataset consistency
    df_absa.fillna(0.5, inplace=True)
    
    os.makedirs(os.path.dirname(EXPLAINABILITY_FEATURES_PATH), exist_ok=True)
    df_absa.to_csv(EXPLAINABILITY_FEATURES_PATH, index=False)
    print(f"ABSA complete. Saved {len(df_absa)} hotel explainability feature records to {os.path.abspath(EXPLAINABILITY_FEATURES_PATH)}")

if __name__ == "__main__":
    extract_absa()
