import re
from typing import Dict, Any, List, Tuple

REQUIRED_FIELDS = ["hotel_id", "hotel_name"]

def validate_record_contract(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    
    # Check Required Fields
    for field in REQUIRED_FIELDS:
        val = str(record.get(field, "")).strip()
        if not val or val.lower() == "nan" or val.lower() == "none":
            errors.append(f"Missing required field: '{field}'")

    # Rating validation: 0.0 <= rating <= 5.0
    rating_raw = record.get("rating")
    if rating_raw is not None and str(rating_raw).strip() != "":
        try:
            rating = float(rating_raw)
            if rating < 0.0 or rating > 5.0:
                errors.append(f"Rating out of bounds [0.0, 5.0]: {rating}")
        except (ValueError, TypeError):
            errors.append(f"Invalid rating format: '{rating_raw}'")

    # Trust Score validation: 0.0 <= trust_score <= 100.0
    trust_raw = record.get("trust_score")
    if trust_raw is not None and str(trust_raw).strip() != "":
        try:
            trust_sc = float(trust_raw)
            if trust_sc <= 1.0 and trust_sc > 0.0:
                trust_sc *= 100.0
            if trust_sc < 0.0 or trust_sc > 100.0:
                errors.append(f"Trust score out of bounds [0.0, 100.0]: {trust_sc}")
        except (ValueError, TypeError):
            errors.append(f"Invalid trust_score format: '{trust_raw}'")

    # Review count validation: review_count >= 0
    rev_raw = record.get("review_count")
    if rev_raw is not None and str(rev_raw).strip() != "":
        try:
            rev_cnt = int(float(rev_raw))
            if rev_cnt < 0:
                errors.append(f"Negative review_count: {rev_cnt}")
        except (ValueError, TypeError):
            errors.append(f"Invalid review_count format: '{rev_raw}'")

    # Latitude / Longitude validation
    lat_raw = record.get("latitude")
    if lat_raw is not None and str(lat_raw).strip() != "":
        try:
            lat = float(lat_raw)
            if lat < -90.0 or lat > 90.0:
                errors.append(f"Latitude out of bounds [-90, 90]: {lat}")
        except (ValueError, TypeError):
            errors.append(f"Invalid latitude format: '{lat_raw}'")

    lng_raw = record.get("longitude")
    if lng_raw is not None and str(lng_raw).strip() != "":
        try:
            lng = float(lng_raw)
            if lng < -180.0 or lng > 180.0:
                errors.append(f"Longitude out of bounds [-180, 180]: {lng}")
        except (ValueError, TypeError):
            errors.append(f"Invalid longitude format: '{lng_raw}'")

    return (len(errors) == 0, errors)
