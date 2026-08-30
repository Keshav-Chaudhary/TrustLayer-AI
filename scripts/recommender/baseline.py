import pandas as pd
import numpy as np

class PopularityBaselineRecommender:
    def __init__(self, hotels_df):
        self.hotels_df = hotels_df.copy()
        
        # Fill missing values
        pop = self.hotels_df['popularity_score'].fillna(0.0)
        trust = self.hotels_df['trust_score'].fillna(0.0)
        
        # Min-max scale to align scales
        if pop.max() != pop.min():
            pop_scaled = (pop - pop.min()) / (pop.max() - pop.min())
        else:
            pop_scaled = pop
            
        if trust.max() != trust.min():
            trust_scaled = (trust - trust.min()) / (trust.max() - trust.min())
        else:
            trust_scaled = trust
            
        # Linear combination
        self.hotels_df['baseline_score'] = 0.5 * pop_scaled + 0.5 * trust_scaled
        
        # Sort and get ranked IDs
        self.ranked_hotels = self.hotels_df.sort_values(by='baseline_score', ascending=False)['google_place_id'].tolist()
        self.scores_dict = dict(zip(self.hotels_df['google_place_id'], self.hotels_df['baseline_score']))
        
    def recommend(self, user_id, top_n=10, exclude_ids=None):
        exclude_ids = exclude_ids or []
        recs = []
        for hid in self.ranked_hotels:
            if hid not in exclude_ids:
                recs.append(hid)
            if len(recs) == top_n:
                break
        return recs

    def predict_score(self, user_id, hotel_id):
        return self.scores_dict.get(hotel_id, 0.0)
