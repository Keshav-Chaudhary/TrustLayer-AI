import os
import time
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
if not API_KEY:
    raise ValueError("Please set the GOOGLE_PLACES_API_KEY environment variable.")
# Delhi NCR rough bounding box
# North: 28.88, South: 28.40, West: 76.84, East: 77.34
LAT_MIN, LAT_MAX = 28.40, 28.88
LNG_MIN, LNG_MAX = 76.84, 77.34

# Grid step (approx 0.05 degrees ~ 5.5 km, search radius 5000m)
GRID_STEP = 0.05
SEARCH_RADIUS = 5000

# Script is located in scripts/collection, so we navigate up two levels
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "google_places", "delhi_hotels_raw.csv")

def generate_grid():
    lats = np.arange(LAT_MIN, LAT_MAX, GRID_STEP)
    lngs = np.arange(LNG_MIN, LNG_MAX, GRID_STEP)
    grid = []
    for lat in lats:
        for lng in lngs:
            grid.append((lat, lng))
    return grid

def fetch_hotels_for_location(lat, lng):
    hotels = []
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        'location': f"{lat},{lng}",
        'radius': SEARCH_RADIUS,
        'type': 'lodging',
        'keyword': 'hotel',
        'key': API_KEY
    }
    
    while True:
        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
            
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
            
        data = response.json()
        if data.get('status') != 'OK' and data.get('status') != 'ZERO_RESULTS':
            print(f"API returned status: {data.get('status')}")
            break
            
        for place in data.get('results', []):
            hotel = {
                'hotel_id': place.get('place_id'), # Temporary placeholder for hotel_id (to be UUID mapped later if needed)
                'google_place_id': place.get('place_id'),
                'hotel_name': place.get('name'),
                'address': place.get('vicinity'),
                'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                'rating': place.get('rating'),
                'review_count': place.get('user_ratings_total'),
                'area': None, # To be determined via reverse geocoding or clustering later
                'hotel_type': 'hotel', # Default baseline
                'price_level': place.get('price_level')
            }
            hotels.append(hotel)
            
        next_page_token = data.get('next_page_token')
        if next_page_token:
            # Google API requires a short delay before using the next page token
            time.sleep(2)
            params = {
                'pagetoken': next_page_token,
                'key': API_KEY
            }
        else:
            break
            
    return hotels

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch hotels from Google Places API.")
    parser.add_argument("--max-points", type=int, help="Maximum number of grid points to process (for testing/quota limits).")
    args = parser.parse_args()

    print("Starting grid-based hotel collection for Delhi NCR...")
    grid = generate_grid()
    print(f"Generated {len(grid)} grid points.")
    
    all_hotels = []
    seen_place_ids = set()
    
    for i, (lat, lng) in enumerate(grid):
        if args.max_points and i >= args.max_points:
            print(f"Reached max points limit ({args.max_points}). Stopping early.")
            break
            
        print(f"Searching grid point {i+1}/{len(grid)} at {lat:.4f}, {lng:.4f}...")
        point_hotels = fetch_hotels_for_location(lat, lng)
        
        # Deduplicate on the fly
        for h in point_hotels:
            if h['google_place_id'] not in seen_place_ids:
                seen_place_ids.add(h['google_place_id'])
                all_hotels.append(h)
                
        print(f"  -> Found {len(point_hotels)} hotels at this point. Total unique so far: {len(all_hotels)}")
        time.sleep(0.5) # Rate limiting
        
    df = pd.DataFrame(all_hotels)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Collection complete! Saved {len(df)} unique hotels to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
