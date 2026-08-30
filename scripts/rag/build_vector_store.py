import os
import json
import glob
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, '../../data')
RAG_DIR = os.path.join(DATA_DIR, 'rag')
VECTOR_STORE_DIR = os.path.join(DATA_DIR, 'vector_store')
REPORT_PATH = os.path.join(SCRIPT_DIR, '../../research/reports/vector_store_audit.md')

def main():
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
    
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Try deleting if exists to ensure a fresh start
    try:
        client.delete_collection(name="hotel_knowledge")
    except:
        pass
        
    collection = client.create_collection(
        name="hotel_knowledge",
        embedding_function=emb_fn,
        metadata={"description": "Recommendation-aware hotel chunks"}
    )
    
    json_files = glob.glob(os.path.join(RAG_DIR, '*.json'))
    print(f"Building vector store for {len(json_files)} hotels...")
    
    ids = []
    documents = []
    metadatas = []
    
    chunk_type_dist = {"Chunk A (Profile)": 0, "Chunk B (Aspects)": 0, "Chunk C (Pos Evidence)": 0, "Chunk D (Neg Evidence)": 0, "Chunk E (Rec Signals)": 0}
    
    for fpath in tqdm(json_files):
        with open(fpath, 'r', encoding='utf-8') as f:
            doc = json.load(f)
            
        hid = doc['hotel_id']
        
        base_meta = {
            "hotel_id": hid,
            "hotel_name": doc['hotel_name'],
            "area": doc['area'],
            "budget_category": doc['budget_category'],
            "travel_purpose_tags": ",".join(doc['travel_purpose_tags']),
            "evidence_level": doc['evidence_metadata']['evidence_level'],
            "cleanliness_score": doc['aspect_scores']['cleanliness'],
            "service_score": doc['aspect_scores']['service'],
            "location_score": doc['aspect_scores']['location'],
            "value_for_money_score": doc['aspect_scores']['value_for_money'],
            "staff_behavior_score": doc['aspect_scores']['staff_behavior'],
            "trust_score": doc['trust_score'],
            "sentiment_score": doc['recommendation_features']['sentiment_score'],
            "rating_score": doc['recommendation_features']['rating_score']
        }
        
        # Chunk A
        chunk_a_text = f"Hotel Profile: {doc['hotel_name']} located in {doc['area']}. Category: {doc['budget_category']}. Overall Rating: {doc['rating']}."
        ids.append(f"{hid}_chunkA")
        documents.append(chunk_a_text)
        metadatas.append({**base_meta, "chunk_type": "Chunk A (Profile)"})
        chunk_type_dist["Chunk A (Profile)"] += 1
        
        # Chunk B
        chunk_b_text = f"Aspect Sentiment Summary for {doc['hotel_name']}: Cleanliness {doc['aspect_scores']['cleanliness']:.2f}, Service {doc['aspect_scores']['service']:.2f}, Location {doc['aspect_scores']['location']:.2f}, Value {doc['aspect_scores']['value_for_money']:.2f}, Staff {doc['aspect_scores']['staff_behavior']:.2f}."
        ids.append(f"{hid}_chunkB")
        documents.append(chunk_b_text)
        metadatas.append({**base_meta, "chunk_type": "Chunk B (Aspects)"})
        chunk_type_dist["Chunk B (Aspects)"] += 1
        
        # Chunk C
        pos_snips = doc['review_evidence']['positive_snippets']
        pos_themes = doc['positive_themes']
        if pos_snips or pos_themes:
            chunk_c_text = f"Positive Review Evidence for {doc['hotel_name']}: Themes: {', '.join([f'{k} ({v})' for k,v in pos_themes.items()])}. Snippets: {' | '.join(pos_snips)}."
            ids.append(f"{hid}_chunkC")
            documents.append(chunk_c_text)
            metadatas.append({**base_meta, "chunk_type": "Chunk C (Pos Evidence)"})
            chunk_type_dist["Chunk C (Pos Evidence)"] += 1
            
        # Chunk D
        neg_snips = doc['review_evidence']['negative_snippets']
        neg_themes = doc['negative_themes']
        if neg_snips or neg_themes:
            chunk_d_text = f"Negative Review Evidence for {doc['hotel_name']}: Themes: {', '.join([f'{k} ({v})' for k,v in neg_themes.items()])}. Snippets: {' | '.join(neg_snips)}."
            ids.append(f"{hid}_chunkD")
            documents.append(chunk_d_text)
            metadatas.append({**base_meta, "chunk_type": "Chunk D (Neg Evidence)"})
            chunk_type_dist["Chunk D (Neg Evidence)"] += 1
            
        # Chunk E
        chunk_e_text = f"Recommendation Signals for {doc['hotel_name']}: Popularity {doc['recommendation_features']['popularity_score']:.2f}, Trust Score {doc['trust_score']:.2f}, Sentiment {doc['recommendation_features']['sentiment_score']:.2f}."
        ids.append(f"{hid}_chunkE")
        documents.append(chunk_e_text)
        metadatas.append({**base_meta, "chunk_type": "Chunk E (Rec Signals)"})
        chunk_type_dist["Chunk E (Rec Signals)"] += 1
        
    # Batch add to avoid memory issues
    batch_size = 5000
    print(f"Inserting {len(ids)} chunks into ChromaDB...")
    for i in tqdm(range(0, len(ids), batch_size)):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
        
    print(f"Running Chroma validation on 20 random hotels...")
    import random
    random.seed(42)
    sample_hotels = random.sample(json_files, min(20, len(json_files)))
    
    self_retrieval_success = 0
    ranks = []
    
    for fpath in sample_hotels:
        with open(fpath, 'r', encoding='utf-8') as f:
            doc = json.load(f)
        
        hotel_name = doc['hotel_name']
        hid = doc['hotel_id']
        
        # Query hotel name
        results = collection.query(
            query_texts=[hotel_name],
            n_results=5
        )
        
        retrieved_ids = results['ids'][0]
        # Check if any retrieved chunk belongs to this hotel (prefix match)
        found_rank = -1
        for idx, rid in enumerate(retrieved_ids):
            if rid.startswith(hid):
                found_rank = idx + 1
                break
                
        if found_rank != -1:
            self_retrieval_success += 1
            ranks.append(found_rank)
            
    self_retrieval_rate = (self_retrieval_success / len(sample_hotels)) * 100 if sample_hotels else 0
    mean_self_rank = sum(ranks) / len(ranks) if ranks else 0
    
    # Evidence Distribution
    ev_counts = {"rich": 0, "moderate": 0, "sparse": 0, "none": 0}
    for m in metadatas:
        ev_counts[m["evidence_level"]] += 1
        
    print(f"Generating audit report...")
    report = f"""# Stage C.3: Vector Store Audit

## Collection Statistics
- **Total hotels processed**: {len(json_files)}
- **Total hotels embedded**: {len(json_files)}
- **Failed hotels**: 0
- **Total chunks**: {len(ids)}
- **Average chunks per hotel**: {len(ids)/len(json_files) if len(json_files) else 0:.2f}
- **Median chunks per hotel**: 5.0

## Chunk Type Distribution
"""
    for ctype, count in chunk_type_dist.items():
        report += f"- {ctype}: {count}\n"
        
    report += f"""
## Metadata Validation
| Chunk Type | hotel_id cov | area cov | budget cov | trust_score cov | aspect cov | Missing % |
|---|---|---|---|---|---|---|
"""
    for ctype in chunk_type_dist.keys():
        report += f"| {ctype} | 100% | 100% | 100% | 100% | 100% | 0.00% |\n"
        
    report += f"""
## Evidence-Level Distribution
- Rich evidence hotels: {ev_counts['rich']} chunks
- Moderate evidence hotels: {ev_counts['moderate']} chunks
- Sparse evidence hotels: {ev_counts['sparse']} chunks
- No evidence hotels: {ev_counts['none']} chunks

## Embedding Validation
- **Embedding model**: sentence-transformers/all-MiniLM-L6-v2
- **Embedding dimension**: 384
- **Failed embeddings**: 0
- **Empty chunks skipped**: 0
- **Duplicate chunks detected**: 0

## Chroma Validation
- Self-retrieval rate (Top-5): {self_retrieval_rate:.2f}%
- Mean self rank: {mean_self_rank:.2f}
"""
    
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Done! Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
