import re
from typing import Dict, Any

class QueryParser:
    def __init__(self, custom_areas: list = None):
        if custom_areas:
            self.areas = [a.lower() for a in custom_areas]
        else:
            self.areas = ["mahipalpur", "karol bagh", "loni", "delhi ncr", "delhi", "new delhi", "gurugram", "noida", "mumbai", "goa", "bangalore", "jaipur", "pune", "aerocity"]
        self.budgets = ["budget", "cheap", "mid-range", "luxury", "expensive"]
        self.purposes = ["business", "family", "solo", "couple", "leisure"]
        self.aspects = ["cleanliness", "service", "location", "value", "staff", "food", "wifi", "pool", "view", "parking"]
        
    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parses natural language query into hard and soft constraints.
        Returns expected metadata structure for oracle evaluation.
        """
        q_lower = query.lower()
        
        parsed = {
            "hard": {},
            "soft": {}
        }
        
        # 1. Parse Area (Fuzzy, Synonyms & Multi-Area matching)
        import difflib
        
        # Pre-clean spelling variations
        q_clean = q_lower.replace("pahar ganj", "paharganj")\
                         .replace("mahipal pur", "mahipalpur")\
                         .replace("preetvihar", "preet vihar")\
                         .replace("gurgaon", "gurugram")
                         
        matched_areas = []
        exact_matched_areas = []
        for area in sorted(self.areas, key=len, reverse=True):
            # Try exact match first
            if area in q_clean:
                exact_matched_areas.append(area)
            else:
                # Token-level fuzzy match
                for word in q_clean.split():
                    if len(word) > 4 and len(area) > 4:
                        ratio = difflib.SequenceMatcher(None, word, area).ratio()
                        if ratio > 0.8:
                            matched_areas.append(area)
                            break
                            
        final_matched = exact_matched_areas if exact_matched_areas else matched_areas
        
        if final_matched:
            unique_matched = []
            for a in final_matched:
                if a not in unique_matched:
                    unique_matched.append(a)
                    
            canonical_names = []
            for a in unique_matched:
                if a in ["delhi", "new delhi"]:
                    canonical_names.append("Delhi NCR")
                elif a == "gurgaon":
                    canonical_names.append("Gurugram")
                else:
                    canonical_names.append(a.title())
            
            parsed["hard"]["area"] = ",".join(canonical_names)
                
        # 2. Parse Budget (Hard constraint if explicitly asked)
        for budget in self.budgets:
            if budget in q_lower:
                mapped_budget = "budget" if budget == "cheap" else "luxury" if budget == "expensive" else budget
                # Assign budget as soft unless explicitly asked "strictly" or if no other constraints exist,
                # but usually budget is considered a hard constraint for specific query types.
                # The implementation plan specifies budget as hard/soft depending on phrasing. Let's default to soft for general queries, hard for explicit.
                if "strictly" in q_lower or "only" in q_lower:
                    parsed["hard"]["budget_category"] = mapped_budget
                else:
                    parsed["soft"]["budget_category"] = mapped_budget
                break
                
        # 3. Parse Travel Purpose (Soft constraint)
        purpose_matches = []
        for purpose in self.purposes:
            if purpose in q_lower:
                purpose_matches.append(purpose)
        if purpose_matches:
            parsed["soft"]["travel_purpose"] = ",".join(purpose_matches)
            
        # 4. Parse Aspects (Soft constraint)
        aspect_matches = []
        for aspect in self.aspects:
            if aspect in q_lower:
                aspect_matches.append(aspect)
        if aspect_matches:
            parsed["soft"]["aspects"] = ",".join(aspect_matches)
            
        # 5. Parse Amenities (Soft constraint)
        amenities_list = ["breakfast", "wifi", "pool", "parking", "gym", "spa", "bar", "restaurant", "laundry", "ac"]
        amenity_matches = []
        for am in amenities_list:
            if am in q_lower:
                if am == "wifi":
                    amenity_matches.append("Free Wi-Fi")
                elif am == "ac":
                    amenity_matches.append("Air Conditioning")
                else:
                    amenity_matches.append(am.title())
        if amenity_matches:
            parsed["soft"]["amenities"] = ",".join(amenity_matches)
            
        # 6. Intent Constraints Mapping
        intent_constraints = {}
        if "cleanliness" in q_lower or "cleanest" in q_lower or "clean room" in q_lower or "clean hotel" in q_lower:
            intent_constraints["cleanliness"] = 4.8
        if "safe" in q_lower or "safety" in q_lower or "security" in q_lower:
            intent_constraints["trust"] = 95.0
        if "best" in q_lower or "top" in q_lower or "highest rated" in q_lower:
            intent_constraints["trust"] = 90.0
            intent_constraints["rating"] = 4.5
            intent_constraints["reviews_count"] = 500
        parsed["intent_constraints"] = intent_constraints

        return parsed

    def evaluate_parser(self, query: str, expected: Dict[str, Any]) -> Dict[str, bool]:
        """
        Evaluates the parser accuracy against an expected constraint set.
        """
        parsed = self.parse(query)
        
        # Flatten for comparison
        parsed_flat = {**parsed["hard"], **parsed["soft"]}
        expected_flat = {**expected.get("hard", {}), **expected.get("soft", {})}
        
        results = {
            "area": parsed_flat.get("area", "").lower() == expected_flat.get("area", "").lower(),
            "budget": parsed_flat.get("budget_category", "").lower() == expected_flat.get("budget_category", "").lower(),
            "purpose": parsed_flat.get("travel_purpose", "").lower() == expected_flat.get("travel_purpose", "").lower(),
            "aspect": parsed_flat.get("aspects", "").lower() == expected_flat.get("aspects", "").lower(),
        }
        
        # Overall is true if all specified expected constraints are correctly parsed
        results["overall"] = all([
            parsed_flat.get(k, "").lower() == expected_flat.get(k, "").lower() 
            for k in expected_flat.keys()
        ])
        
        return results

if __name__ == "__main__":
    parser = QueryParser()
    res = parser.parse("luxury family hotels in Delhi")
    print(res)
