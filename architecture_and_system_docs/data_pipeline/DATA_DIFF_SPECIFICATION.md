# DATA DIFF SPECIFICATION

The Diff Engine (`scripts/ingestion/diff_engine.py`) categorizes incoming records against live PostgreSQL:
- **`NEW`**: `hotel_id` does not exist in PostgreSQL `hotels` table.
- **`UPDATED`**: `hotel_id` exists in PostgreSQL, but canonical content hash differs.
- **`UNCHANGED`**: `hotel_id` exists in PostgreSQL and content hash matches byte-for-byte.
- **`REMOVED`**: `hotel_id` exists in PostgreSQL but missing from incoming canonical dataset.
