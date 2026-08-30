import os
import sys
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.config import settings
from app.repositories.db_schema import Base, HotelModel, EmbeddingDocumentModel
from scripts.ingestion.bootstrap_postgres import run_bootstrap
from scripts.ingestion.backfill_pgvector import run_pgvector_backfill

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "postgres"
PG_PASS = "postgres"
TARGET_DB = "trustlayer_db"
TARGET_URL = f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{TARGET_DB}"

report_data = {}

# ----------------------------------------------------
# PHASE 2 — CREATE DATABASE
# ----------------------------------------------------
print("=== PHASE 2: CREATING DATABASE ===")
conn = psycopg2.connect(dbname="postgres", user=PG_USER, password=PG_PASS, host=PG_HOST, port=PG_PORT)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute("SELECT datname FROM pg_database WHERE datname = %s;", (TARGET_DB,))
if not cur.fetchone():
    cur.execute(f"CREATE DATABASE {TARGET_DB};")
    print(f"Created database '{TARGET_DB}' successfully!")
else:
    print(f"Database '{TARGET_DB}' already exists.")

conn.close()

# ----------------------------------------------------
# PHASE 3 — CHECK PGVECTOR EXTENSION
# ----------------------------------------------------
print("\n=== PHASE 3: CHECKING PGVECTOR EXTENSION ===")
target_conn = psycopg2.connect(dbname=TARGET_DB, user=PG_USER, password=PG_PASS, host=PG_HOST, port=PG_PORT)
target_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
t_cur = target_conn.cursor()

t_cur.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name = 'vector';")
available_vec = t_cur.fetchall()
report_data["phase3_pgvector_available"] = len(available_vec) > 0

pgvector_installed = False
if available_vec:
    try:
        t_cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        pgvector_installed = True
        print("Created extension 'vector' in trustlayer_db!")
    except Exception as ex:
        print("Failed to enable vector extension:", str(ex))
else:
    print("pgvector extension binary is NOT available in this PostgreSQL 17 installation.")

report_data["phase3_pgvector_installed"] = pgvector_installed

# ----------------------------------------------------
# PHASE 4 & 5 — CONFIGURE .ENV & PROVE CONNECTION
# ----------------------------------------------------
print("\n=== PHASE 4 & 5: CONFIGURING ENVIRONMENT & PROVING CONNECTION ===")
env_path = ".env"
with open(env_path, "r", encoding="utf-8") as f:
    env_lines = f.readlines()

new_env = [l for l in env_lines if not l.startswith("DATA_BACKEND") and not l.startswith("VECTOR_BACKEND") and not l.startswith("DATABASE_URL")]
new_env.append("DATA_BACKEND=postgres\n")
new_env.append("VECTOR_BACKEND=pgvector\n")
new_env.append(f"DATABASE_URL={TARGET_URL}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_env)

print("Updated .env with REAL PostgreSQL configuration.")

engine = create_engine(TARGET_URL)
with engine.connect() as conn:
    row = conn.execute(text("SELECT current_database(), current_user, version();")).fetchone()
    print(f"Connected to REAL PostgreSQL -> DB: {row[0]}, User: {row[1]}, Version: {row[2][:30]}")
    report_data["phase5_db"] = row[0]
    report_data["phase5_user"] = row[1]
    report_data["phase5_version"] = row[2]

# ----------------------------------------------------
# PHASE 6 — CREATE REAL POSTGRESQL SCHEMA
# ----------------------------------------------------
print("\n=== PHASE 6: CREATING POSTGRESQL SCHEMA ===")
Base.metadata.create_all(engine)

t_cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
""")
tables = [r[0] for r in t_cur.fetchall()]
print("Tables in 'trustlayer_db' public schema:", tables)
report_data["phase6_tables"] = tables

# ----------------------------------------------------
# PHASE 7 — PERFORM REAL POSTGRESQL HOTEL INGESTION
# ----------------------------------------------------
print("\n=== PHASE 7: INGESTING HOTELS INTO REAL POSTGRESQL ===")
ingest_res = run_bootstrap(mode="apply", db_url=TARGET_URL)
print("Bootstrap Ingestion Result:", ingest_res)
report_data["phase7_ingestion"] = ingest_res

# ----------------------------------------------------
# PHASE 8, 9, 10 — DIRECTLY VERIFY POSTGRESQL DATA
# ----------------------------------------------------
print("\n=== PHASE 8, 9, 10: VERIFYING POSTGRESQL DATA ===")
t_cur.execute("SELECT COUNT(*) FROM hotels;")
h_count = t_cur.fetchone()[0]

t_cur.execute("SELECT COUNT(DISTINCT hotel_id) FROM hotels;")
h_unique = t_cur.fetchone()[0]

print(f"PostgreSQL Hotels Count: {h_count} (Unique IDs: {h_unique})")

table_counts = {}
for t in ["hotels", "hotel_locations", "hotel_scores", "hotel_sources", "hotel_amenities", "hotel_provenance", "domain_events", "ingestion_records", "ingestion_runs"]:
    t_cur.execute(f"SELECT COUNT(*) FROM {t};")
    table_counts[t] = t_cur.fetchone()[0]

print("PostgreSQL Table Counts:", table_counts)

t_cur.execute("""
    SELECT COUNT(*) 
    FROM hotel_locations l 
    LEFT JOIN hotels h ON h.hotel_id = l.hotel_id 
    WHERE h.hotel_id IS NULL;
""")
orphan_locs = t_cur.fetchone()[0]

report_data["phase8_h_count"] = h_count
report_data["phase8_h_unique"] = h_unique
report_data["phase9_table_counts"] = table_counts
report_data["phase10_orphan_locs"] = orphan_locs

# ----------------------------------------------------
# PHASE 12 — CHECK EMBEDDING COLUMN DATATYPE
# ----------------------------------------------------
print("\n=== PHASE 12: CHECKING EMBEDDING DATATYPE ===")
t_cur.execute("""
    SELECT column_name, data_type, udt_name 
    FROM information_schema.columns 
    WHERE table_name = 'embedding_documents' AND column_name = 'embedding_vector';
""")
col_info = t_cur.fetchone()
print("embedding_vector Column Datatype:", col_info)
report_data["phase12_col_info"] = col_info

is_native_pgvector = col_info and col_info[2] == "vector"
print("Is Native pgvector ('vector'):", is_native_pgvector)
report_data["phase12_is_native_pgvector"] = is_native_pgvector

# ----------------------------------------------------
# PHASE 13 — PERFORM PGVECTOR BACKFILL
# ----------------------------------------------------
print("\n=== PHASE 13: PERFORMING BACKFILL INTO POSTGRESQL ===")
backfill_res = run_pgvector_backfill(mode="apply", batch_size=200, db_url=TARGET_URL)
print("Backfill Result:", backfill_res)

t_cur.execute("SELECT COUNT(*) FROM embedding_documents;")
emb_count = t_cur.fetchone()[0]
print("PostgreSQL embedding_documents Count:", emb_count)
report_data["phase13_emb_count"] = emb_count

target_conn.close()

# Save raw pipeline result
with open("architecture_and_system_docs/stage24/stage24_4_pipeline_raw.json", "w", encoding="utf-8") as f:
    json.dump(report_data, f, indent=2, default=str)

print("\nPhase 2 to 13 completed successfully. Raw data saved to architecture_and_system_docs/stage24/stage24_4_pipeline_raw.json")
