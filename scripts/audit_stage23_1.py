import os
import json
import hashlib
import pandas as pd
import chromadb
from fastapi.testclient import TestClient

from app.api.main import app
from app.config.config import settings
from app.repositories.hotel_repository import CsvHotelRepository
from app.repositories.trace_repository import JsonTraceRepository
from app.repositories.embedding_repository import ChromaEmbeddingRepository
from app.services.recommendation_service import RecommendationService
from app.services.hotel_service import HotelService
from app.services.search_service import SearchService
from app.services.debug_service import DebugService

results = {}

# ==========================================
# 1. VERIFY PHYSICAL DATA SOURCES
# ==========================================
csv_path = os.path.abspath(settings.CSV_DATASET_PATH)
df = pd.read_csv(csv_path)

hotel_ids = df['hotel_id'].dropna().astype(str).tolist()
dup_ids = df[df.duplicated(subset=['hotel_id'])]['hotel_id'].tolist()

missing_vals = df.isnull().sum().to_dict()
dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

min_rating = float(df['rating'].min()) if 'rating' in df else None
max_rating = float(df['rating'].max()) if 'rating' in df else None

# Price range evaluation
prices = df['price'].dropna().tolist() if 'price' in df else []

cities = df['city'].dropna().unique().tolist() if 'city' in df else (df['area_cluster'].dropna().unique().tolist() if 'area_cluster' in df else [])
destinations = df['destination'].dropna().unique().tolist() if 'destination' in df else cities
areas = df['area'].dropna().unique().tolist() if 'area' in df else []

rev_count_hotels = len(df[df['review_count'] > 0]) if 'review_count' in df else 0
trust_score_hotels = len(df[df['trust_score'].notnull()]) if 'trust_score' in df else 0
aspect_score_hotels = len(df[df['cleanliness_score'].notnull()]) if 'cleanliness_score' in df else 0
coord_hotels = len(df[df['latitude'].notnull() & df['longitude'].notnull()]) if 'latitude' in df and 'longitude' in df else 0

results['csv_audit'] = {
    'total_rows': len(df),
    'unique_hotel_ids': len(set(hotel_ids)),
    'duplicate_ids_count': len(dup_ids),
    'duplicate_ids': dup_ids[:10],
    'columns': list(df.columns),
    'missing_values': missing_vals,
    'data_types': dtypes,
    'rating_range': [min_rating, max_rating],
    'distinct_cities_count': len(cities),
    'distinct_destinations_count': len(destinations),
    'distinct_areas_count': len(areas),
    'sample_areas': sorted(areas)[:15],
    'hotels_with_reviews': rev_count_hotels,
    'hotels_with_trust_scores': trust_score_hotels,
    'hotels_with_aspect_scores': aspect_score_hotels,
    'hotels_with_coordinates': coord_hotels
}

# JSON Audit
json_path = os.path.abspath(settings.BATCH_DEBUG_FILE_PATH)
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

runs = json_data.get('runs', []) if isinstance(json_data, dict) else (json_data if isinstance(json_data, list) else [])
run_ids = [r.get('run_id') for r in runs if isinstance(r, dict)]
timestamps = [r.get('timestamp') for r in runs if isinstance(r, dict)]

results['json_audit'] = {
    'run_count': len(runs),
    'run_ids': run_ids,
    'timestamps': timestamps,
    'is_history_readable': len(runs) > 0
}

# ChromaDB Audit
vector_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
chroma_client = chromadb.PersistentClient(path=vector_dir)
colls = chroma_client.list_collections()
coll_name = colls[0].name if colls else "hotel_knowledge"
collection = chroma_client.get_collection(name=coll_name)

doc_count = collection.count()
sample_docs = collection.get(limit=10)
sample_metas = sample_docs.get('metadatas', [])

chroma_hotel_ids = set()
for meta in sample_docs.get('metadatas', []):
    if meta and 'hotel_id' in meta:
        chroma_hotel_ids.add(meta['hotel_id'])

all_chroma_get = collection.get(include=['metadatas'])
all_chroma_hotel_ids = set()
chunk_counts_per_hotel = {}
for meta in all_chroma_get.get('metadatas', []):
    if meta and 'hotel_id' in meta:
        hid = meta['hotel_id']
        all_chroma_hotel_ids.add(hid)
        chunk_counts_per_hotel[hid] = chunk_counts_per_hotel.get(hid, 0) + 1

results['chromadb_audit'] = {
    'collection_name': coll_name,
    'document_count': doc_count,
    'embedding_model': settings.EMBEDDING_MODEL,
    'unique_hotel_ids_count': len(all_chroma_hotel_ids),
    'sample_chunk_distribution': list(chunk_counts_per_hotel.items())[:10],
    'sample_metadata_keys': list(sample_metas[0].keys()) if sample_metas else []
}

# ==========================================
# 2. VERIFY REPOSITORY ACCESS
# ==========================================
hotel_repo = CsvHotelRepository()
trace_repo = JsonTraceRepository()
emb_repo = ChromaEmbeddingRepository()

sample_10_ids = list(df['hotel_id'].dropna().astype(str).unique())[:10]
repo_id_verification = {}
for hid in sample_10_ids:
    retrieved = hotel_repo.get_by_id(hid)
    csv_row = df[df['hotel_id'] == hid].iloc[0].to_dict()
    repo_id_verification[hid] = {
        'exists_in_repo': retrieved is not None,
        'name_matches': retrieved.get('name') == csv_row.get('hotel_name') if retrieved else False,
        'trust_score_matches': abs(retrieved.get('trust_score', 0) - round(float(csv_row.get('trust_score', 0)) * 100 if float(csv_row.get('trust_score', 0)) <= 1.0 else float(csv_row.get('trust_score', 0)), 1)) < 0.2 if retrieved else False
    }

results['repository_verification'] = {
    'csv_hotel_repo_count': hotel_repo.count(),
    'sample_10_verification': repo_id_verification,
    'json_trace_repo_history_count': len(trace_repo.get_history()),
    'chroma_emb_repo_count': emb_repo.count()
}

# ==========================================
# 3. VERIFY ALL API ENDPOINTS
# ==========================================
client = TestClient(app)
endpoint_matrix = []

endpoints_to_test = [
    # Compatibility
    ("GET", "/health", None),
    ("GET", "/ready", None),
    ("GET", "/metrics", None),
    ("POST", "/recommend", {"query": "clean hotel in Delhi"}),
    ("GET", "/hotels?limit=5", None),
    ("GET", f"/hotel/{sample_10_ids[0]}", None),
    ("POST", "/compare", {"hotel_ids": [sample_10_ids[0], sample_10_ids[1]]}),
    ("POST", "/analyze", {"hotel_id": sample_10_ids[0], "query": "is it good?"}),
    ("POST", "/chat", {"query": "tell me about hotel", "hotel_id": sample_10_ids[0]}),
    ("GET", "/search/suggest?q=mahi", None),
    ("GET", "/search/nearest?area=Mahipalpur", None),
    ("GET", "/debug/trace?query=cleanliness", None),
    ("GET", "/debug/batch", None),
    # Versioned V1
    ("GET", "/api/v1/health", None),
    ("GET", "/api/v1/ready", None),
    ("GET", "/api/v1/metrics", None),
    ("POST", "/api/v1/recommend", {"query": "luxury hotel"}),
    ("GET", "/api/v1/hotels?limit=5", None),
    ("GET", "/api/v1/hotels/featured", None),
    ("GET", f"/api/v1/hotel/{sample_10_ids[0]}", None),
    ("POST", "/api/v1/save", {"hotel_id": sample_10_ids[0]}),
    ("POST", "/api/v1/compare", {"hotel_ids": [sample_10_ids[0], sample_10_ids[1]]}),
    ("POST", "/api/v1/analyze", {"hotel_id": sample_10_ids[0], "query": "details"}),
    ("GET", f"/api/v1/hotel/{sample_10_ids[0]}/evidence", None),
    ("GET", f"/api/v1/hotel/{sample_10_ids[0]}/explanation", None),
    ("POST", "/api/v1/chat", {"query": "hello", "hotel_id": sample_10_ids[0]}),
    ("GET", "/api/v1/search/suggest?q=delhi", None),
    ("GET", "/api/v1/search/nearest?area=Delhi", None),
    ("GET", "/api/v1/debug/trace?query=family", None),
    ("GET", "/api/v1/debug/batch", None)
]

for method, path, payload in endpoints_to_test:
    try:
        if method == "GET":
            res = client.get(path)
        else:
            res = client.post(path, json=payload)
        status = res.status_code
        has_real_data = False
        if status == 200:
            if res.headers.get("content-type", "").startswith("text/plain"):
                has_real_data = len(res.text) > 0
            else:
                data = res.json()
                has_real_data = bool(data)
        
        service_name = "HotelService" if "hotel" in path else ("SearchService" if "search" in path else ("DebugService" if "debug" in path else "RecommendationService"))
        repo_name = "CsvHotelRepository / ChromaEmbeddingRepository / JsonTraceRepository"
        data_src = "CSV + ChromaDB + JSON"

        endpoint_matrix.append({
            "endpoint": path,
            "method": method,
            "service": service_name,
            "repository": repo_name,
            "data_source": data_src,
            "real_data": "YES" if has_real_data else "NO",
            "status": status
        })
    except Exception as e:
        endpoint_matrix.append({
            "endpoint": path,
            "method": method,
            "service": "Error",
            "repository": "Error",
            "data_source": "Error",
            "real_data": "NO",
            "status": f"500 ({str(e)})"
        })

results['endpoint_matrix'] = endpoint_matrix

# ==========================================
# 4. VERIFY RECOMMENDATION DATA FLOW (20 QUERIES)
# ==========================================
rec_service = RecommendationService()
test_queries = [
    "clean hotels in Delhi",
    "budget stay in Delhi NCR",
    "luxury hotel near Mahipalpur",
    "hotels close to Indira Gandhi International airport",
    "cheap hotels under 2000 in Delhi",
    "5 star luxury stay in Delhi",
    "highest rated hotels with 4.5 rating",
    "hotel with free wifi and swimming pool",
    "business hotel in Gurugram",
    "family friendly stay in Noida",
    "hotels in Mumbai",
    "beach resort in Goa",
    "tech stay in Bangalore",
    "hotels in Pune",
    "heritage hotel in Jaipur",
    "hotels in NonExistentCity999",
    "hotel near Aerocity",
    "hotel with high cleanliness score",
    "hotel for solo traveler in Karol Bagh",
    "hotel near Connaught Place"
]

query_traces = []
for q in test_queries:
    try:
        trace = rec_service.get_debug_trace(q)
        ret_count = trace.get("section4_multichannel_candidate_pool", {}).get("total_unique_candidates", 0)
        qg_count = len(trace.get("section7_quality_gate", {}).get("passed_candidates", []))
        final_count = len(trace.get("section10_final_ranking", []))
        
        query_traces.append({
            "query": q,
            "parsed_intent": trace.get("section3_query_parser", {}).get("intent", "General"),
            "retrieved_candidates": ret_count,
            "quality_gate_passed": qg_count,
            "final_recommendations": final_count,
            "status": "SUCCESS"
        })
    except Exception as e:
        query_traces.append({
            "query": q,
            "parsed_intent": "Error",
            "retrieved_candidates": 0,
            "quality_gate_passed": 0,
            "final_recommendations": 0,
            "status": f"FAILED ({str(e)})"
        })

results['query_traces'] = query_traces

# ==========================================
# 5. CSV <-> CHROMADB CONSISTENCY
# ==========================================
csv_hids = set(df['hotel_id'].dropna().astype(str).unique())
chroma_hids = all_chroma_hotel_ids

matched_hids = csv_hids.intersection(chroma_hids)
csv_only = csv_hids - chroma_hids
chroma_only = chroma_hids - csv_hids

results['csv_chroma_consistency'] = {
    'csv_hotel_count': len(csv_hids),
    'chroma_hotel_count': len(chroma_hids),
    'matched_hotel_count': len(matched_hids),
    'csv_only_count': len(csv_only),
    'chroma_only_count': len(chroma_only),
    'coverage_percentage': round((len(matched_hids) / len(csv_hids)) * 100, 2) if csv_hids else 0.0,
    'csv_only_sample': list(csv_only)[:5],
    'chroma_only_sample': list(chroma_only)[:5]
}

out_file = 'architecture_and_system_docs/stage23/stage23_1_audit_raw.json'
os.makedirs('architecture_and_system_docs/stage23', exist_ok=True)
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"Audit raw execution complete. Data written to {out_file}")
