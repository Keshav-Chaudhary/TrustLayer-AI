# STAGE 28 — DATA LINEAGE

```text
PostgreSQL Hotel Record (hotels table in trustlayer_db)
  ▲
  │ (Stage 26 Ingestion: pipeline.py apply)
  │
Canonical Hotel Row (data/exports/final_hotel_dataset.csv)
  ▲
  │ (merge_dataset.py)
  ├───────────────────────────────────────┐
  │                                       │
Hotel Features (hotel_features.csv)    Hotel Review Summary (hotel_review_summary.csv)
  ▲                                       ▲
  │ (engineer_features.py)                │ (aggregate_reviews.py)
  │                                       │
Cleaned Hotel Metadata                Review Features (review_features.csv)
  ▲                                       ▲
  │ (clean_hotel_metadata.py)             │ (analyze_sentiment.py & extract_absa_features.py)
  │                                       │
Raw Google Places CSV                 Cleaned Reviews CSV (reviews_cleaned.csv)
  ▲                                       ▲
  │ (fetch_google_places.py)              │ (clean_reviews.py)
  │                                       │
Google Places API                     Raw Reviews CSV (reviews_raw.csv)
```
