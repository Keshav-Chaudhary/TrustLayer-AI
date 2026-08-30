import os
import sys
import time
import json
import argparse
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.db_schema import DomainEventModel, Base
from app.repositories.pgvector_embedding_repository import PgVectorEmbeddingRepository

def process_outbox_events(db_url: Optional[str] = None, batch_size: int = 50) -> Dict[str, Any]:
    target_db_url = db_url or settings.DATABASE_URL or "sqlite:///data/bootstrap_stage24.db"
    engine = create_engine(target_db_url, connect_args={"check_same_thread": False} if "sqlite" in target_db_url else {})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    session = SessionLocal()
    processed_count = 0
    failed_count = 0

    try:
        unprocessed = session.query(DomainEventModel)\
            .filter(DomainEventModel.processed_at.is_(None))\
            .filter(DomainEventModel.attempt_count < 3)\
            .order_by(DomainEventModel.created_at.asc())\
            .limit(batch_size).all()

        if not unprocessed:
            return {"processed": 0, "failed": 0, "status": "NO_EVENTS"}

        emb_repo = PgVectorEmbeddingRepository(db_url=target_db_url, session=session)

        for evt in unprocessed:
            evt.attempt_count += 1
            try:
                payload = json.loads(evt.payload)
                hid = evt.aggregate_id

                if evt.event_type in ["HOTEL_CREATED", "HOTEL_UPDATED", "EMBEDDING_REQUIRED"]:
                    name = payload.get("name", "")
                    area = payload.get("area", "")
                    city = payload.get("city", "")
                    trust_score = payload.get("trust_score", 85.0)

                    snippet = f"Hotel {name} located in {area}, {city} with a Trust Score of {trust_score:.1f}. Features guest-verified amenities."
                    chk_id = f"{hid}_chunk_a"

                    emb_repo.upsert_embeddings([{
                        "chunk_id": chk_id,
                        "hotel_id": hid,
                        "chunk_type": "Chunk A (Profile)",
                        "snippet": snippet,
                        "content_hash": evt.event_id
                    }])

                evt.processed_at = datetime.utcnow()
                processed_count += 1
            except Exception as ex:
                evt.last_error = str(ex)
                failed_count += 1

        session.commit()
        return {"processed": processed_count, "failed": failed_count, "status": "SUCCESS"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def run_worker_loop(db_url: Optional[str] = None, interval: float = 2.0, max_runs: Optional[int] = None):
    print(f"=== OUTBOX EVENT WORKER STARTED [POLL INTERVAL: {interval}s] ===")
    runs = 0
    while True:
        try:
            res = process_outbox_events(db_url=db_url)
            if res["processed"] > 0 or res["failed"] > 0:
                print(f"Outbox Worker Processed: {res['processed']}, Failed: {res['failed']}")
        except Exception as e:
            print(f"Worker Error: {str(e)}")

        runs += 1
        if max_runs and runs >= max_runs:
            break
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 24 Domain Event Outbox Worker")
    parser.add_argument("--db-url", help="Target database URL")
    parser.add_argument("--once", action="store_true", help="Run a single batch process and exit")
    args = parser.parse_args()

    if args.once:
        res = process_outbox_events(db_url=args.db_url)
        print(f"Single run completed: {res}")
    else:
        run_worker_loop(db_url=args.db_url)
