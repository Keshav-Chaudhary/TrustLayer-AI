import os
import json
import glob
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
RAG_DIR = os.path.join(DATA_DIR, 'rag')
REPORT_PATH = os.path.join(SCRIPT_DIR, '../../research/reports/hotel_document_audit.md')

def main():
    print(f"Auditing JSON documents in {RAG_DIR}...")
    json_files = glob.glob(os.path.join(RAG_DIR, '*.json'))
    
    total_hotels = len(json_files)
    missing_reviews = 0
    missing_aspects = 0
    theme_coverage_count = 0
    
    # We will simulate chunk estimation based on the content
    # Chunk A: Profile (1)
    # Chunk B: Aspect summary (1)
    # Chunk C: Positive review evidence (1 if positive themes/snippets exist)
    # Chunk D: Negative review evidence (1 if negative themes/snippets exist)
    # Chunk E: Recommendation features (1)
    
    total_chunks = 0
    chunk_lengths = []
    
    for fpath in json_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            
        # Check reviews
        pos_snips = doc['review_evidence']['positive_snippets']
        neg_snips = doc['review_evidence']['negative_snippets']
        if len(pos_snips) == 0 and len(neg_snips) == 0:
            missing_reviews += 1
            
        # Check aspects
        aspects = doc['aspect_scores']
        if all(v == 0.5 for v in aspects.values()):
            # If all are exactly 0.5, we might consider them missing/default
            missing_aspects += 1
            
        # Check themes
        pos_themes = doc['positive_themes']
        neg_themes = doc['negative_themes']
        if pos_themes or neg_themes:
            theme_coverage_count += 1
            
        # Estimate chunks
        # Chunk A
        total_chunks += 1
        chunk_lengths.append(len(str(doc['hotel_name']) + str(doc['area']) + str(doc['budget_category'])))
        
        # Chunk B
        total_chunks += 1
        chunk_lengths.append(len(str(aspects)))
        
        # Chunk C
        if pos_snips or pos_themes:
            total_chunks += 1
            chunk_lengths.append(len(str(pos_snips) + str(pos_themes)))
            
        # Chunk D
        if neg_snips or neg_themes:
            total_chunks += 1
            chunk_lengths.append(len(str(neg_snips) + str(neg_themes)))
            
        # Chunk E
        total_chunks += 1
        chunk_lengths.append(len(str(doc['recommendation_features'])))
        
    avg_chunks = total_chunks / total_hotels if total_hotels > 0 else 0
    avg_chunk_len = np.mean(chunk_lengths) if chunk_lengths else 0
    theme_coverage = (theme_coverage_count / total_hotels) * 100 if total_hotels > 0 else 0
    
    report = f"""# Stage C: Hotel Document Audit Report

## Knowledge Base Construction Audit

- **Total Hotels Processed**: {total_hotels}
- **Hotels Missing Reviews**: {missing_reviews} ({(missing_reviews/total_hotels*100) if total_hotels else 0:.2f}%)
- **Hotels with Default/Missing Aspect Scores**: {missing_aspects} ({(missing_aspects/total_hotels*100) if total_hotels else 0:.2f}%)

## Semantic Chunking Projections

- **Average Chunks per Hotel**: {avg_chunks:.2f}
- **Average Chunk Length (characters)**: {avg_chunk_len:.0f}
- **Theme Extraction Coverage**: {theme_coverage:.2f}% of hotels successfully extracted structured positive/negative themes.

## Conclusion
This audit verifies the data readiness before building the ChromaDB Vector Store.
"""
    
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Audit report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
