import pandas as pd
import numpy as np
import os
import re

SCRIPT_DIR = os.path.dirname(__file__)
RAW_REVIEWS_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/reviews/reviews_raw.csv")
CLEANED_REVIEWS_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/reviews_cleaned.csv")

def clean_text(text):
    if pd.isna(text):
        return ""
    # Remove newlines and extra whitespace
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()

def clean_reviews():
    if not os.path.exists(RAW_REVIEWS_PATH):
        raise FileNotFoundError(f"Could not find {RAW_REVIEWS_PATH}")

    df = pd.read_csv(RAW_REVIEWS_PATH)
    initial_count = len(df)
    print(f"Loaded {initial_count} raw reviews.")

    # 1. Remove empty or too short reviews (less than 10 characters)
    # We want meaningful text for Sentiment Analysis and RAG.
    df['review_text'] = df['review_text'].apply(clean_text)
    df = df[df['review_text'].str.len() > 10]
    print(f"After dropping empty/short reviews (<10 chars): {len(df)} records.")

    # 2. Remove duplicates
    # A duplicate could happen if the same review is fetched twice for the same hotel
    df = df.drop_duplicates(subset=['google_place_id', 'review_text', 'review_rating'])
    print(f"After deduplication: {len(df)} records.")

    # 3. Standardize ratings
    df['review_rating'] = pd.to_numeric(df['review_rating'], errors='coerce')
    df = df.dropna(subset=['review_rating'])
    df['review_rating'] = df['review_rating'].astype(float)
    df = df[df['review_rating'].between(1.0, 5.0)]
    print(f"After validating rating formats (1.0 to 5.0): {len(df)} records.")

    # 4. Standardize dates
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')

    # Save
    os.makedirs(os.path.dirname(CLEANED_REVIEWS_PATH), exist_ok=True)
    df.to_csv(CLEANED_REVIEWS_PATH, index=False)
    
    print(f"\n--- Cleaning Complete ---")
    print(f"Final usable review count: {len(df)}")
    print(f"Total unique hotels covered: {df['google_place_id'].nunique()}")
    print(f"Cleaned reviews saved to {os.path.abspath(CLEANED_REVIEWS_PATH)}")

if __name__ == "__main__":
    clean_reviews()
