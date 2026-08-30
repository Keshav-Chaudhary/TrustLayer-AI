import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(__file__)
USERS_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/users.csv")
HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")
INTERACTIONS_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/interactions.csv")

def generate_interactions():
    if not os.path.exists(USERS_PATH) or not os.path.exists(HOTELS_PATH):
        raise FileNotFoundError("Users or Hotels dataset not found.")

    df_users = pd.read_csv(USERS_PATH)
    df_hotels = pd.read_csv(HOTELS_PATH)
    
    num_interactions = 5000
    interactions = []
    
    # Interaction funnel probabilities
    # View (60%), Click (25%), Booking (10%), Rating (5%)
    interaction_types = ['view', 'click', 'booking', 'rating']
    interaction_probs = [0.60, 0.25, 0.10, 0.05]
    
    user_ids = df_users['user_id'].tolist()
    
    # Weight hotels by popularity so interactions are realistic (popular hotels get more views)
    # Using trust_score or popularity_score for weights
    # We ensure no negative weights and handle NaNs
    weights = df_hotels['popularity_score'].fillna(0.1) + 0.1
    weights = weights / weights.sum()
    hotel_ids = df_hotels['google_place_id'].tolist()
    
    start_date = datetime.now() - timedelta(days=180)
    
    for _ in range(num_interactions):
        user = np.random.choice(user_ids)
        hotel = np.random.choice(hotel_ids, p=weights)
        itype = np.random.choice(interaction_types, p=interaction_probs)
        
        # Random timestamp within last 6 months
        random_days = np.random.randint(0, 180)
        random_hours = np.random.randint(0, 24)
        ts = start_date + timedelta(days=random_days, hours=random_hours)
        
        interactions.append({
            'interaction_id': str(uuid.uuid4()),
            'user_id': user,
            'google_place_id': hotel,
            'interaction_type': itype,
            'timestamp': ts.isoformat()
        })
        
    df_interactions = pd.DataFrame(interactions)
    
    # Sort by timestamp
    df_interactions = df_interactions.sort_values('timestamp')
    
    os.makedirs(os.path.dirname(INTERACTIONS_OUTPUT_PATH), exist_ok=True)
    df_interactions.to_csv(INTERACTIONS_OUTPUT_PATH, index=False)
    print(f"Generated {len(df_interactions)} synthetic interactions. Saved to {os.path.abspath(INTERACTIONS_OUTPUT_PATH)}")

if __name__ == "__main__":
    generate_interactions()
