import asyncio
import json
from app.services.recommendation_service import RecommendationService

async def main():
    service = RecommendationService()
    query = "Paharganj for couple"
    print(f"Starting pipeline audit for: {query}")
    
    # Stage 1: Query Parser
    parsed = service.parser.parse(query)
    print("\n--- 1. Query Parser Output ---")
    print(f"parsed.area: {parsed.get('hard', {}).get('area')}")
    print(f"parsed.purpose: {parsed.get('soft', {}).get('travel_purpose')}")
    print(f"parsed.budget: {parsed.get('hard', {}).get('budget_category')}")
    print(f"parsed.amenities: {parsed.get('soft', {}).get('amenities')}")
    print(f"parsed.normalized_query: None (not returned by parser)")
    
    # Let's run the actual recommend endpoint logic (Stage 2-5)
    print("\nRunning get_recommendations...")
    # This might use fallback logic, so we need to mock or trace it.
    
    # We will trace it manually based on recommendation_service.py
    print("\n--- 2. Retriever Constraint Output ---")
    area = parsed.get("hard", {}).get("area")
    filters = {"area": area} if area and area.lower() != "all" else {}
    print(f"hard_constraints: {filters}")
    
    candidates, _ = service.retriever.retrieve(query, filters, {}, top_k=50)
    print(f"candidate_count_before_semantic: {len(candidates)}")
    
    unique_areas = set()
    for c in candidates:
        if c.get("metadata") and c["metadata"].get("area"):
            unique_areas.add(c["metadata"]["area"])
    print(f"unique_candidate_areas: {list(unique_areas)}")
    
    print("\n--- 3. Semantic Ranking Output ---")
    # Candidates are returned ranked by similarity by the retriever
    for i, c in enumerate(candidates[:10]):
        area = c.get("metadata", {}).get("area", "Unknown")
        score = c.get("score", 0)
        print(f"{i+1}. {c.get('hotel_id', 'Unknown')} - Area: {area} - Score: {score}")

    print("\n--- 4. Alignment Filter Output ---")
    # Simulate Alignment Filtering logic from recommendation_service.py
    aligned_candidates = []
    # Base threshold
    threshold = 0.45
    # Relax threshold for broad queries
    broad_areas = ["delhi", "new delhi", "delhi ncr", "gurugram", "gurgaon"]
    if area and area.lower() in broad_areas:
        threshold = 0.35
        
    for c in candidates:
        score = c.get("score", 0)
        passed = score >= threshold
        c_area = c.get("metadata", {}).get("area", "Unknown")
        print(f"hotel_id: {c.get('hotel_id', 'Unknown')}, area: {c_area}, alignment_score: {score}, passed_threshold: {passed}")
        if passed:
            aligned_candidates.append(c)
    
    # Relax further if we don't have enough
    if len(aligned_candidates) < 3 and len(candidates) > 0:
        print("\nRelaxing threshold because matches < 3")
        aligned_candidates = []
        for c in candidates:
            score = c.get("score", 0)
            if score >= 0.25:
                aligned_candidates.append(c)

    print("\n--- 5. Fallback Trigger Logic ---")
    direct_match_count = len([c for c in aligned_candidates if c.get("metadata", {}).get("area") == area])
    fallback_triggered = False
    fallback_reason = "None"
    
    if direct_match_count < 3:
        fallback_triggered = True
        fallback_reason = f"Only {direct_match_count} direct matches found, which is < 3."
        
    print(f"direct_match_count: {direct_match_count}")
    print(f"fallback_triggered: {fallback_triggered}")
    print(f"fallback_reason: {fallback_reason}")

if __name__ == '__main__':
    asyncio.run(main())
