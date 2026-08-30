import os
import sys
import json
import uuid
import hashlib
import argparse
from datetime import datetime
from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.db_schema import (
    Base, HotelModel, HotelLocationModel, HotelScoreModel, HotelSourceModel,
    HotelAmenityModel, HotelProvenanceModel, IngestionRunModel, IngestionRecordModel,
    DomainEventModel, calculate_canonical_content_hash
)

def validate_hotel_record(row: pd.Series) -> Tuple[bool, List[str]]:
    errors = []
    hid = str(row.get('hotel_id', '')).strip()
    if not hid or hid == 'nan':
        errors.append("Missing hotel_id")
    
    hname = str(row.get('hotel_name', '')).strip()
    if not hname or hname == 'nan':
        errors.append("Missing hotel_name")
        
    try:
        rating = float(row.get('rating', 4.0)) if pd.notnull(row.get('rating')) else 4.0
        if rating < 0.0 or rating > 5.0:
            errors.append(f"Rating out of bounds [0.0, 5.0]: {rating}")
    except (ValueError, TypeError):
        errors.append("Invalid rating format")
        
    try:
        rev_cnt = int(float(row.get('review_count', 0))) if pd.notnull(row.get('review_count')) else 0
        if rev_cnt < 0:
            errors.append(f"Negative review_count: {rev_cnt}")
    except (ValueError, TypeError):
        errors.append("Invalid review_count format")
        
    try:
        trust_sc = float(row.get('trust_score', 85.0))
        if trust_sc <= 1.0:
            trust_sc *= 100.0
        if trust_sc < 0.0 or trust_sc > 100.0:
            errors.append(f"Trust score out of bounds [0.0, 100.0]: {trust_sc}")
    except (ValueError, TypeError):
        errors.append("Invalid trust_score format")
        
    return (len(errors) == 0, errors)


def run_bootstrap(
    mode: str = "dry-run",
    csv_path: Optional[str] = None,
    db_url: Optional[str] = None
) -> Dict[str, Any]:
    csv_file = csv_path or settings.CSV_DATASET_PATH
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV dataset not found at {csv_file}")
        
    target_db_url = db_url or settings.DATABASE_URL or "sqlite:///data/bootstrap_stage24.db"
    
    engine = create_engine(target_db_url, connect_args={"check_same_thread": False} if "sqlite" in target_db_url else {})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    
    # Calculate CSV source checksum
    h = hashlib.sha256()
    with open(csv_file, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    source_checksum = h.hexdigest()
    
    df = pd.read_csv(csv_file)
    total_records = len(df)
    
    run_id = str(uuid.uuid4())
    started_at = datetime.utcnow()
    
    records_inserted = 0
    records_updated = 0
    records_unchanged = 0
    records_rejected = 0
    validation_errors_list = []
    
    print(f"=== POSTGRESQL BOOTSTRAP PIPELINE [MODE: {mode.upper()}] ===")
    print(f"Run ID: {run_id}")
    print(f"Source Checksum: {source_checksum}")
    print(f"Target Database URL: {target_db_url}")
    print(f"Records Seen: {total_records}")
    
    if mode == "validate-only":
        for idx, row in df.iterrows():
            valid, errs = validate_hotel_record(row)
            if not valid:
                records_rejected += 1
                validation_errors_list.append({"row": idx, "hotel_id": str(row.get('hotel_id')), "errors": errs})
        print(f"Validation complete: {total_records - records_rejected} valid, {records_rejected} rejected.")
        return {
            "status": "VALIDATED",
            "records_seen": total_records,
            "records_valid": total_records - records_rejected,
            "records_rejected": records_rejected,
            "validation_errors": validation_errors_list
        }
        
    session = SessionLocal()
    try:
        run_record = IngestionRunModel(
            run_id=run_id,
            source=os.path.basename(csv_file),
            source_checksum=source_checksum,
            started_at=started_at,
            status="IN_PROGRESS" if mode == "apply" else "DRY_RUN"
        )
        if mode == "apply":
            session.add(run_record)
            
        for idx, row in df.iterrows():
            valid, errs = validate_hotel_record(row)
            hid = str(row.get('hotel_id', '')).strip()
            
            if not valid:
                records_rejected += 1
                validation_errors_list.append({"row": idx, "hotel_id": hid, "errors": errs})
                continue
                
            # Prepare canonical record dict
            hname = str(row.get('hotel_name', '')).strip()
            area = str(row.get('area', '')).strip() if pd.notnull(row.get('area')) else "Delhi"
            city = str(row.get('city', '')).strip() if pd.notnull(row.get('city')) else "Delhi"
            dest = str(row.get('destination', '')).strip() if pd.notnull(row.get('destination')) else city
            
            raw_trust = float(row.get('trust_score', 85.0))
            trust_score = round(raw_trust * 100.0 if raw_trust <= 1.0 else raw_trust, 1)
            
            clean_score = round(float(row.get('cleanliness_score', 0.9)) * 5.0 if float(row.get('cleanliness_score', 0.9)) <= 1.0 else float(row.get('cleanliness_score', 4.5)), 1)
            serv_score = round(float(row.get('service_score', 0.9)) * 5.0 if float(row.get('service_score', 0.9)) <= 1.0 else float(row.get('service_score', 4.5)), 1)
            loc_score = round(float(row.get('location_score', 0.9)) * 5.0 if float(row.get('location_score', 0.9)) <= 1.0 else float(row.get('location_score', 4.5)), 1)
            val_score = round(float(row.get('value_score', 0.9)) * 5.0 if float(row.get('value_score', 0.9)) <= 1.0 else float(row.get('value_score', 4.5)), 1)
            staff_score = round(float(row.get('staff_behavior_score', 0.9)) * 5.0 if float(row.get('staff_behavior_score', 0.9)) <= 1.0 else float(row.get('staff_behavior_score', 4.5)), 1)

            record_dict = {
                "hotel_id": hid,
                "name": hname,
                "address": f"{area}, {city}",
                "area": area,
                "city": city,
                "destination": dest,
                "latitude": float(row.get('latitude')) if pd.notnull(row.get('latitude')) else None,
                "longitude": float(row.get('longitude')) if pd.notnull(row.get('longitude')) else None,
                "rating": float(row.get('rating', 4.0)) if pd.notnull(row.get('rating')) else 4.0,
                "review_count": int(float(row.get('review_count', 0))) if pd.notnull(row.get('review_count')) else 0,
                "price": str(row.get('price')) if pd.notnull(row.get('price')) else "₹2,500 - ₹5,000 / night",
                "budget_category": "Mid-Range",
                "trust_score": trust_score,
                "cleanliness_score": clean_score,
                "service_score": serv_score,
                "location_score": loc_score,
                "value_score": val_score,
                "amenities": ["Free Wi-Fi", "Air Conditioning", "Housekeeping", "Room Service", "24-hour Desk"]
            }

            content_hash = calculate_canonical_content_hash(record_dict)

            # Change Detection against DB
            existing = session.query(HotelModel).filter(HotelModel.hotel_id == hid).first()
            existing_source = session.query(HotelSourceModel).filter(HotelSourceModel.hotel_id == hid).first()

            previous_hash = existing_source.content_hash if existing_source else None

            if not existing:
                operation = "CREATED"
                records_inserted += 1
            elif previous_hash == content_hash:
                operation = "UNCHANGED"
                records_unchanged += 1
            else:
                operation = "UPDATED"
                records_updated += 1

            if mode == "apply":
                if operation in ["CREATED", "UPDATED"]:
                    if not existing:
                        existing = HotelModel(hotel_id=hid)
                        session.add(existing)

                    existing.name = record_dict["name"]
                    existing.address = record_dict["address"]
                    existing.rating = record_dict["rating"]
                    existing.review_count = record_dict["review_count"]
                    existing.price = record_dict["price"]
                    existing.budget_category = record_dict["budget_category"]

                    if not existing.location:
                        existing.location = HotelLocationModel(hotel_id=hid)
                    existing.location.area = record_dict["area"]
                    existing.location.city = record_dict["city"]
                    existing.location.destination = record_dict["destination"]
                    existing.location.latitude = record_dict["latitude"]
                    existing.location.longitude = record_dict["longitude"]

                    if not existing.score:
                        existing.score = HotelScoreModel(hotel_id=hid)
                    existing.score.trust_score = record_dict["trust_score"]
                    existing.score.cleanliness_score = record_dict["cleanliness_score"]
                    existing.score.service_score = record_dict["service_score"]
                    existing.score.location_score = record_dict["location_score"]
                    existing.score.value_score = record_dict["value_score"]

                    if not existing.amenities:
                        existing.amenities = HotelAmenityModel(hotel_id=hid)
                    existing.amenities.amenities_json = json.dumps(record_dict["amenities"])

                    # Update Source Content Hash
                    if not existing_source:
                        existing_source = HotelSourceModel(hotel_id=hid, source="final_hotel_dataset.csv", content_hash=content_hash)
                        session.add(existing_source)
                    else:
                        existing_source.content_hash = content_hash
                        existing_source.last_seen_at = datetime.utcnow()

                    # Domain Event Outbox (Atomic within transaction)
                    event_id = str(uuid.uuid4())
                    event_type = "HOTEL_CREATED" if operation == "CREATED" else "HOTEL_UPDATED"
                    domain_event = DomainEventModel(
                        event_id=event_id,
                        event_type=event_type,
                        aggregate_type="Hotel",
                        aggregate_id=hid,
                        version=existing.version,
                        payload=json.dumps(record_dict)
                    )
                    session.add(domain_event)

                # Record Ingestion Audit Record
                ing_rec = IngestionRecordModel(
                    ingestion_run_id=run_id,
                    hotel_id=hid,
                    operation=operation,
                    previous_hash=previous_hash,
                    new_hash=content_hash,
                    changed_fields=json.dumps(["all"] if operation == "CREATED" else []),
                    timestamp=datetime.utcnow()
                )
                session.add(ing_rec)

        if mode == "apply":
            run_record.completed_at = datetime.utcnow()
            run_record.records_seen = total_records
            run_record.records_inserted = records_inserted
            run_record.records_updated = records_updated
            run_record.records_unchanged = records_unchanged
            run_record.records_rejected = records_rejected
            run_record.validation_errors = json.dumps(validation_errors_list)
            run_record.status = "SUCCESS"
            session.commit()
            
        print("\n--- INGESTION SUMMARY ---")
        print(f"Records Inserted : {records_inserted}")
        print(f"Records Updated  : {records_updated}")
        print(f"Records Unchanged: {records_unchanged}")
        print(f"Records Rejected : {records_rejected}")
        
        return {
            "run_id": run_id,
            "mode": mode,
            "status": "SUCCESS",
            "records_seen": total_records,
            "records_inserted": records_inserted,
            "records_updated": records_updated,
            "records_unchanged": records_unchanged,
            "records_rejected": records_rejected,
            "validation_errors": validation_errors_list
        }
    except Exception as e:
        session.rollback()
        print(f"Bootstrap Failed with Error: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 24 PostgreSQL Bootstrap & ETL Pipeline")
    parser.add_argument("--mode", choices=["dry-run", "validate-only", "apply", "verify"], default="dry-run", help="Execution mode")
    parser.add_argument("--csv-path", help="Path to input CSV file")
    parser.add_argument("--db-url", help="Target database URL")
    args = parser.parse_args()
    
    run_bootstrap(mode=args.mode, csv_path=args.csv_path, db_url=args.db_url)
