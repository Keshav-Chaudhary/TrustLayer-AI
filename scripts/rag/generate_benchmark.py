import json
import os
import random

def main():
    random.seed(42)
    
    # We need 25 queries for each of the 6 categories (Total = 150)
    # Area, Budget, Aspect, Review, Recommendation, Multi
    
    # We also need to define Oracle answers (expected metadata/hotels) for evaluation
    # To do this robustly without looking at the full DB, we'll just specify the EXPECTED constraint parsing for the oracle evaluation
    
    queries = []
    
    # 1. Area Queries (25)
    areas = ["Mahipalpur", "Karol Bagh", "Loni", "Delhi NCR", "Gurugram", "Noida"]
    for i in range(25):
        area = areas[i % len(areas)]
        queries.append({
            "category": "Area",
            "query": f"hotels in {area}",
            "expected_constraints": {"hard": {"area": area}, "soft": {}},
            "expected_chunk_types": ["Chunk A (Profile)"]
        })
        
    # 2. Budget Queries (25)
    budgets = ["budget", "cheap", "mid-range", "luxury", "expensive"]
    for i in range(25):
        b = budgets[i % len(budgets)]
        mapped_b = "budget" if b == "cheap" else "luxury" if b == "expensive" else b
        queries.append({
            "category": "Budget",
            "query": f"strictly {b} hotels",
            "expected_constraints": {"hard": {"budget_category": mapped_b}, "soft": {}},
            "expected_chunk_types": ["Chunk A (Profile)", "Chunk B (Aspects)"]
        })
        
    # 3. Aspect Queries (25)
    aspects = ["cleanliness", "service", "location", "value", "staff", "food", "wifi", "pool", "view", "parking"]
    for i in range(25):
        a = aspects[i % len(aspects)]
        queries.append({
            "category": "Aspect",
            "query": f"hotels with best {a}",
            "expected_constraints": {"hard": {}, "soft": {"aspects": a}},
            "expected_chunk_types": ["Chunk B (Aspects)"]
        })
        
    # 4. Review-Evidence Queries (25)
    review_terms = [
        ("complaints about cleanliness", "cleanliness", "Chunk D (Neg Evidence)"),
        ("guests mention food quality", "food", "Chunk C (Pos Evidence)"),
        ("recurring issues with wifi", "wifi", "Chunk D (Neg Evidence)"),
        ("praise for staff", "staff", "Chunk C (Pos Evidence)"),
        ("bad location", "location", "Chunk D (Neg Evidence)")
    ]
    for i in range(25):
        term, aspect, ctype = review_terms[i % len(review_terms)]
        queries.append({
            "category": "Review",
            "query": term,
            "expected_constraints": {"hard": {}, "soft": {"aspects": aspect}},
            "expected_chunk_types": [ctype, "Chunk B (Aspects)"]
        })
        
    # 5. Recommendation-Aware Queries (25)
    rec_terms = [
        "why was this hotel recommended",
        "explain this recommendation",
        "strengths and weaknesses",
        "why should I trust this hotel",
        "what makes this hotel popular"
    ]
    for i in range(25):
        term = rec_terms[i % len(rec_terms)]
        queries.append({
            "category": "Recommendation",
            "query": term,
            "expected_constraints": {"hard": {}, "soft": {}},
            "expected_chunk_types": ["Chunk E (Rec Signals)", "Chunk A (Profile)"]
        })
        
    # 6. Multi-Constraint Queries (25)
    for i in range(25):
        area = areas[i % len(areas)]
        b = budgets[i % len(budgets)]
        mapped_b = "budget" if b == "cheap" else "luxury" if b == "expensive" else b
        a = aspects[i % len(aspects)]
        
        queries.append({
            "category": "Multi",
            "query": f"strictly {b} family hotels in {area} with good {a}",
            "expected_constraints": {
                "hard": {"area": area, "budget_category": mapped_b}, 
                "soft": {"travel_purpose": "family", "aspects": a}
            },
            "expected_chunk_types": ["Chunk A (Profile)", "Chunk B (Aspects)"]
        })
        
    # Introduce evidence level balance: since we can't control the DB here, we assume 
    # queries are general enough to hit various evidence levels.
    # The evaluation script will track the Evidence-Level Bias Audit to prove balance.

    # Save
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../research/evaluation'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'retrieval_queries.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2)
        
    print(f"Generated 150 benchmark queries at {out_path}")

if __name__ == "__main__":
    main()
