import pandas as pd
import numpy as np
import os

# Paths relative to script location
SCRIPT_DIR = os.path.dirname(__file__)
RAW_DATA_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/google_places/delhi_hotels_raw.csv")
CLEANED_DATA_PATH = os.path.join(SCRIPT_DIR, "../../data/processed/cleaned/delhi_hotels_cleaned.csv")

def clean_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Could not find {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    initial_count = len(df)
    print(f"Loaded {initial_count} raw records.")

    # 1. Deduplicate
    df = df.drop_duplicates(subset=['google_place_id'])
    print(f"After deduplication by google_place_id: {len(df)} unique records.")

    # 2. Remove incomplete entries (missing name, lat, or lng)
    df = df.dropna(subset=['hotel_name', 'latitude', 'longitude'])
    print(f"After dropping missing names/coordinates: {len(df)} records.")

    # 3. Validate coordinates (Rough bounding box for Delhi NCR)
    lat_valid = df['latitude'].between(28.0, 29.0)
    lng_valid = df['longitude'].between(76.5, 77.5)
    df = df[lat_valid & lng_valid]
    print(f"After coordinate bounding box validation: {len(df)} records.")

    # 4. Normalize strings
    df['hotel_name'] = df['hotel_name'].astype(str).str.strip().str.title()
    df['address'] = df['address'].astype(str).str.strip()

    # 5. Extract Area (naive extraction, taking the second to last part of address before City/State)
    def extract_area(address):
        parts = [p.strip() for p in address.split(',')]
        if len(parts) >= 2:
            return parts[-2]
        return None
    
    df['area'] = df['address'].apply(extract_area)

    # 6. Analyze Missing Values (especially price_level)
    print("\n--- Missing Value Report ---")
    missing_report = df.isna().sum()
    print(missing_report[missing_report > 0])
    print("----------------------------\n")

    # Save
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Cleaned dataset saved to {os.path.abspath(CLEANED_DATA_PATH)}")

if __name__ == "__main__":
    clean_data()
