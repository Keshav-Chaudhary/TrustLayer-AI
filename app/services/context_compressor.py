from typing import List, Dict, Any

class ContextCompressor:
    """
    Handles token-budget-aware compression and deduplication of retrieved evidence
    before sending it to the LLM.
    """
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        
    def compress(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Mock token length approximation (4 chars ~= 1 token)
        seen_snippets = set()
        compressed_chunks = []
        current_length = 0
        
        # Sort chunks: prioritize specific types (e.g., 'Review' over 'Profile') if needed.
        # Here we just iterate and deduplicate.
        for chunk in chunks:
            snippet = chunk.get("document", "").strip()
            
            # Deduplication
            if snippet in seen_snippets:
                continue
                
            approx_tokens = len(snippet) // 4
            
            # Token budget constraint
            if current_length + approx_tokens > self.max_tokens:
                break
                
            seen_snippets.add(snippet)
            compressed_chunks.append(chunk)
            current_length += approx_tokens
            
        return compressed_chunks
    
    def format_for_prompt(self, chunks: List[Dict[str, Any]]) -> str:
        """Formats the compressed chunks with explicit IDs and hotel names for citation injection."""
        formatted = []
        for c in chunks:
            meta = c.get("metadata", {})
            hname = meta.get("hotel_name") or meta.get("name") or meta.get("place_name") or f"Hotel {meta.get('hotel_id', '')[:6]}"
            formatted.append(f"[Chunk ID: {c.get('id', 'unknown')}] [Hotel: {hname}]\n{c.get('document', '')}")
        return "\n\n".join(formatted)
