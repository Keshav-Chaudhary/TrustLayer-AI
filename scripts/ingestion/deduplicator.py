from typing import List, Dict, Any, Tuple

def deduplicate_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    seen_ids = set()
    deduped = []
    rejected_duplicates = []

    for r in records:
        hid = r.get("hotel_id")
        if not hid:
            continue

        if hid in seen_ids:
            rejected_duplicates.append(r)
        else:
            seen_ids.add(hid)
            deduped.append(r)

    return (deduped, rejected_duplicates)
