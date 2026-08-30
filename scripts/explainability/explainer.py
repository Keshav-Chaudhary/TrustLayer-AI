import numpy as np
import pandas as pd

class RecommendationExplainer:
    def __init__(self, hybrid_recommender):
        self.hybrid = hybrid_recommender
        self.cb = hybrid_recommender.cb_model
        self.cf = hybrid_recommender.cf_model
        self.k = hybrid_recommender.k
        
        # Determine feature block indices for CB
        self.aspects = ['cleanliness_score', 'service_score', 'location_score', 'value_for_money_score', 'staff_behavior_score']
        self.other_scores = ['trust_score', 'popularity_score', 'rating_score', 'sentiment_score']
        
        # 0:5 aspects, 5:9 other scores
        self.area_start = 9
        self.area_end = 9 + len(self.cb.unique_areas)
        self.budget_start = self.area_end
        self.budget_end = self.budget_start + len(self.cb.unique_budgets)

    def explain(self, user_row, hotel_id, all_hotels, train_interactions=None):
        """
        Extract structured explanation for why hotel_id was recommended to user_row.
        Returns a JSON-serializable dictionary.
        """
        user_id = user_row['user_id']
        
        # 1. Determine cold-start and interaction counts
        interaction_count = 0
        is_cold = True
        user_ints = pd.DataFrame()
        
        if train_interactions is not None and len(train_interactions) > 0:
            user_ints = train_interactions[train_interactions['user_id'] == user_id]
            interaction_count = len(user_ints)
            if interaction_count > 5:
                is_cold = False

        # 2. Get precomputed vectors and calculate ranks
        cb_u_vec = self.cb._get_user_vector(user_row, train_interactions)
        
        cb_scores = []
        cf_scores = []
        
        for hid in all_hotels:
            cb_scores.append(self.cb.predict_score(user_row, hid, precomputed_u_vec=cb_u_vec))
            cf_scores.append(self.cf.predict_score(user_id, hid))
            
        cb_sort_idx = np.argsort(cb_scores)[::-1]
        cf_sort_idx = np.argsort(cf_scores)[::-1]
        
        cb_ranks = {all_hotels[idx]: rank + 1 for rank, idx in enumerate(cb_sort_idx)}
        cf_ranks = {all_hotels[idx]: rank + 1 for rank, idx in enumerate(cf_sort_idx)}
        
        cb_rank = cb_ranks.get(hotel_id, len(all_hotels))
        cf_rank = cf_ranks.get(hotel_id, len(all_hotels))
        
        # 3. Hybrid RRF Decomposition
        if is_cold:
            rrf_score = 1.0 / (self.k + cb_rank)
            cb_contrib = 1.0
            cf_contrib = 0.0
        else:
            cb_val = 1.0 / (self.k + cb_rank)
            cf_val = 1.0 / (self.k + cf_rank)
            rrf_score = cb_val + cf_val
            cb_contrib = cb_val / rrf_score
            cf_contrib = cf_val / rrf_score

        if cb_contrib > 0.6:
            explanation_type = "cb_dominant"
        elif cf_contrib > 0.6:
            explanation_type = "cf_dominant"
        else:
            explanation_type = "balanced_hybrid"

        # 4. Confidence Score Logic
        # High: >25 interactions, both rank in top 10
        # Low: cold start
        # Medium: otherwise
        if is_cold:
            confidence = "Low"
        elif interaction_count > 25 and cb_rank <= 10 and cf_rank <= 10:
            confidence = "High"
        elif interaction_count > 25 and cb_contrib > 0.6 and cb_rank <= 5:
            # High interaction, but leans CB heavily. Still good if CB rank is very high.
            confidence = "High"
        elif interaction_count > 10 and cf_contrib > 0.6 and cf_rank <= 5:
             confidence = "High"
        else:
            confidence = "Medium"

        # 5. Extract CB feature contributions via dot product breakdown
        top_factors = []
        
        if cb_contrib > 0.3 or is_cold:
            h_vec = self.cb.hotel_features.get(hotel_id, np.zeros(self.cb.feature_dim))
            feature_products = cb_u_vec * h_vec
            
            # Aggregate blocks
            aspect_prod = np.sum(feature_products[0:5])
            other_prod = np.sum(feature_products[5:9])
            area_prod = np.sum(feature_products[self.area_start:self.area_end])
            budget_prod = np.sum(feature_products[self.budget_start:self.budget_end])
            
            # Find which specific aspect is best
            best_aspect_idx = np.argmax(feature_products[0:5])
            best_aspect_name = self.aspects[best_aspect_idx].replace('_score', '')
            
            if area_prod > 0.5:
                top_factors.append("area_match")
            if budget_prod > 0.5:
                top_factors.append("budget_match")
            if aspect_prod > 0.5:
                top_factors.append(f"{best_aspect_name}_sentiment")
            if feature_products[5] > 0.5: # index 5 is trust_score
                top_factors.append("high_trust_score")

        # 6. Extract CF similar item evidence
        similar_hotel_str = None
        if cf_contrib > 0.3 and not is_cold and hotel_id in self.cf.hotel_to_idx:
            # User interacted items
            interacted_hids = user_ints['google_place_id'].tolist()
            valid_interacted = [hid for hid in interacted_hids if hid in self.cf.hotel_to_idx]
            
            if valid_interacted:
                target_i_idx = self.cf.hotel_to_idx[hotel_id]
                target_latent = self.cf.Q[target_i_idx]
                target_norm = np.linalg.norm(target_latent)
                
                best_sim = -1
                best_sim_hid = None
                
                for past_hid in valid_interacted:
                    if past_hid == hotel_id:
                        continue
                    past_idx = self.cf.hotel_to_idx[past_hid]
                    past_latent = self.cf.Q[past_idx]
                    past_norm = np.linalg.norm(past_latent)
                    
                    if target_norm > 0 and past_norm > 0:
                        sim = np.dot(target_latent, past_latent) / (target_norm * past_norm)
                        if sim > best_sim:
                            best_sim = sim
                            best_sim_hid = past_hid
                            
                if best_sim > 0.5 and best_sim_hid:
                    top_factors.append("similar_to_past_view")
                    similar_hotel_str = best_sim_hid

        # Deduplicate top factors
        top_factors = list(dict.fromkeys(top_factors))
        
        # Fallback if no factors
        if not top_factors:
            top_factors.append("popularity_fallback")

        # 7. Generate NLG Text
        nlg_text = self._generate_nlg(explanation_type, confidence, top_factors, user_row, similar_hotel_str)

        return {
            "hotel_id": hotel_id,
            "user_id": user_id,
            "cb_rank": cb_rank,
            "cf_rank": cf_rank,
            "rrf_score": float(rrf_score),
            "explanation_type": explanation_type,
            "top_factors": top_factors,
            "confidence": confidence,
            "nlg_text": nlg_text
        }

    def _generate_nlg(self, exp_type, confidence, factors, user_row, similar_hotel_str):
        area = user_row.get('preferred_area', 'your preferred area')
        budget = user_row.get('budget_preference', 'your budget')
        
        reasons = []
        if "area_match" in factors:
            reasons.append(f"matches your preferred area ({area})")
        if "budget_match" in factors:
            reasons.append(f"falls within your budget category ({budget})")
            
        sentiment_factors = [f for f in factors if "_sentiment" in f]
        if sentiment_factors:
            best_sent = sentiment_factors[0].split('_')[0]
            reasons.append(f"has excellent {best_sent} sentiment")
            
        if "high_trust_score" in factors:
            reasons.append("has a strong verified trust score")
            
        if "similar_to_past_view" in factors:
            reasons.append("is similar to hotels you previously viewed")
            
        if "popularity_fallback" in factors:
            reasons.append("is a highly popular and trusted choice")
            
        if exp_type == "cf_dominant" and "similar_to_past_view" not in factors:
            reasons.append("was highly ranked by travelers with similar booking patterns")
            
        if exp_type == "balanced_hybrid":
            if "was highly ranked by travelers with similar booking patterns" not in reasons and "is similar to hotels you previously viewed" not in reasons:
                reasons.append("is highly favored by similar travelers")
                
        # Join reasons naturally
        if len(reasons) == 1:
            reason_str = reasons[0]
        elif len(reasons) == 2:
            reason_str = f"{reasons[0]} and {reasons[1]}"
        else:
            reason_str = ", ".join(reasons[:-1]) + f", and {reasons[-1]}"
            
        return f"Recommended because it {reason_str}. Confidence: {confidence}"
