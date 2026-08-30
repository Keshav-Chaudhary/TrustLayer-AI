import pandas as pd
import numpy as np

class CollaborativeFilteringSVD:
    def __init__(self, n_factors=10, lr=0.005, reg=0.02, epochs=60, random_state=42):
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.epochs = epochs
        self.random_state = random_state
        
        # Mappings
        self.user_to_idx = {}
        self.idx_to_user = {}
        self.hotel_to_idx = {}
        self.idx_to_hotel = {}
        
        # Biases & Latent factors
        self.mu = 0.0
        self.b_u = None
        self.b_i = None
        self.P = None
        self.Q = None
        
        # Tracking metrics
        self.history = {'loss': []}
        
    def _map_engagement(self, itype):
        mapping = {
            'view': 1.0,
            'click': 2.0,
            'rating': 4.0,
            'booking': 5.0
        }
        return mapping.get(itype, 1.0)
        
    def fit(self, interactions_df):
        # 1. Create rating targets
        df = interactions_df.copy()
        df['rating'] = df['interaction_type'].apply(self._map_engagement)
        
        # Aggregate interactions to maximum engagement score per user-hotel pair
        grouped = df.groupby(['user_id', 'google_place_id'])['rating'].max().reset_index()
        
        # 2. Build index mappings
        unique_users = grouped['user_id'].unique()
        unique_hotels = grouped['google_place_id'].unique()
        
        self.user_to_idx = {uid: idx for idx, uid in enumerate(unique_users)}
        self.idx_to_user = {idx: uid for idx, uid in enumerate(unique_users)}
        self.hotel_to_idx = {hid: idx for idx, hid in enumerate(unique_hotels)}
        self.idx_to_hotel = {idx: hid for idx, hid in enumerate(unique_hotels)}
        
        n_users = len(unique_users)
        n_items = len(unique_hotels)
        
        # 3. Initialize parameters
        rng = np.random.default_rng(self.random_state)
        self.mu = grouped['rating'].mean()
        self.b_u = np.zeros(n_users)
        self.b_i = np.zeros(n_items)
        self.P = rng.normal(0, 0.1, (n_users, self.n_factors))
        self.Q = rng.normal(0, 0.1, (n_items, self.n_factors))
        
        # 4. Prepare training samples
        samples = []
        for _, row in grouped.iterrows():
            u_idx = self.user_to_idx[row['user_id']]
            i_idx = self.hotel_to_idx[row['google_place_id']]
            r = row['rating']
            samples.append((u_idx, i_idx, r))
            
        # 5. Stochastic Gradient Descent
        for epoch in range(self.epochs):
            rng.shuffle(samples)
            for u, i, r in samples:
                # Prediction
                pred = self.mu + self.b_u[u] + self.b_i[i] + np.dot(self.P[u], self.Q[i])
                err = r - pred
                
                # Gradient update
                self.b_u[u] += self.lr * (err - self.reg * self.b_u[u])
                self.b_i[i] += self.lr * (err - self.reg * self.b_i[i])
                
                p_temp = self.P[u].copy()
                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * p_temp - self.reg * self.Q[i])
                
            # Calculate and store epoch loss (MSE)
            epoch_loss = 0.0
            for u, i, r in samples:
                pred = self.mu + self.b_u[u] + self.b_i[i] + np.dot(self.P[u], self.Q[i])
                epoch_loss += (r - pred) ** 2
            self.history['loss'].append(epoch_loss / len(samples))
            
        print(f"SVD fit completed. Users: {n_users}, Hotels: {n_items}")
        
    def predict_score(self, user_id, hotel_id):
        # Handle cold-start cases
        u_seen = user_id in self.user_to_idx
        i_seen = hotel_id in self.hotel_to_idx
        
        if u_seen and i_seen:
            u_idx = self.user_to_idx[user_id]
            i_idx = self.hotel_to_idx[hotel_id]
            return self.mu + self.b_u[u_idx] + self.b_i[i_idx] + np.dot(self.P[u_idx], self.Q[i_idx])
        elif i_seen:
            # Cold user: global mean + item bias
            i_idx = self.hotel_to_idx[hotel_id]
            return self.mu + self.b_i[i_idx]
        elif u_seen:
            # Cold item: global mean + user bias
            u_idx = self.user_to_idx[user_id]
            return self.mu + self.b_u[u_idx]
        else:
            # Both unseen
            return self.mu
            
    def recommend(self, user_id, all_hotels, top_n=10, exclude_ids=None):
        exclude_ids = exclude_ids or []
        scores = {}
        
        for hid in all_hotels:
            if hid in exclude_ids:
                continue
            scores[hid] = self.predict_score(user_id, hid)
            
        # Sort by predicted score descending
        sorted_recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [hid for hid, score in sorted_recs[:top_n]]
