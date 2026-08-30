import os
import sys
import json
import psycopg2
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.config import settings
from app.repositories.factory import get_hotel_repository, get_embedding_repository, get_trace_repository
from app.api.main import app

PG_URL = settings.DATABASE_URL
report = {}

# ----------------------------------------------------
# PHASE 14 — DIRECT SIMILARITY QUERY AGAINST POSTGRESQL
# ----------------------------------------------------
print("=== PHASE 14: DIRECT POSTGRESQL SIMILARITY QUERY ===")
emb_repo = get_embedding_repository()
search_res = emb_repo.query_vectors("clean hotel in Delhi", 3)

ids = search_res.get("ids", [[]])[0]
docs = search_res.get("documents", [[]])[0]
metas = search_res.get("metadatas", [[]])[0]
dists = search_res.get("distances", [[]])[0]

print(f"Direct Similarity Query Returned {len(ids)} matches from PostgreSQL.")
for idx, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists)):
    print(f"  Rank {idx+1}: Chunk ID={cid}, Similarity={round(1.0-dist, 4)}, Snippet Length={len(doc)}")

report["phase14_matches"] = len(ids)

# ----------------------------------------------------
# PHASE 15 & 17 — FACTORY RESOLUTION & CONFIG CHECK
# ----------------------------------------------------
print("\n=== PHASE 15 & 17: REPOSITORY FACTORY RESOLUTION & CONFIG ===")
h_repo = get_hotel_repository()
e_repo = get_embedding_repository()
t_repo = get_trace_repository()

print("DATA_BACKEND =", settings.DATA_BACKEND)
print("VECTOR_BACKEND =", settings.VECTOR_BACKEND)
print("DATABASE_URL configured =", bool(settings.DATABASE_URL))
print("Instantiated Hotel Repository :", h_repo.__class__.__name__)
print("Instantiated Embedding Repo   :", e_repo.__class__.__name__)

report["phase15_h_repo"] = h_repo.__class__.__name__
report["phase15_e_repo"] = e_repo.__class__.__name__

# ----------------------------------------------------
# PHASE 16 — LIVE API BACKEND VERIFICATION
# ----------------------------------------------------
print("\n=== PHASE 16: API BACKEND VERIFICATION ===")
client = TestClient(app)

res_ready = client.get("/ready")
print("/ready status:", res_ready.status_code, res_ready.json())

res_hotels = client.get("/api/v1/hotels?limit=5")
print("/api/v1/hotels status:", res_hotels.status_code, "Returned Count:", len(res_hotels.json().get("hotels", [])))

sampled_h = res_hotels.json().get("hotels", [])[0]
sample_hid = sampled_h.get("hotel_id")

# Verify in PostgreSQL
conn = psycopg2.connect(PG_URL)
cur = conn.cursor()
cur.execute("SELECT hotel_id, name, rating FROM hotels WHERE hotel_id = %s;", (sample_hid,))
db_row = cur.fetchone()
conn.close()

print(f"API Returned Hotel ID: {sample_hid} ('{sampled_h.get('name')}')")
print(f"PostgreSQL Database Row: ID={db_row[0]}, Name='{db_row[1]}', Rating={db_row[2]}")

report["phase16_api_ready"] = res_ready.status_code == 200
report["phase16_api_matched"] = db_row is not None and db_row[0] == sample_hid

with open("architecture_and_system_docs/stage24/stage24_4_phase14_17_raw.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("\nPhase 14 to 17 completed successfully.")
