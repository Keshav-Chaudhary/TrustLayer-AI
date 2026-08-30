import pandas as pd
import requests
import os
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
if not API_KEY:
    raise ValueError("Please set the GOOGLE_PLACES_API_KEY environment variable.")

SCRIPT_DIR = os.path.dirname(__file__)
HOTELS_FILE = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/delhi_hotels_cleaned.csv")
REVIEWS_OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../../data/raw/reviews/reviews_raw.csv")

def fetch_reviews():
    print(f"Loading hotels from {os.path.abspath(HOTELS_FILE)}")
    df_hotels = pd.read_csv(HOTELS_FILE)
    
    # Prioritize hotels that have reviews according to our metadata
    df_hotels = df_hotels[df_hotels['review_count'] > 0]
    total_hotels = len(df_hotels)
    print(f"Found {total_hotels} hotels with at least 1 review to process.")

    all_reviews = []
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    for i, row in df_hotels.iterrows():
        place_id = row['google_place_id']
        hotel_id = row['hotel_id']
        hotel_name = row['hotel_name']
        
        params = {
            'place_id': place_id,
            'fields': 'reviews',
            'key': API_KEY
        }
        
        if (i+1) % 50 == 0:
            print(f"Processed {i+1}/{total_hotels} hotels. Collected {len(all_reviews)} reviews so far...")
            
        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {hotel_name}: {e}")
            continue
            
        if response.status_code == 200:
            data = response.json()
            reviews = data.get('result', {}).get('reviews', [])
            
            for rev in reviews:
                review_text = rev.get('text', '').strip()
                # Skip completely empty reviews as they are useless for sentiment analysis
                if not review_text:
                    continue 
                    
                review_entry = {
                    'review_id': str(uuid.uuid4()),
                    'hotel_id': hotel_id,
                    'google_place_id': place_id,
                    'hotel_name': hotel_name,
                    'review_text': review_text,
                    'review_rating': rev.get('rating'),
                    'review_date': pd.to_datetime(rev.get('time'), unit='s').isoformat() if rev.get('time') else None,
                    'review_source': 'Google Places API'
                }
                all_reviews.append(review_entry)
        
        # Respect API rate limits
        time.sleep(0.1)

    df_reviews = pd.DataFrame(all_reviews)
    
    os.makedirs(os.path.dirname(REVIEWS_OUTPUT_FILE), exist_ok=True)
    df_reviews.to_csv(REVIEWS_OUTPUT_FILE, index=False)
    
    print(f"\nReview collection complete!")
    print(f"Total reviews collected: {len(df_reviews)}")
    print(f"Unique hotels with reviews: {df_reviews['google_place_id'].nunique()}")
    print(f"Saved to {os.path.abspath(REVIEWS_OUTPUT_FILE)}")

if __name__ == "__main__":
    fetch_reviews()
