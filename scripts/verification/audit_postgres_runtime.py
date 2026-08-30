import os
import sys
import json
import psycopg2
from typing import Dict, Any
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.factory import get_hotel_repository, get_embedding_repository, get_trace_repository
from app.api.main import app

def run_runtime_audit() -> Dict[str, Any]:
    db_url = settings.DATABASE_URL
    assert db_url and "postgresql" in db_url, "DATABASE_URL must be configured for PostgreSQL"

    audit = {}

    # 1. DATABASE & SERVER DETAILS
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port(), version();")
    db, user, addr, port, ver = cur.fetchone()

    audit["database"] = db
    audit["server"] = f"{addr or 'localhost'}:{port or 5432}"
    audit["backend"] = settings.DATA_BACKEND
    audit["vector_backend"] = settings.VECTOR_BACKEND
    audit["postgres_version"] = ver

    # 2. TABLE ROW COUNTS & INTEGRITY
    table_names = ["hotels", "hotel_locations", "hotel_scores", "hotel_sources", "hotel_amenities", "hotel_provenance", "embedding_documents", "domain_events", "ingestion_records", "ingestion_runs"]
    row_counts = {}
    for t in table_names:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        row_counts[t] = cur.fetchone()[0]
    audit["row_counts"] = row_counts

    # Orphans
    cur.execute("SELECT COUNT(*) FROM hotel_locations l LEFT JOIN hotels h ON h.hotel_id = l.hotel_id WHERE h.hotel_id IS NULL;")
    orphan_locs = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hotel_scores s LEFT JOIN hotels h ON h.hotel_id = s.hotel_id WHERE h.hotel_id IS NULL;")
    orphan_scores = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hotel_sources src LEFT JOIN hotels h ON h.hotel_id = src.hotel_id WHERE h.hotel_id IS NULL;")
    orphan_sources = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hotel_amenities a LEFT JOIN hotels h ON h.hotel_id = a.hotel_id WHERE h.hotel_id IS NULL;")
    orphan_amenities = cur.fetchone()[0]

    audit["orphans"] = {
        "locations": orphan_locs,
        "scores": orphan_scores,
        "sources": orphan_sources,
        "amenities": orphan_amenities
    }

    # Duplicates
    cur.execute("SELECT hotel_id, COUNT(*) FROM hotels GROUP BY hotel_id HAVING COUNT(*) > 1;")
    dup_hotels = cur.fetchall()

    cur.execute("SELECT chunk_id, COUNT(*) FROM embedding_documents GROUP BY chunk_id HAVING COUNT(*) > 1;")
    dup_chunks = cur.fetchall()

    audit["duplicates"] = {
        "hotels": len(dup_hotels),
        "chunks": len(dup_chunks)
    }

    # Vector Integrity
    cur.execute("SELECT COUNT(*) FROM embedding_documents WHERE embedding_vector IS NULL;")
    null_vecs = cur.fetchone()[0]

    cur.execute("SELECT column_name, data_type, udt_name FROM information_schema.columns WHERE table_name = 'embedding_documents' AND column_name = 'embedding_vector';")
    col_info = cur.fetchone()

    audit["vector_integrity"] = {
        "total_vectors": row_counts.get("embedding_documents", 0),
        "null_vectors": null_vecs,
        "column_datatype": col_info[1] if col_info else "unknown",
        "column_udt_name": col_info[2] if col_info else "unknown",
        "is_native_pgvector": (col_info[2] == "vector") if col_info else False
    }

    # 3. REPOSITORY RESOLUTION
    h_repo = get_hotel_repository()
    e_repo = get_embedding_repository()
    t_repo = get_trace_repository()

    audit["repository_resolution"] = {
        "hotel_repository": h_repo.__class__.__name__,
        "embedding_repository": e_repo.__class__.__name__,
        "trace_repository": t_repo.__class__.__name__,
        "hotel_repo_target_db": getattr(h_repo, "db_url", "").split("@")[-1]
    }

    # 4. API PROVENANCE
    client = TestClient(app)
    res = client.get("/api/v1/hotels?limit=5")
    api_hotels = res.json().get("hotels", [])
    
    matched = 0
    for h in api_hotels:
        hid = h["hotel_id"]
        cur.execute("SELECT name, rating FROM hotels WHERE hotel_id = %s;", (hid,))
        row = cur.fetchone()
        if row and row[0] == h["name"]:
            matched += 1

    audit["api_provenance"] = {
        "api_returned_count": len(api_hotels),
        "postgres_matched_count": matched,
        "provenance_verified": matched == len(api_hotels) and len(api_hotels) > 0
    }

    # 5. LEGACY DETACHMENT STATUS
    audit["legacy_dependency_checks"] = {
        "csv_source_bypassed": settings.DATA_BACKEND == "postgres",
        "chroma_source_bypassed": settings.VECTOR_BACKEND == "pgvector",
        "sqlite_bypassed": "postgresql" in str(settings.DATABASE_URL)
    }

    conn.close()

    overall_pass = (
        audit["database"] == "trustlayer_db" and
        row_counts.get("hotels") == 1661 and
        row_counts.get("embedding_documents") == 7910 and
        orphan_locs == 0 and
        audit["duplicates"]["hotels"] == 0 and
        audit["api_provenance"]["provenance_verified"]
    )

    audit["overall_status"] = "PASS" if overall_pass else "FAIL"

    out_file = "stage24_5_backend_audit.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    print(f"PostgreSQL Runtime Audit saved to {out_file}")
    return audit

if __name__ == "__main__":
    run_runtime_audit()
