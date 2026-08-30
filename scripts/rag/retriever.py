import os
import chromadb
from typing import List, Dict, Any, Tuple

class HybridRetriever:
    def __init__(self, vector_store_dir: str):
        self.client = chromadb.PersistentClient(path=vector_store_dir)
        self.collection = self.client.get_collection(name="hotel_knowledge")

    def _normalize_semantic_scores(self, distances: List[float]) -> List[float]:
        if not distances:
            return []
        min_dist = min(distances)
        max_dist = max(distances)
        
        normalized = []
        for dist in distances:
            sim = 1.0 - ((dist - min_dist) / (max_dist - min_dist + 1e-9))
            normalized.append(sim)
        return normalized

    def _calculate_metadata_score(self, metadata: Dict[str, Any], soft_constraints: Dict[str, str]) -> float:
        if not soft_constraints:
            return 0.0
            
        area_match = 0.0
        if 'area' in soft_constraints:
            target = soft_constraints['area'].lower()
            actual = str(metadata.get('area', '')).lower()
            if target == actual:
                area_match = 1.0
                
        budget_match = 0.0
        if 'budget_category' in soft_constraints:
            target = soft_constraints['budget_category'].lower()
            actual = str(metadata.get('budget_category', '')).lower()
            categories = ['budget', 'mid-range', 'luxury']
            
            if target == actual:
                budget_match = 1.0
            elif target in categories and actual in categories:
                target_idx = categories.index(target)
                actual_idx = categories.index(actual)
                if abs(target_idx - actual_idx) == 1:
                    budget_match = 0.5
                    
        purpose_match = 0.0
        if 'travel_purpose' in soft_constraints:
            target_tags = set(soft_constraints['travel_purpose'].lower().split(','))
            actual_tags = set(str(metadata.get('travel_purpose_tags', '')).lower().split(','))
            if actual_tags:
                intersection = len(target_tags.intersection(actual_tags))
                union = len(target_tags.union(actual_tags))
                purpose_match = intersection / union if union > 0 else 0.0

        amenities_match = 0.0
        if 'amenities' in soft_constraints:
            target_am = set(soft_constraints['amenities'].lower().split(','))
            actual_am = set([a.strip().lower() for a in metadata.get('amenities', []) if a])
            if target_am:
                intersection = len(target_am.intersection(actual_am))
                amenities_match = intersection / len(target_am)

        return 0.40 * area_match + 0.25 * budget_match + 0.20 * purpose_match + 0.15 * amenities_match

    def _calculate_rec_score(self, metadata: Dict[str, Any]) -> float:
        trust = float(metadata.get('trust_score', 0.0))
        rating = float(metadata.get('rating_score', 1.0))
        sentiment = float(metadata.get('sentiment_score', 0.0))
        
        normalized_rating = (rating - 1) / 4.0
        
        return 0.40 * trust + 0.30 * normalized_rating + 0.30 * sentiment

    def retrieve(self, query: str, hard_constraints: Dict[str, str] = None, soft_constraints: Dict[str, str] = None, top_k: int = 10) -> Tuple[List[Dict[str, Any]], int]:
        hard_constraints = hard_constraints or {}
        soft_constraints = soft_constraints or {}
        
        # Initial large fetch to ensure we have enough after hard filtering
        fetch_k = top_k * 5
        where_clause = None
        if hard_constraints and 'hotel_id' in hard_constraints:
            if isinstance(hard_constraints['hotel_id'], list):
                if hard_constraints['hotel_id']:
                    where_clause = {'hotel_id': {'$in': hard_constraints['hotel_id']}}
            else:
                where_clause = {'hotel_id': hard_constraints['hotel_id']}
            
        allowed_types = ["Chunk A (Profile)", "Chunk B (Aspects)", "Chunk E (Rec Signals)"]
        type_filter = {"chunk_type": {"$in": allowed_types}}
        if where_clause:
            where_clause = {
                "$and": [
                    where_clause,
                    type_filter
                ]
            }
        else:
            where_clause = type_filter

        results = self.collection.query(
            query_texts=[query],
            n_results=fetch_k,
            where=where_clause
        )
        
        if not results['ids'] or not results['ids'][0]:
            return [], 0
            
        ids = results['ids'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        documents = results['documents'][0]
        
        # Fallback hierarchy
        # Level 0: All hard constraints
        # Level 1: Relax budget constraint
        # Level 2: Relax area constraint (and budget)
        # Level 3: Pure semantic
        fallback_levels = [
            hard_constraints,
            {k: v for k, v in hard_constraints.items() if k != 'budget_category'},
            {k: v for k, v in hard_constraints.items() if k not in ['budget_category', 'area']},
            {k: v for k, v in hard_constraints.items() if k == 'hotel_id'}
        ]
        
        filtered_candidates = []
        triggered_fallback_level = 0
        
        for level, current_hard_constraints in enumerate(fallback_levels):
            filtered_candidates = []
            for i in range(len(ids)):
                meta = metadatas[i]
                
                # Apply hard constraints for current level
                skip = False
                for k, v in current_hard_constraints.items():
                    if k == 'area':
                        target_areas = [a.strip().lower() for a in str(v).split(',')]
                        meta_area = str(meta.get(k, '')).lower()
                        if not any(t in meta_area for t in target_areas):
                            skip = True
                            break
                    elif k == 'hotel_id' and isinstance(v, list):
                        if meta.get(k) not in v:
                            skip = True
                            break
                    elif str(meta.get(k, '')).lower() != str(v).lower():
                        skip = True
                        break
                        
                if not skip:
                    filtered_candidates.append({
                        'id': ids[i],
                        'distance': distances[i],
                        'metadata': meta,
                        'document': documents[i]
                    })
            
            if filtered_candidates:
                triggered_fallback_level = level
                break
                
        if not filtered_candidates:
            return [], 3
            
        # 2. Semantic Normalization (Query-local min-max)
        filtered_distances = [c['distance'] for c in filtered_candidates]
        normalized_semantics = self._normalize_semantic_scores(filtered_distances)
        
        # 3. Compute final scores
        final_results = []
        for i, candidate in enumerate(filtered_candidates):
            semantic_score = normalized_semantics[i]
            metadata_score = self._calculate_metadata_score(candidate['metadata'], soft_constraints)
            rec_score = self._calculate_rec_score(candidate['metadata'])
            
            # Exact area boost
            area_boost = 0.0
            target_area = hard_constraints.get('area') if hard_constraints else None
            if target_area and candidate['metadata'].get('area'):
                target_areas = [a.strip().lower() for a in str(target_area).split(',')]
                if str(candidate['metadata'].get('area')).lower() in target_areas:
                    area_boost = 0.12
                    
            # Amenities penalty
            amenities_penalty = 0.0
            if soft_constraints and 'amenities' in soft_constraints:
                target_am = set(soft_constraints['amenities'].lower().split(','))
                actual_am = set([a.strip().lower() for a in candidate['metadata'].get('amenities', []) if a])
                for am in target_am:
                    if am not in actual_am:
                        amenities_penalty += 0.15

            final_score = (0.60 * semantic_score) + (0.20 * metadata_score) + (0.20 * rec_score) + area_boost - amenities_penalty
            
            final_results.append({
                'id': candidate['id'],
                'document': candidate['document'],
                'metadata': candidate['metadata'],
                'debug_info': {
                    'raw_distance': float(candidate['distance']),
                    'semantic_score': semantic_score,
                    'metadata_score': metadata_score,
                    'recommendation_score': rec_score,
                    'area_boost': area_boost,
                    'amenities_penalty': amenities_penalty,
                    'final_score': final_score,
                    'hard_constraints_applied': fallback_levels[triggered_fallback_level],
                    'metadata_matches': soft_constraints,
                },
                'final_score': final_score
            })
            
        # 4. Rank and sort
        final_results.sort(key=lambda x: x['final_score'], reverse=True)
        top_results = final_results[:top_k]
        
        # Add rerank position
        for i, res in enumerate(top_results):
            res['debug_info']['rerank_position'] = i + 1
            
        return top_results, triggered_fallback_level
