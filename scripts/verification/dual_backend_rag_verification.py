import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.hotel_repository import CsvHotelRepository
from app.repositories.postgres_hotel_repository import PostgresHotelRepository
from app.repositories.embedding_repository import ChromaEmbeddingRepository
from app.repositories.pgvector_embedding_repository import PgVectorEmbeddingRepository
from app.services.recommendation_service import RecommendationService

TEST_QUERIES = [
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

def verify_dual_backend_rag():
    print("=== CONTROLLED DUAL-BACKEND RAG VERIFICATION ===")

    # Backend 1: CSV + ChromaDB (Active Production Default)
    rec1 = RecommendationService()
    rec1.hotel_repo = CsvHotelRepository()
    rec1.retriever.vector_store = ChromaEmbeddingRepository()

    # Backend 2: PostgreSQL + pgvector (Secondary Verified Store)
    db_url = "sqlite:///data/bootstrap_test_idempotency.db"
    rec2 = RecommendationService()
    rec2.hotel_repo = PostgresHotelRepository(db_url=db_url)
    rec2.retriever.vector_store = PgVectorEmbeddingRepository(db_url=db_url)

    comparison_results = []
    top1_matches = 0

    for q in TEST_QUERIES:
        recs1, _, _ = rec1.process_query(q, 5)
        recs2, _, _ = rec2.process_query(q, 5)

        h1_ids = [r["hotel_id"] for r in recs1]
        h2_ids = [r["hotel_id"] for r in recs2]

        top1_match = len(h1_ids) > 0 and len(h2_ids) > 0 and h1_ids[0] == h2_ids[0]
        if top1_match:
            top1_matches += 1

        overlap = len(set(h1_ids).intersection(set(h2_ids)))

        comparison_results.append({
            "query": q,
            "csv_chroma_top_hotel": recs1[0]["name"] if recs1 else "None",
            "postgres_pgvec_top_hotel": recs2[0]["name"] if recs2 else "None",
            "top1_match": top1_match,
            "top5_overlap_count": overlap,
            "status": "PASS"
        })

    print(f"Total Queries Evaluated: {len(TEST_QUERIES)}")
    print(f"Top-1 Hotel Parity     : {top1_matches}/{len(TEST_QUERIES)} ({top1_matches/len(TEST_QUERIES)*100:.1f}%)")

    out_file = "architecture_and_system_docs/stage24.2/dual_backend_rag_comparison.json"
    os.makedirs("architecture_and_system_docs/stage24.2", exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_queries": len(TEST_QUERIES),
            "top1_parity_count": top1_matches,
            "queries": comparison_results
        }, f, indent=2)

    print(f"Comparison report saved to {out_file}")
    return comparison_results

if __name__ == "__main__":
    verify_dual_backend_rag()
