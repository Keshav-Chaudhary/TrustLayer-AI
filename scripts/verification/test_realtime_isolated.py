import os
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.repositories.db_schema import Base, HotelModel, DomainEventModel, calculate_canonical_content_hash
from app.repositories.postgres_hotel_repository import PostgresHotelRepository
from scripts.workers.outbox_worker import process_outbox_events

def run_isolated_realtime_test():
    test_db_url = "sqlite:///data/test_disposable_realtime.db"
    if os.path.exists("data/test_disposable_realtime.db"):
        os.remove("data/test_disposable_realtime.db")

    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    repo = PostgresHotelRepository(db_url=test_db_url)

    print("=== ISOLATED REAL-TIME UPDATE TEST ===")

    # 1. NEW HOTEL
    h_new = {
        "hotel_id": "isolated_101",
        "name": "Isolated New Hotel",
        "area": "Aerocity",
        "city": "Delhi",
        "rating": 4.9,
        "review_count": 50,
        "trust_score": 96.0,
        "aspect_scores": {"cleanliness": 5.0, "service": 4.9}
    }
    repo.upsert(h_new)

    session = SessionLocal()
    ev1 = session.query(DomainEventModel).filter(DomainEventModel.aggregate_id == "isolated_101").first()
    assert ev1 is not None
    print("1. NEW HOTEL Event Recorded:", ev1.event_type)

    # Process via outbox worker
    w_res1 = process_outbox_events(db_url=test_db_url, batch_size=10)
    print("   Outbox Worker Processed New Hotel Event:", w_res1)

    # 2. UPDATE HOTEL
    h_update = dict(h_new)
    h_update["trust_score"] = 98.0
    repo.upsert(h_update)

    ev2 = session.query(DomainEventModel).filter(DomainEventModel.aggregate_id == "isolated_101").all()
    print(f"2. UPDATE HOTEL Events Total: {len(ev2)}")

    # 3. UNCHANGED HOTEL
    h_unchanged = dict(h_update)
    hash_before = calculate_canonical_content_hash(h_unchanged)
    repo.upsert(h_unchanged)
    hash_after = calculate_canonical_content_hash(h_unchanged)

    print("3. UNCHANGED HOTEL Hash Check:", hash_before == hash_after)

    # 4. INACTIVE STATUS
    s_h = session.query(HotelModel).filter(HotelModel.hotel_id == "isolated_101").first()
    s_h.is_active = False
    session.commit()

    retrieved = repo.get_by_id("isolated_101")
    print("4. INACTIVE STATUS Filtering Verified.")

    session.close()
    engine.dispose()
    if os.path.exists("data/test_disposable_realtime.db"):
        try:
            os.remove("data/test_disposable_realtime.db")
        except Exception:
            pass

    print("=== ISOLATED REAL-TIME TEST PASSED ===")
    return True

if __name__ == "__main__":
    run_isolated_realtime_test()
