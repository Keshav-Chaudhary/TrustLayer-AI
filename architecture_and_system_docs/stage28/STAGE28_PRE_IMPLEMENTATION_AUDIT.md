# STAGE 28 — PRE-IMPLEMENTATION FORENSIC PIPELINE AUDIT REPORT

## Executive Summary
This pre-implementation audit documents the exact call graph, script entrypoints, file paths, parameters, schemas, and dependencies for the end-to-end data pipeline in **TrustLayer-AI**.

---

## 1. Upstream Data Engineering Call Graph & Component Matrix

| Stage ID | Stage Name | Script File | Entrypoint Function | Primary Input File(s) | Primary Output File(s) | Dependencies / Models |
|---|---|---|---|---|---|---|
| `1.1` | **Fetch Places** | `scripts/collection/fetch_google_places.py` | `main()` | Google Places API / Grid | `data/raw/google_places/delhi_hotels_raw.csv` | `GOOGLE_PLACES_API_KEY`, `requests` |
| `1.2` | **Fetch Reviews** | `scripts/collection/fetch_google_reviews.py` | `fetch_reviews()` | `delhi_hotels_cleaned.csv` + Google Places API | `data/raw/reviews/reviews_raw.csv` | `GOOGLE_PLACES_API_KEY`, `requests` |
| `1.3` | **Synthetic Users** | `scripts/recommender/generate_users.py` | `generate_users()` | `final_hotel_dataset.csv` (area clusters) | `data/raw/synthetic_users/users.csv` | `pandas`, `numpy` |
| `2.1` | **Clean Hotels** | `scripts/cleaning/clean_hotel_metadata.py` | `clean_data()` | `data/raw/google_places/delhi_hotels_raw.csv` | `data/processed/cleaned/delhi_hotels_cleaned.csv` | `pandas`, bounding box filtering |
| `2.2` | **Clean Reviews** | `scripts/cleaning/clean_reviews.py` | `clean_reviews()` | `data/raw/reviews/reviews_raw.csv` | `data/processed/cleaned/reviews_cleaned.csv` | `pandas`, string regex |
| `3.1` | **Sentiment NLP** | `scripts/nlp/analyze_sentiment.py` | `run_sentiment_analysis()` | `data/processed/cleaned/reviews_cleaned.csv` | `data/processed/features/review_features.csv` | `DistilBERT` (`transformers` pipeline) |
| `3.2` | **ABSA NLP** | `scripts/nlp/extract_absa_features.py` | `extract_absa()` | `data/processed/features/review_features.csv` | `data/processed/features/explainability_features.csv` | Keyword matching + sentiment probability |
| `3.3` | **Aggregate Reviews** | `scripts/recommender/aggregate_reviews.py` | `aggregate_reviews()` | `data/processed/features/review_features.csv` | `data/processed/features/hotel_review_summary.csv` | `pandas` |
| `4.1` | **Hotel Features** | `scripts/recommender/engineer_features.py` | `engineer_features()` | `delhi_hotels_cleaned.csv` + `hotel_review_summary.csv` | `data/processed/features/hotel_features.csv` | `MinMaxScaler` (`scikit-learn`) |
| `5.1` | **Merge Dataset** | `scripts/recommender/merge_dataset.py` | `merge_final_dataset()` | `delhi_hotels_cleaned.csv` + `hotel_review_summary.csv` + `explainability_features.csv` + `hotel_features.csv` | `data/exports/final_hotel_dataset.csv` | `pandas` merge |
| `6.1` | **Stage 26 Diff** | `scripts/ingestion/pipeline.py` | `execute_pipeline(mode="dry-run")` | `data/exports/final_hotel_dataset.csv` + PostgreSQL | `data/diffs/<RUN_ID>/dry_run.json` | `diff_engine.py`, `schema_contract.py` |
| `6.2` | **PostgreSQL Apply** | `scripts/ingestion/pipeline.py` | `execute_pipeline(mode="apply", run_id=...)` | `data/diffs/<RUN_ID>/dry_run.json` | PostgreSQL `trustlayer_db` + `embedding_documents` | `bootstrap_postgres.py`, `selective_vector_sync.py` |

---

## 2. Identified Incompatibilities & Fallback Rules
1. **Google API Key Connectivity**: If `GOOGLE_PLACES_API_KEY` is not present in `.env`, source acquisition (`fetch_google_places.py` and `fetch_google_reviews.py`) fall back gracefully to preserving existing raw datasets (`delhi_hotels_raw.csv` and `reviews_raw.csv`), logging a clear warning rather than failing hard.
2. **Path Resolution**: All script entrypoints use relative pathing via `os.path.dirname(__file__)`. The orchestrator normalizes all path resolutions relative to project root (`WORKSPACE_ROOT`).
3. **Canonical Handoff Artifact**: `data/exports/final_hotel_dataset.csv` is established as the canonical handoff file between upstream feature engineering and Stage 26 PostgreSQL ingestion.
