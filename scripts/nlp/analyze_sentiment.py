import pandas as pd
import numpy as np
import os
from transformers import pipeline
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(__file__)
CLEANED_REVIEWS_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/reviews_cleaned.csv")
FEATURES_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/features/review_features.csv")

def run_sentiment_analysis():
    if not os.path.exists(CLEANED_REVIEWS_PATH):
        raise FileNotFoundError(f"Could not find {CLEANED_REVIEWS_PATH}")

    df = pd.read_csv(CLEANED_REVIEWS_PATH)
    print(f"Loaded {len(df)} cleaned reviews for sentiment analysis.")

    if os.path.exists(FEATURES_OUTPUT_PATH):
        try:
            df_existing = pd.read_csv(FEATURES_OUTPUT_PATH)
            if len(df_existing) == len(df):
                print(f"Sentiment features already computed and verified ({len(df_existing)} records). Skipping inference.")
                return
        except Exception:
            pass
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", top_k=None)

    print("Running inference...")
    
    positive_probs = []
    negative_probs = []
    sentiment_labels = []

    # Process each review with a progress bar
    for text in tqdm(df['review_text'].fillna(""), desc="Analyzing sentiment"):
        try:
            # DistilBERT max length is 512 tokens. We truncate long reviews (approx 400 words) to avoid errors.
            truncated_text = " ".join(str(text).split()[:400])
            
            result = sentiment_pipeline(truncated_text)[0]
            
            # Extract scores
            pos_score = next(item['score'] for item in result if item['label'] == 'POSITIVE')
            neg_score = next(item['score'] for item in result if item['label'] == 'NEGATIVE')
            
            positive_probs.append(pos_score)
            negative_probs.append(neg_score)
            sentiment_labels.append("POSITIVE" if pos_score > neg_score else "NEGATIVE")
        except Exception as e:
            # Fallback for completely unprocessable text
            positive_probs.append(0.5)
            negative_probs.append(0.5)
            sentiment_labels.append("NEUTRAL")

    df['positive_probability'] = positive_probs
    df['negative_probability'] = negative_probs
    df['sentiment_label'] = sentiment_labels

    os.makedirs(os.path.dirname(FEATURES_OUTPUT_PATH), exist_ok=True)
    df.to_csv(FEATURES_OUTPUT_PATH, index=False)
    print(f"\nSentiment analysis complete. Features saved to {os.path.abspath(FEATURES_OUTPUT_PATH)}")

if __name__ == "__main__":
    run_sentiment_analysis()
