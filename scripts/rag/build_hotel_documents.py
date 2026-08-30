import pandas as pd
import json
import os
import re
from collections import Counter
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
HOTELS_PATH = os.path.join(DATA_DIR, 'exports/final_hotel_dataset.csv')
REVIEWS_PATH = os.path.join(DATA_DIR, 'raw/reviews/reviews_raw.csv')
RAG_DIR = os.path.join(DATA_DIR, 'rag')

def extract_themes(texts):
    pos_themes = Counter()
    neg_themes = Counter()
    
    pos_keywords = {
        'clean_rooms': ['clean', 'spotless', 'neat', 'tidy'],
        'friendly_staff': ['friendly', 'helpful', 'polite', 'welcoming', 'staff'],
        'good_location': ['location', 'near', 'close to', 'convenient'],
        'great_value': ['value', 'cheap', 'affordable', 'worth'],
        'good_food': ['food', 'breakfast', 'tasty', 'delicious']
    }
    
    neg_keywords = {
        'dirty_rooms': ['dirty', 'unclean', 'smell', 'filthy', 'stains'],
        'rude_staff': ['rude', 'unprofessional', 'unhelpful', 'bad service'],
        'noise': ['noisy', 'loud', 'noise'],
        'bad_food': ['bad food', 'tasteless', 'stale'],
        'parking_issues': ['parking', 'no parking']
    }
    
    for text in texts:
        if not isinstance(text, str): continue
        text_lower = text.lower()
        
        # Check positive
        for theme, words in pos_keywords.items():
            if any(w in text_lower for w in words):
                pos_themes[theme] += 1
                
        # Check negative
        for theme, words in neg_keywords.items():
            if any(w in text_lower for w in words):
                neg_themes[theme] += 1
                
    return dict(pos_themes), dict(neg_themes)

def get_travel_purpose_tags(row):
    tags = []
    if row['location_score'] >= 0.7:
        tags.append("Leisure")
    if row['service_score'] >= 0.7 and row['staff_behavior_score'] >= 0.7:
        tags.append("Business")
    if row['cleanliness_score'] >= 0.7 and row['value_for_money_score'] >= 0.6:
        tags.append("Family")
    if not tags:
        tags.append("Budget")
    return tags

def main():
    os.makedirs(RAG_DIR, exist_ok=True)
    
    print("Loading data...")
    df_hotels = pd.read_csv(HOTELS_PATH)
    try:
        df_reviews = pd.read_csv(REVIEWS_PATH)
    except FileNotFoundError:
        df_reviews = pd.DataFrame(columns=['google_place_id', 'review_text', 'review_rating'])
        
    print(f"Loaded {len(df_hotels)} hotels and {len(df_reviews)} reviews.")
    
    # Pre-group reviews by hotel
    reviews_by_hotel = df_reviews.groupby('google_place_id')
    
    docs_created = 0
    
    for _, hotel in tqdm(df_hotels.iterrows(), total=len(df_hotels)):
        hid = hotel['google_place_id']
        
        hotel_reviews = []
        if hid in reviews_by_hotel.groups:
            hotel_reviews = reviews_by_hotel.get_group(hid)
            
        # Separate positive and negative reviews based on rating or simple heuristics
        pos_reviews = []
        neg_reviews = []
        
        if len(hotel_reviews) > 0:
            if 'review_rating' in hotel_reviews.columns:
                pos_reviews = hotel_reviews[hotel_reviews['review_rating'] >= 4]['review_text'].dropna().tolist()
                neg_reviews = hotel_reviews[hotel_reviews['review_rating'] <= 3]['review_text'].dropna().tolist()
            else:
                pos_reviews = hotel_reviews['review_text'].dropna().tolist()
                
        pos_themes, neg_themes = extract_themes(pos_reviews + neg_reviews)
        
        pos_snips_cnt = len(pos_reviews[:3])
        neg_snips_cnt = len(neg_reviews[:3])
        tot_themes = len(pos_themes) + len(neg_themes)
        
        if pos_snips_cnt >= 3 and neg_snips_cnt >= 2 and tot_themes >= 3:
            evidence_level = "rich"
        elif (pos_snips_cnt + neg_snips_cnt) >= 2 and tot_themes >= 2:
            evidence_level = "moderate"
        elif (pos_snips_cnt + neg_snips_cnt) == 0 and tot_themes == 0:
            evidence_level = "none"
        else:
            evidence_level = "sparse"

        doc = {
            "hotel_id": hid,
            "hotel_name": hotel['hotel_name'],
            "area": hotel['area'],
            "budget_category": hotel.get('budget_category', 'Unknown'),
            "rating": hotel.get('rating', 0.0),
            "trust_score": hotel.get('trust_score', 0.0),
            "travel_purpose_tags": get_travel_purpose_tags(hotel),
            
            "evidence_metadata": {
                "evidence_level": evidence_level,
                "review_count": len(hotel_reviews),
                "positive_snippet_count": pos_snips_cnt,
                "negative_snippet_count": neg_snips_cnt,
                "positive_theme_count": len(pos_themes),
                "negative_theme_count": len(neg_themes)
            },
            
            "aspect_scores": {
                "cleanliness": hotel.get('cleanliness_score', 0.5),
                "service": hotel.get('service_score', 0.5),
                "location": hotel.get('location_score', 0.5),
                "value_for_money": hotel.get('value_for_money_score', 0.5),
                "staff_behavior": hotel.get('staff_behavior_score', 0.5)
            },
            
            "recommendation_features": {
                "popularity_score": hotel.get('popularity_score', 0.0),
                "rating_score": hotel.get('rating_score', 0.0),
                "sentiment_score": hotel.get('sentiment_score', 0.0)
            },
            
            "review_evidence": {
                "positive_snippets": pos_reviews[:3],
                "negative_snippets": neg_reviews[:3]
            },
            
            "review_summary": f"Based on {len(hotel_reviews)} reviews.",
            "positive_themes": pos_themes,
            "negative_themes": neg_themes
        }
        
        out_path = os.path.join(RAG_DIR, f"{hid}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(doc, f, indent=2)
            
        docs_created += 1
        
    print(f"Successfully generated {docs_created} hotel knowledge documents in {RAG_DIR}")

if __name__ == "__main__":
    main()
