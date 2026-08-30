import re
from typing import List, Dict, Any, Tuple

class ContextBuilder:
    def __init__(self, max_tokens: int = 2000):
        # A simple token estimator: 1 token ~ 4 characters
        self.max_tokens = max_tokens
        
    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4
        
    def _deduplicate_evidence(self, items: List[str]) -> List[str]:
        """Simple exact and substring deduplication for text snippets"""
        unique_items = []
        for item in items:
            item_clean = item.strip()
            if not item_clean: continue
            
            is_dup = False
            for u in unique_items:
                if item_clean in u or u in item_clean:
                    is_dup = True
                    break
            if not is_dup:
                unique_items.append(item_clean)
        return unique_items

    def build_context(self, retrieved_results: List[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """
        Builds the context string and returns audit metrics.
        """
        # Group by hotel
        hotels = {}
        for res in retrieved_results:
            hid = res['metadata']['hotel_id']
            if hid not in hotels:
                hotels[hid] = []
            hotels[hid].append(res)
            
        sections = {
            "explanation": [],
            "aspect": [],
            "pos_review": [],
            "neg_review": [],
            "trust": []
        }
        
        chunk_types_seen = set()
        duplicate_chunks_removed = 0
        total_evidence_items_before = 0
        total_evidence_items_after = 0
        
        # Deduplicate chunks by ID
        seen_chunk_ids = set()
        deduped_results = []
        for res in retrieved_results:
            if res['id'] in seen_chunk_ids:
                duplicate_chunks_removed += 1
                continue
            seen_chunk_ids.add(res['id'])
            deduped_results.append(res)
            
        # Parse and categorize chunks
        for res in deduped_results:
            ctype = res['metadata'].get('chunk_type', '')
            hid = res['metadata']['hotel_id']
            ev_level = res['metadata'].get('evidence_level', 'none')
            provenance = f"(Hotel: {hid} | {ctype} | {ev_level})"
            
            chunk_types_seen.add(ctype)
            
            doc = res['document']
            total_evidence_items_before += 1
            
            if 'Chunk E' in ctype:
                sections['explanation'].append(f"{doc} {provenance}")
                sections['trust'].append(f"{doc} {provenance}")
            elif 'Chunk B' in ctype:
                sections['aspect'].append(f"{doc} {provenance}")
            elif 'Chunk C' in ctype:
                sections['pos_review'].append(f"{doc} {provenance}")
            elif 'Chunk D' in ctype:
                sections['neg_review'].append(f"{doc} {provenance}")
            elif 'Chunk A' in ctype:
                sections['trust'].append(f"{doc} {provenance}")
                
        # Deduplicate within sections
        for k in sections:
            total_evidence_items_after += len(self._deduplicate_evidence(sections[k]))
            sections[k] = self._deduplicate_evidence(sections[k])
            
        # Build priority sections
        # 1. Recommendation explanation
        # 2. Aspect evidence
        # 3. Positive review evidence
        # 4. Negative review evidence
        # 5. Trust / popularity metadata
        priority_keys = ["explanation", "aspect", "pos_review", "neg_review", "trust"]
        section_titles = {
            "explanation": "Section 1: Recommendation Explanation",
            "aspect": "Section 3: Aspect Evidence",
            "pos_review": "Section 2a: Positive Review Evidence",
            "neg_review": "Section 2b: Negative Review Evidence",
            "trust": "Section 4: Trust and Popularity Signals"
        }
        
        final_context_parts = []
        current_tokens = 0
        exceeded_budget = False
        
        tokens_before_compression = sum([self._estimate_tokens(" ".join(sections[k])) for k in sections])
        if tokens_before_compression > self.max_tokens:
            exceeded_budget = True
            
        for k in priority_keys:
            if not sections[k]:
                continue
                
            title = f"\n[{section_titles[k]}]\n"
            title_tokens = self._estimate_tokens(title)
            
            if current_tokens + title_tokens >= self.max_tokens:
                break
                
            final_context_parts.append(title)
            current_tokens += title_tokens
            
            for item in sections[k]:
                item_tokens = self._estimate_tokens(item + "\n")
                if current_tokens + item_tokens <= self.max_tokens:
                    final_context_parts.append(item + "\n")
                    current_tokens += item_tokens
                else:
                    # Partial inclusion or break
                    break
                    
        final_context = "".join(final_context_parts).strip()
        tokens_after_compression = self._estimate_tokens(final_context)
        
        compression_ratio = tokens_after_compression / (tokens_before_compression + 1e-9)
        duplicate_evidence_rate = 1.0 - (total_evidence_items_after / (total_evidence_items_before + 1e-9)) if total_evidence_items_before else 0.0
        
        audit_metrics = {
            "tokens_before": tokens_before_compression,
            "tokens_after": tokens_after_compression,
            "compression_ratio": compression_ratio,
            "exceeded_budget": exceeded_budget,
            "duplicate_evidence_rate": duplicate_evidence_rate,
            "duplicate_chunks_removed": duplicate_chunks_removed,
            "context_reduction_percent": (1.0 - compression_ratio) * 100,
            "hotels_represented": len(hotels),
            "chunk_types_represented": len(chunk_types_seen)
        }
        
        return final_context, audit_metrics

if __name__ == "__main__":
    pass
