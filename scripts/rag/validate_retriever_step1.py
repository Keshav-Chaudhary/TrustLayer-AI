import os
import sys
import time
import json
import statistics

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from scripts.rag.retriever import HybridRetriever

def main():
    SCRIPT_DIR = os.path.dirname(__file__)
    VECTOR_STORE_DIR = os.path.join(SCRIPT_DIR, '../../data/vector_store')
    REPORT_PATH = os.path.join(SCRIPT_DIR, '../../research/reports/retriever_validation.md')
    
    retriever = HybridRetriever(VECTOR_STORE_DIR)
    
    queries = [
        {"q": "luxury family hotels in Delhi", "hard": {}, "soft": {"travel_purpose": "family", "budget_category": "luxury"}},
        {"q": "cheap hotels with great service in Mahipalpur", "hard": {"area": "Mahipalpur"}, "soft": {"budget_category": "budget"}},
        {"q": "business hotels", "hard": {}, "soft": {"travel_purpose": "business"}},
        {"q": "best cleanliness", "hard": {}, "soft": {}},
        {"q": "hotels in Loni", "hard": {"area": "Loni"}, "soft": {}}
    ]
    
    latencies = []
    cands_before = []
    cands_after = []
    
    all_semantic_scores = []
    all_metadata_scores = []
    all_rec_scores = []
    all_final_scores = []
    
    top10_example = None
    
    for i, q in enumerate(queries):
        start_time = time.time()
        
        top_k = 10
        fetch_k = top_k * 5
        
        results = retriever.retrieve(query=q["q"], hard_constraints=q["hard"], soft_constraints=q["soft"], top_k=top_k)
        
        latency = (time.time() - start_time) * 1000 # ms
        latencies.append(latency)
        
        cands_before.append(fetch_k)
        
        for res in results:
            dbg = res['debug_info']
            all_semantic_scores.append(dbg['semantic_score'])
            all_metadata_scores.append(dbg['metadata_score'])
            all_rec_scores.append(dbg['recommendation_score'])
            all_final_scores.append(dbg['final_score'])
            
        # grab the first query that returned results
        if not top10_example and len(results) > 0:
            top10_example = {
                "query": q,
                "results": results
            }
            
    avg_latency = statistics.mean(latencies)
    
    report = f"""# Step 1: Retriever Validation

## Performance
- **Average Retrieval Latency**: {avg_latency:.2f} ms
- **Candidates before filtering**: 50 (fetch_k = 10 * 5)
- **Candidates after filtering**: Varies based on hard constraints (returns up to 10 after ranking)

## Score Distributions
- **Semantic Score**: min={min(all_semantic_scores):.2f}, max={max(all_semantic_scores):.2f}, avg={statistics.mean(all_semantic_scores):.2f}
- **Metadata Score**: min={min(all_metadata_scores):.2f}, max={max(all_metadata_scores):.2f}, avg={statistics.mean(all_metadata_scores):.2f}
- **Recommendation Score**: min={min(all_rec_scores):.2f}, max={max(all_rec_scores):.2f}, avg={statistics.mean(all_rec_scores):.2f}
- **Final Score**: min={min(all_final_scores):.2f}, max={max(all_final_scores):.2f}, avg={statistics.mean(all_final_scores):.2f}

## Edge Cases Handled
- **Empty Constraints**: Gracefully handles missing hard/soft constraints (defaults to empty dicts).
- **No Semantic Spread**: The `1e-9` in `max_dist - min_dist + 1e-9` prevents division by zero when all semantic distances are identical.
- **Normalization Boundaries**: Min-max normalization strictly forces the highest ranked semantic chunk to 1.0 and lowest to 0.0 per query batch.

## Top-10 Example: Score Decomposition
**Query**: `{top10_example['query']['q']}`
**Hard Constraints**: `{top10_example['query']['hard']}`
**Soft Constraints**: `{top10_example['query']['soft']}`

| Rank | Hotel/Chunk ID | Semantic (0.6) | Metadata (0.2) | Rec Score (0.2) | Final Score |
|---|---|---|---|---|---|
"""
    for res in top10_example['results']:
        dbg = res['debug_info']
        report += f"| {dbg['rerank_position']} | {res['id']} | {dbg['semantic_score']:.3f} | {dbg['metadata_score']:.3f} | {dbg['recommendation_score']:.3f} | **{dbg['final_score']:.3f}** |\n"
        
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Validation report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
