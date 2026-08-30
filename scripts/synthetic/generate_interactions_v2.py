import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime, timedelta
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(__file__)
USERS_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/users.csv")
HOTELS_PATH = os.path.join(SCRIPT_DIR, "../../data/exports/final_hotel_dataset.csv")
INTERACTIONS_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "../../data/raw/synthetic_users/interactions_v2.csv")

def generate_interactions_v2():
    print("Loading datasets...")
    df_users = pd.read_csv(USERS_PATH)
    df_hotels = pd.read_csv(HOTELS_PATH)
    
    # Interaction funnel probabilities
    interaction_types = ['view', 'click', 'booking', 'rating']
    interaction_probs = [0.60, 0.25, 0.10, 0.05]
    
    users = df_users.to_dict('records')
    hotels = df_hotels.to_dict('records')
    
    interactions = []
    start_date = datetime.now() - timedelta(days=180)
    
    # Assign interaction counts per user based on defined distribution
    print("Assigning user activity distribution...")
    n_users = len(users)
    
    n_tier1 = int(0.40 * n_users)  # 5-15
    n_tier2 = int(0.35 * n_users)  # 15-30
    n_tier3 = int(0.20 * n_users)  # 30-75
    n_tier4 = n_users - n_tier1 - n_tier2 - n_tier3  # 75-150
    
    counts = []
    counts.extend(np.random.randint(5, 16, size=n_tier1))
    counts.extend(np.random.randint(15, 31, size=n_tier2))
    counts.extend(np.random.randint(30, 76, size=n_tier3))
    counts.extend(np.random.randint(75, 151, size=n_tier4))
    
    np.random.shuffle(counts)
    
    # Pre-process hotel base scores
    hotel_ids = np.array([h['google_place_id'] for h in hotels])
    base_scores = np.array([(h.get('popularity_score', 0.5) + 0.1) * (h.get('trust_score', 0.5) + 0.1) for h in hotels])
    
    print("Generating interactions per user...")
    for i, user in enumerate(tqdm(users)):
        u_area = user.get('preferred_area')
        u_budget = user.get('budget_preference')
        u_amenities = user.get('amenity_preferences', '')
        u_amenities_list = [a.strip() for a in u_amenities.split('|')] if isinstance(u_amenities, str) and u_amenities else []
        
        # Calculate hotel scores for this user
        u_scores = base_scores.copy()
        
        for j, h in enumerate(hotels):
            # Area Alignment Target >= 70%
            if h.get('area') == u_area:
                u_scores[j] *= 1000.0
                
            # Budget Alignment Target >= 80%
            if h.get('budget_category') == u_budget:
                u_scores[j] *= 500.0
                
            # Amenity Alignment Target >= 60%
            h_amenities = str(h.get('amenities', ''))
            match_count = sum(1 for a in u_amenities_list if a in h_amenities)
            if match_count > 0:
                u_scores[j] *= (10.0 * match_count)
                
        # Normalize to probabilities
        probs = u_scores / u_scores.sum()
        
        # Introduce epsilon-greedy noise (15% purely random)
        noise_probs = base_scores / base_scores.sum()
        final_probs = 0.85 * probs + 0.15 * noise_probs
        final_probs = final_probs / final_probs.sum()
        
        # Sample interactions
        num_ints = counts[i]
        sampled_hotels = np.random.choice(hotel_ids, size=num_ints, p=final_probs, replace=True)
        
        for hid in sampled_hotels:
            itype = np.random.choice(interaction_types, p=interaction_probs)
            
            random_days = np.random.randint(0, 180)
            random_hours = np.random.randint(0, 24)
            ts = start_date + timedelta(days=random_days, hours=random_hours)
            
            interactions.append({
                'interaction_id': str(uuid.uuid4()),
                'user_id': user['user_id'],
                'google_place_id': hid,
                'interaction_type': itype,
                'timestamp': ts.isoformat()
            })
            
    df_interactions = pd.DataFrame(interactions)
    df_interactions = df_interactions.sort_values('timestamp')
    
    os.makedirs(os.path.dirname(INTERACTIONS_OUTPUT_PATH), exist_ok=True)
    df_interactions.to_csv(INTERACTIONS_OUTPUT_PATH, index=False)
    print(f"\\nGenerated {len(df_interactions)} high-signal interactions.")
    print(f"Saved to {os.path.abspath(INTERACTIONS_OUTPUT_PATH)}")

if __name__ == "__main__":
    generate_interactions_v2()
