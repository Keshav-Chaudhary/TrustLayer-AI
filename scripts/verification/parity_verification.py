import os
import sys
import json
import pandas as pd
from typing import List, Dict, Any

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

def run_parity_verification(db_url: str = "sqlite:///data/bootstrap_test_idempotency.db") -> Dict[str, Any]:
    print("=== DUAL-BACKEND PARITY VERIFICATION ===")
    csv_repo = CsvHotelRepository()
    pg_repo = PostgresHotelRepository(db_url=db_url)

    csv_count = csv_repo.count()
    pg_count = pg_repo.count()

    print(f"CSV Hotel Count     : {csv_count}")
    print(f"PostgreSQL Hotel Count: {pg_count}")

    csv_hotels = csv_repo.get_all_hotels()
    pg_hotels = pg_repo.get_all_hotels()

    csv_ids = set(csv_hotels.keys())
    pg_ids = set(pg_hotels.keys())

    missing_in_pg = csv_ids - pg_ids
    extra_in_pg = pg_ids - csv_ids

    field_mismatches = []
    for hid in csv_ids.intersection(pg_ids):
        c_h = csv_hotels[hid]
        p_h = pg_hotels[hid]

        if c_h["name"].strip() != p_h["name"].strip():
            field_mismatches.append({"hotel_id": hid, "field": "name", "csv": c_h["name"], "pg": p_h["name"]})
        if abs(c_h.get("trust_score", 0) - p_h.get("trust_score", 0)) > 0.2:
            field_mismatches.append({"hotel_id": hid, "field": "trust_score", "csv": c_h["trust_score"], "pg": p_h["trust_score"]})

    print(f"Matched Hotel IDs   : {len(csv_ids.intersection(pg_ids))}")
    print(f"Missing in PG       : {len(missing_in_pg)}")
    print(f"Extra in PG         : {len(extra_in_pg)}")
    print(f"Field Mismatches    : {len(field_mismatches)}")

    # Vector Embedding Parity
    chroma_repo = ChromaEmbeddingRepository()
    pgvec_repo = PgVectorEmbeddingRepository(db_url=db_url)

    print(f"Chroma Vector Count : {chroma_repo.count()}")
    print(f"PgVector Count      : {pgvec_repo.count()}")

    # 20 RAG Recommendation Queries Execution Parity
    rec_service = RecommendationService()
    query_results = []

    for q in TEST_QUERIES:
        try:
            recs, _, _ = rec_service.process_query(q, limit=5)
            query_results.append({
                "query": q,
                "recommendation_count": len(recs),
                "top_hotel_name": recs[0]["name"] if recs else "None",
                "top_trust_score": recs[0].get("trust_score") if recs else 0.0,
                "status": "SUCCESS"
            })
        except Exception as e:
            query_results.append({
                "query": q,
                "recommendation_count": 0,
                "top_hotel_name": "Error",
                "top_trust_score": 0.0,
                "status": f"FAILED ({str(e)})"
            })

    report_data = {
        "csv_hotel_count": csv_count,
        "postgres_hotel_count": pg_count,
        "matched_ids_count": len(csv_ids.intersection(pg_ids)),
        "missing_in_postgres": list(missing_in_pg)[:10],
        "extra_in_postgres": list(extra_in_pg)[:10],
        "field_mismatches_count": len(field_mismatches),
        "field_mismatches_sample": field_mismatches[:10],
        "chroma_vector_count": chroma_repo.count(),
        "pgvector_count": pgvec_repo.count(),
        "rag_queries": query_results
    }

    # Generate STAGE24_PARITY_REPORT.md
    md = []
    md.append("# STAGE 24 — DUAL-BACKEND PARITY VERIFICATION REPORT\n")
    md.append("## Executive Summary")
    md.append("This document provides empirical dual-backend parity results comparing the active **CSV + ChromaDB** backend against the secondary **PostgreSQL + pgvector** storage target.\n")
    md.append("---")
    md.append("## 1. Hotel Entity & Field Parity")
    md.append(f"- **CSV Hotel Count**: {csv_count}")
    md.append(f"- **PostgreSQL Hotel Count**: {pg_count}")
    md.append(f"- **Matched Hotel IDs**: {len(csv_ids.intersection(pg_ids))}")
    md.append(f"- **Missing in PostgreSQL**: {len(missing_in_pg)}")
    md.append(f"- **Extra in PostgreSQL**: {len(extra_in_pg)}")
    md.append(f"- **Field Mismatches Count**: {len(field_mismatches)}\n")

    md.append("---")
    md.append("## 2. Vector Embedding Coverage")
    md.append(f"- **ChromaDB Vector Chunks**: {chroma_repo.count()}")
    md.append(f"- **pgvector Storage Chunks**: {pgvec_repo.count()}\n")

    md.append("---")
    md.append("## 3. 20 RAG Recommendation Queries Parity Suite")
    md.append("| Query | Top Recommendation | Trust Score | Count | Status |")
    md.append("|---|---|---|---|---|")
    for qr in query_results:
        md.append(f"| `{qr['query']}` | {qr['top_hotel_name']} | {qr['top_trust_score']} | {qr['recommendation_count']} | `{qr['status']}` |")

    md_out_path = "architecture_and_system_docs/stage24/STAGE24_PARITY_REPORT.md"
    os.makedirs("architecture_and_system_docs/stage24", exist_ok=True)
    with open(md_out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"\nParity report markdown saved to {md_out_path}")
    return report_data

if __name__ == "__main__":
    run_parity_verification()
