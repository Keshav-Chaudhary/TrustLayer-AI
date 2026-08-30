import pandas as pd
import numpy as np
import os
import uuid

SCRIPT_DIR = os.path.dirname(__file__)
USERS_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/users.csv")
HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")

def generate_users():
    num_users = 500
    
    # We load hotels to get realistic area options
    df_hotels = pd.read_csv(HOTELS_PATH)
    valid_areas = df_hotels['area_cluster'].unique()
    valid_areas = [a for a in valid_areas if str(a) != 'nan']
    
    users = []
    
    # Define realistic distributions
    budgets = ['Budget', 'Mid-Range', 'Luxury']
    budget_probs = [0.4, 0.45, 0.15]
    
    purposes = ['Business', 'Leisure', 'Family', 'Solo', 'Couple']
    purpose_probs = [0.25, 0.3, 0.2, 0.1, 0.15]
    
    amenity_options = ['WiFi', 'Pool', 'Breakfast', 'Parking', 'Gym', 'Spa']
    
    for _ in range(num_users):
        budget = np.random.choice(budgets, p=budget_probs)
        purpose = np.random.choice(purposes, p=purpose_probs)
        area = np.random.choice(valid_areas)
        
        # Select 2 to 4 random amenities
        num_amenities = np.random.randint(2, 5)
        amenities = np.random.choice(amenity_options, size=num_amenities, replace=False)
        
        users.append({
            'user_id': str(uuid.uuid4()),
            'budget_preference': budget,
            'preferred_area': area,
            'travel_purpose': purpose,
            'amenity_preferences': "|".join(amenities)
        })
        
    df_users = pd.DataFrame(users)
    
    os.makedirs(os.path.dirname(USERS_OUTPUT_PATH), exist_ok=True)
    df_users.to_csv(USERS_OUTPUT_PATH, index=False)
    print(f"Generated {len(df_users)} synthetic users. Saved to {os.path.abspath(USERS_OUTPUT_PATH)}")

if __name__ == "__main__":
    generate_users()
