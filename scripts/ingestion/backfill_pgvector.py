import os
import sys
import json
import time
import hashlib
import argparse
from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.db_schema import Base, EmbeddingDocumentModel

def run_pgvector_backfill(
    mode: str = "dry-run",
    batch_size: int = 100,
    db_url: Optional[str] = None
) -> Dict[str, Any]:
    target_db_url = db_url or settings.DATABASE_URL or "sqlite:///data/bootstrap_test_idempotency.db"
    engine = create_engine(target_db_url, connect_args={"check_same_thread": False} if "sqlite" in target_db_url else {})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    # Read-only source: ChromaDB
    chroma_dir = os.path.abspath(settings.VECTOR_STORE_PATH)
    chroma_client = chromadb.PersistentClient(path=chroma_dir)
    coll = chroma_client.get_collection("hotel_knowledge")

    chroma_data = coll.get(include=["metadatas", "documents"])
    c_ids = chroma_data["ids"]
    c_docs = chroma_data["documents"]
    c_metas = chroma_data["metadatas"]

    total_chroma = len(c_ids)

    session = SessionLocal()
    try:
        # Read existing pgvector chunk IDs & content hashes
        existing_pg_docs = session.query(EmbeddingDocumentModel).all()
        pg_map = {d.chunk_id: d.content_hash for d in existing_pg_docs}
        existing_pg_count = len(pg_map)

        missing_ids = []
        unchanged_ids = []
        changed_ids = []

        for cid, doc, meta in zip(c_ids, c_docs, c_metas):
            chash = hashlib.sha256(doc.encode("utf-8")).hexdigest()
            if cid not in pg_map:
                missing_ids.append((cid, doc, meta, chash))
            elif pg_map[cid] == chash:
                unchanged_ids.append(cid)
            else:
                changed_ids.append((cid, doc, meta, chash))

        print(f"=== PGVECTOR EMBEDDING BACKFILL PIPELINE [MODE: {mode.upper()}] ===")
        print(f"Chroma Source Chunks  : {total_chroma}")
        print(f"Existing pgvector Chunks: {existing_pg_count}")
        print(f"Already Synchronized : {len(unchanged_ids)}")
        print(f"Missing Chunks to Add: {len(missing_ids)}")
        print(f"Changed Chunks       : {len(changed_ids)}")

        if mode == "dry-run":
            return {
                "mode": "dry-run",
                "chroma_chunks": total_chroma,
                "existing_pgvector": existing_pg_count,
                "synchronized": len(unchanged_ids),
                "missing": len(missing_ids),
                "changed": len(changed_ids),
                "expected_inserts": len(missing_ids) + len(changed_ids)
            }

        if mode == "verify":
            parity_matched = (len(missing_ids) == 0 and len(changed_ids) == 0 and existing_pg_count == total_chroma)
            print(f"Parity Verification Result: {'PASSED (100% Match)' if parity_matched else 'INCOMPLETE'}")
            return {
                "mode": "verify",
                "parity_matched": parity_matched,
                "chroma_chunks": total_chroma,
                "pgvector_chunks": existing_pg_count
            }

        # MODE: APPLY
        to_process = missing_ids + changed_ids
        if not to_process:
            print("No missing or changed chunks to process. Backfill is up-to-date!")
            return {
                "mode": "apply",
                "inserted": 0,
                "updated": 0,
                "unchanged": len(unchanged_ids)
            }

        print(f"\nStarting batch embedding generation ({len(to_process)} chunks in batches of {batch_size})...")
        encoder = SentenceTransformer(settings.EMBEDDING_MODEL)

        inserted_cnt = 0
        updated_cnt = 0
        start_time = time.time()

        for i in range(0, len(to_process), batch_size):
            batch = to_process[i:i + batch_size]
            b_texts = [item[1] for item in batch]
            b_vecs = encoder.encode(b_texts).tolist()

            batch_session = SessionLocal()
            try:
                for (cid, doc, meta, chash), vec in zip(batch, b_vecs):
                    hid = meta.get("hotel_id", "") if meta else ""
                    ctype = meta.get("chunk_type", "Chunk A (Profile)") if meta else "Chunk A (Profile)"

                    db_doc = batch_session.query(EmbeddingDocumentModel).filter(EmbeddingDocumentModel.chunk_id == cid).first()

                    if not db_doc:
                        db_doc = EmbeddingDocumentModel(
                            chunk_id=cid,
                            hotel_id=hid,
                            chunk_type=ctype
                        )
                        batch_session.add(db_doc)
                        inserted_cnt += 1
                    else:
                        updated_cnt += 1

                    db_doc.snippet = doc
                    db_doc.content_hash = chash
                    db_doc.embedding_model = settings.EMBEDDING_MODEL
                    db_doc.embedding_dimension = len(vec)
                    db_doc.embedding_vector = json.dumps(vec)

                batch_session.commit()
                print(f"Batch {i // batch_size + 1}/{(len(to_process) + batch_size - 1) // batch_size} committed ({len(batch)} chunks).")
            except Exception as ex:
                batch_session.rollback()
                print(f"Batch failed at offset {i}: {str(ex)}")
                raise ex
            finally:
                batch_session.close()

        elapsed = time.time() - start_time
        print(f"\n--- PGVECTOR BACKFILL SUMMARY ---")
        print(f"Duration        : {elapsed:.2f}s")
        print(f"Chunks Inserted : {inserted_cnt}")
        print(f"Chunks Updated  : {updated_cnt}")
        print(f"Chunks Unchanged: {len(unchanged_ids)}")
        print(f"Total pgvector  : {session.query(EmbeddingDocumentModel).count()}")

        return {
            "mode": "apply",
            "inserted": inserted_cnt,
            "updated": updated_cnt,
            "unchanged": len(unchanged_ids),
            "total_pgvector": session.query(EmbeddingDocumentModel).count(),
            "duration_seconds": elapsed
        }
    finally:
        session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 24.2 pgvector Full Backfill Script")
    parser.add_argument("--mode", choices=["dry-run", "apply", "verify"], default="dry-run", help="Execution mode")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for embedding generation")
    parser.add_argument("--db-url", help="Target database URL")
    args = parser.parse_args()

    run_pgvector_backfill(mode=args.mode, batch_size=args.batch_size, db_url=args.db_url)
