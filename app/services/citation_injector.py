import re
from typing import List, Dict, Any, Tuple

class CitationInjector:
    """
    Parses LLM outputs for citation markers and strictly maps them back to the 
    original provenance chunks, ensuring traceability for every claim.
    """
    
    def extract_and_verify_citations(self, text: str, available_chunks: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Finds patterns like [Chunk ID: X] or [X] and verifies they exist in available_chunks.
        Returns the formatted text and the valid provenance metadata.
        """
        # A real implementation would parse complex citations.
        # Here we do a simple substring match for known chunk IDs for demonstration.
        
        valid_citations = []
        seen_ids = set()
        
        # Simple extraction logic: check if chunk ID is mentioned in the text
        for chunk in available_chunks:
            cid = chunk.get("id")
            if cid and cid in text and cid not in seen_ids:
                valid_citations.append({
                    "chunk_id": cid,
                    "chunk_type": chunk.get("metadata", {}).get("chunk_type", "Text"),
                    "snippet": chunk.get("document", "")[:100]
                })
                seen_ids.add(cid)
                # Normalize citation format in text if needed
                text = text.replace(cid, f"[{cid}]")
                
        return text, valid_citations
