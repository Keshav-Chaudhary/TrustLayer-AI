import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class ContentBasedRecommender:
    def __init__(self, hotels_df, beta=0.5):
        """
        beta: weight given to explicit user profile vs implicit interaction profile.
              1.0 means pure explicit profile, 0.0 means pure implicit profile.
        """
        self.hotels_df = hotels_df.copy()
        self.beta = beta
        
        # 1. Impute missing aspect scores
        aspects = ['cleanliness_score', 'service_score', 'location_score', 'value_for_money_score', 'staff_behavior_score']
        for col in aspects:
            # Impute with area cluster average first, then overall median if still null
            self.hotels_df[col] = self.hotels_df.groupby('area_cluster')[col].transform(lambda x: x.fillna(x.mean()))
            overall_median = self.hotels_df[col].median()
            self.hotels_df[col] = self.hotels_df[col].fillna(overall_median if not pd.isna(overall_median) else 0.5)
            
        # Also impute other scores
        other_scores = ['trust_score', 'popularity_score', 'rating_score', 'sentiment_score']
        for col in other_scores:
            overall_median = self.hotels_df[col].median()
            self.hotels_df[col] = self.hotels_df[col].fillna(overall_median if not pd.isna(overall_median) else 0.5)
            
        # 2. Build hotel feature vectors
        # Continuous features
        continuous_features = aspects + other_scores
        scaler = MinMaxScaler()
        self.hotels_df[continuous_features] = scaler.fit_transform(self.hotels_df[continuous_features])
        
        # Categorical features one-hot encoding
        # We manually encode area and budget_category to have full control over the feature space mapping
        self.unique_areas = sorted(list(self.hotels_df['area'].dropna().unique()))
        self.unique_budgets = sorted(list(self.hotels_df['budget_category'].dropna().unique()))
        
        # Map hotel IDs to features
        self.hotel_features = {}
        for idx, row in self.hotels_df.iterrows():
            features = []
            # Add continuous scores
            features.extend([row[col] for col in continuous_features])
            
            # One-hot area
            area_vec = [1.0 if row['area'] == area else 0.0 for area in self.unique_areas]
            features.extend(area_vec)
            
            # One-hot budget
            budget_vec = [1.0 if row['budget_category'] == b else 0.0 for b in self.unique_budgets]
            features.extend(budget_vec)
            
            self.hotel_features[row['google_place_id']] = np.array(features)
            
        self.feature_dim = len(next(iter(self.hotel_features.values())))
        
    def _build_explicit_user_vector(self, user_row):
        """
        Builds a D-dimensional user preference vector based only on explicit demographic profile.
        """
        # Feature order matches the hotel vectors:
        # aspects (5), other_scores (4), areas (len(unique_areas)), budgets (len(unique_budgets))
        vec = np.zeros(self.feature_dim)
        
        # 1. Travel purpose mapping to aspect weights
        purpose = user_row.get('travel_purpose', 'Leisure')
        aspect_weights = {
            'cleanliness_score': 0.5,
            'service_score': 0.5,
            'location_score': 0.5,
            'value_for_money_score': 0.5,
            'staff_behavior_score': 0.5
        }
        if purpose == 'Business':
            aspect_weights['service_score'] = 1.0
            aspect_weights['staff_behavior_score'] = 1.0
            aspect_weights['location_score'] = 0.6
        elif purpose == 'Family':
            aspect_weights['cleanliness_score'] = 1.0
            aspect_weights['location_score'] = 0.8
            aspect_weights['value_for_money_score'] = 0.7
        else: # Leisure or other
            aspect_weights['location_score'] = 1.0
            aspect_weights['value_for_money_score'] = 0.8
            aspect_weights['service_score'] = 0.6
            
        # 2. Amenities mapping to adjust aspect weights
        amenities = user_row.get('amenity_preferences', '')
        if isinstance(amenities, str) and amenities:
            amenity_list = [a.strip() for a in amenities.split('|')]
            for a in amenity_list:
                if a in ['Pool', 'Spa', 'Gym']:
                    aspect_weights['service_score'] = min(1.0, aspect_weights['service_score'] + 0.1)
                elif a in ['Breakfast', 'WiFi', 'Parking']:
                    aspect_weights['value_for_money_score'] = min(1.0, aspect_weights['value_for_money_score'] + 0.1)
                    
        # Put aspects into vector
        aspects_list = ['cleanliness_score', 'service_score', 'location_score', 'value_for_money_score', 'staff_behavior_score']
        for i, col in enumerate(aspects_list):
            vec[i] = aspect_weights[col]
            
        # Put other scores (trust, popularity, rating, sentiment) to a moderate weight
        # e.g., trust_score, popularity_score, rating_score, sentiment_score set to 0.7 to prefer higher quality
        vec[5:9] = 0.7
        
        # 3. Area preference (one-hot)
        pref_area = user_row.get('preferred_area', '')
        area_offset = 9
        for i, area in enumerate(self.unique_areas):
            if area == pref_area:
                vec[area_offset + i] = 1.5 # Extra weight for preferred area
                
        # 4. Budget preference (one-hot)
        pref_budget = user_row.get('budget_preference', '')
        budget_offset = area_offset + len(self.unique_areas)
        for i, budget in enumerate(self.unique_budgets):
            if budget == pref_budget:
                vec[budget_offset + i] = 1.5 # Extra weight for preferred budget
                
        return vec
        
    def _get_user_vector(self, user_row, train_interactions=None):
        u_exp = self._build_explicit_user_vector(user_row)
        user_id = user_row['user_id']
        u_imp = np.zeros(self.feature_dim)
        has_interactions = False
        
        if train_interactions is not None and len(train_interactions) > 0:
            user_ints = train_interactions[train_interactions['user_id'] == user_id]
            if len(user_ints) > 0:
                interacted_hids = user_ints['google_place_id'].tolist()
                valid_feat_vectors = [self.hotel_features[hid] for hid in interacted_hids if hid in self.hotel_features]
                if len(valid_feat_vectors) > 0:
                    u_imp = np.mean(valid_feat_vectors, axis=0)
                    has_interactions = True
                    
        if has_interactions:
            u_vec = self.beta * u_exp + (1 - self.beta) * u_imp
        else:
            u_vec = u_exp
        return u_vec

    def recommend(self, user_row, train_interactions=None, top_n=10, exclude_ids=None):
        """
        user_row: dict or Series containing user metadata (user_id, travel_purpose, preferred_area, budget_preference, amenity_preferences)
        train_interactions: DataFrame containing training interactions for this user to build implicit profile
        """
        exclude_ids = exclude_ids or []
        
        # Build user vector once
        u_vec = self._get_user_vector(user_row, train_interactions)
            
        # Compute cosine similarity
        u_norm = np.linalg.norm(u_vec)
        if u_norm == 0:
            u_norm = 1.0
            
        scores = {}
        for hid, h_vec in self.hotel_features.items():
            if hid in exclude_ids:
                continue
            h_norm = np.linalg.norm(h_vec)
            if h_norm == 0:
                h_norm = 1.0
            sim = np.dot(u_vec, h_vec) / (u_norm * h_norm)
            scores[hid] = sim
            
        # Sort and recommend
        sorted_recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [hid for hid, score in sorted_recs[:top_n]]

    def predict_score(self, user_row, hotel_id, train_interactions=None, precomputed_u_vec=None):
        if precomputed_u_vec is not None:
            u_vec = precomputed_u_vec
        else:
            u_vec = self._get_user_vector(user_row, train_interactions)
            
        if hotel_id not in self.hotel_features:
            return 0.0
            
        h_vec = self.hotel_features[hotel_id]
        u_norm = np.linalg.norm(u_vec)
        h_norm = np.linalg.norm(h_vec)
        if u_norm == 0 or h_norm == 0:
            return 0.0
            
        return np.dot(u_vec, h_vec) / (u_norm * h_norm)
