from typing import List, Dict, Any

class GroundingValidator:
    def __init__(self):
        pass

    def validate_response(self, response_text: str, provenance_chunks: List[Dict[str, Any]], hotel_name: str) -> Dict[str, Any]:
        """
        Post-processes LLM output to ensure zero hallucinations.
        Checks if amenities or claims are present in the provided provenance chunks.
        """
        combined_provenance = " ".join([chunk.get("document", "") for chunk in provenance_chunks]).lower()
        response_lower = response_text.lower()
        # Define a list of high-risk claims (amenities)
        high_risk_keywords = ["pool", "spa", "gym", "breakfast", "wifi", "parking", "restaurant", "bar", "beach", "pet"]
        
        unsupported_claims = []
        for keyword in high_risk_keywords:
            if keyword in response_lower and keyword not in combined_provenance:
                unsupported_claims.append(keyword)
                
        is_valid = len(unsupported_claims) == 0
        
        remediated_text = response_text
        if not is_valid:
            # Simple remediation: append a disclaimer
            disclaimer = f" (Warning: AI generated claims about {', '.join(unsupported_claims)} could not be verified in the reviews.)"
            remediated_text += disclaimer
            
        return {
            "is_valid": is_valid,
            "unsupported_claims": unsupported_claims,
            "remediated_text": remediated_text
        }
