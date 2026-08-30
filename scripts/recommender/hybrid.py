import numpy as np

class HybridRecommender:
    def __init__(self, cb_model, cf_model, k=60):
        """
        cb_model: Trained ContentBasedRecommender
        cf_model: Trained CollaborativeFilteringSVD
        k: Smoothing parameter for Reciprocal Rank Fusion
        """
        self.cb_model = cb_model
        self.cf_model = cf_model
        self.k = k
        
    def recommend(self, user_row, all_hotels, train_interactions=None, top_n=10, exclude_ids=None):
        exclude_ids = exclude_ids or []
        user_id = user_row['user_id']
        
        # Determine if this is a cold-start user (no training interactions)
        is_cold = True
        if train_interactions is not None and len(train_interactions) > 0:
            user_ints = train_interactions[train_interactions['user_id'] == user_id]
            if len(user_ints) > 0:
                is_cold = False
                
        # If cold-start, fall back to pure Content-Based recommendation
        
        # Candidate hotels to recommend
        candidates = [hid for hid in all_hotels if hid not in exclude_ids]
        if not candidates:
            return []
            
        # Precompute CB user vector
        cb_u_vec = self.cb_model._get_user_vector(user_row, train_interactions)
        
        # Get raw scores
        cb_scores = []
        cf_scores = []
        
        for hid in candidates:
            cb_scores.append(self.cb_model.predict_score(user_row, hid, train_interactions=None, precomputed_u_vec=cb_u_vec))
            cf_scores.append(self.cf_model.predict_score(user_id, hid))
            
        cb_scores = np.array(cb_scores)
        cf_scores = np.array(cf_scores)
        
        # Calculate ranks (higher score = lower rank number)
        # Sort indices descending to get rank
        cb_sort_idx = np.argsort(cb_scores)[::-1]
        cf_sort_idx = np.argsort(cf_scores)[::-1]
        
        # Build dictionaries for rank mapping
        cb_ranks = {candidates[idx]: rank + 1 for rank, idx in enumerate(cb_sort_idx)}
        cf_ranks = {candidates[idx]: rank + 1 for rank, idx in enumerate(cf_sort_idx)}
        
        # Calculate RRF score for each candidate
        hybrid_scores = []
        for hid in candidates:
            if is_cold:
                # If cold start, RRF only relies on CB
                rrf_score = 1.0 / (self.k + cb_ranks[hid])
            else:
                rrf_score = 1.0 / (self.k + cb_ranks[hid]) + 1.0 / (self.k + cf_ranks[hid])
            hybrid_scores.append(rrf_score)
        
        # Pair up and sort
        scored_candidates = list(zip(candidates, hybrid_scores))
        sorted_recs = sorted(scored_candidates, key=lambda x: x[1], reverse=True)
        
        return [hid for hid, score in sorted_recs[:top_n]]

    def predict_score(self, user_row, hotel_id, train_interactions=None, all_candidates=None):
        """
        Calculates hybrid score for a single hotel.
        all_candidates is optionally supplied to compute proper min-max normalization context.
        """
        user_id = user_row['user_id']
        is_cold = True
        if train_interactions is not None and len(train_interactions) > 0:
            user_ints = train_interactions[train_interactions['user_id'] == user_id]
            if len(user_ints) > 0:
                is_cold = False
                
        # For single hotel prediction in reports, RRF requires ranking against all candidates.
        # If all_candidates is not provided, we cannot properly compute rank. We'll return a fallback.
        if all_candidates is None or len(all_candidates) <= 1:
            return 0.0
            
        cb_u_vec = self.cb_model._get_user_vector(user_row, train_interactions)
        
        cb_scores = [self.cb_model.predict_score(user_row, hid, precomputed_u_vec=cb_u_vec) for hid in all_candidates]
        cf_scores = [self.cf_model.predict_score(user_id, hid) for hid in all_candidates]
        
        cb_sort_idx = np.argsort(cb_scores)[::-1]
        cf_sort_idx = np.argsort(cf_scores)[::-1]
        
        cb_ranks = {all_candidates[idx]: rank + 1 for rank, idx in enumerate(cb_sort_idx)}
        cf_ranks = {all_candidates[idx]: rank + 1 for rank, idx in enumerate(cf_sort_idx)}
        
        if is_cold:
            return 1.0 / (self.k + cb_ranks.get(hotel_id, len(all_candidates)))
            
        return 1.0 / (self.k + cb_ranks.get(hotel_id, len(all_candidates))) + 1.0 / (self.k + cf_ranks.get(hotel_id, len(all_candidates)))
