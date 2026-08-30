import os
import sys
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.db_schema import HotelModel, calculate_canonical_content_hash

def compute_postgresql_diff(
    canonical_records: List[Dict[str, Any]],
    db_url: Optional[str] = None
) -> Dict[str, Any]:
    target_db_url = db_url or settings.DATABASE_URL
    assert target_db_url and "postgresql" in target_db_url, "DATABASE_URL must be configured for PostgreSQL"

    engine = create_engine(target_db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        existing_hotels = session.query(HotelModel).all()
        db_map = {h.hotel_id: h for h in existing_hotels}

        from app.repositories.db_schema import IngestionRecordModel
        records_db = session.query(IngestionRecordModel).order_by(IngestionRecordModel.timestamp.desc()).all()
        hash_map = {}
        for r in records_db:
            if r.hotel_id not in hash_map:
                hash_map[r.hotel_id] = r.new_hash

        new_hotels = []
        updated_hotels = []
        unchanged_hotels = []
        field_diffs = []

        canonical_ids = set()

        for rec in canonical_records:
            hid = rec.get("hotel_id")
            canonical_ids.add(hid)

            new_hash = calculate_canonical_content_hash(rec)
            
            if hid not in db_map:
                new_hotels.append(rec)
            else:
                existing_h = db_map[hid]
                stored_hash = hash_map.get(hid)

                if stored_hash and stored_hash == new_hash:
                    unchanged_hotels.append(rec)
                else:
                    updated_hotels.append(rec)
                    diff_item = {"hotel_id": hid, "changes": []}
                    if existing_h.name != rec.get("name"):
                        diff_item["changes"].append({"field": "name", "old": existing_h.name, "new": rec.get("name")})
                    field_diffs.append(diff_item)

        # Removed records (In DB but missing from incoming canonical dataset)
        removed_ids = [hid for hid in db_map.keys() if hid not in canonical_ids]

        return {
            "total_canonical": len(canonical_records),
            "total_db_existing": len(db_map),
            "new_count": len(new_hotels),
            "updated_count": len(updated_hotels),
            "unchanged_count": len(unchanged_hotels),
            "removed_count": len(removed_ids),
            "new_hotels": new_hotels[:10],
            "updated_hotels": updated_hotels[:10],
            "field_diffs": field_diffs[:20],
            "removed_ids": removed_ids[:10]
        }
    finally:
        session.close()
