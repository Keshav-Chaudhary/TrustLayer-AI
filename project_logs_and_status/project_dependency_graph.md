# Project Dependency Graph

## Data Pipeline Dependency Chain
`delhi_hotels_raw.csv`
↓
`clean_hotel_metadata.py`
↓
`delhi_hotels_cleaned.csv`
↓
`engineer_features.py`
↓
`hotel_features.csv`
↓
`merge_dataset.py`
↓
`final_hotel_dataset.csv`
↓
`content_based.py` & `hybrid.py`
↓
Hybrid Recommender
↓
Explainability Layer
↓
Validation Reports
↓
Audit Reports

## Reviews Pipeline Dependency Chain
`reviews_raw.csv`
↓
`clean_reviews.py`
↓
`reviews_cleaned.csv`
↓
`analyze_sentiment.py` & `extract_absa_features.py`
↓
`review_features.csv`
↓
`aggregate_reviews.py`
↓
`hotel_review_summary.csv`
↓
`merge_dataset.py`
↓
`final_hotel_dataset.csv`

## User Interaction Pipeline Dependency Chain
`users.csv` + `final_hotel_dataset.csv`
↓
`generate_interactions.py`
↓
`interactions.csv`
↓
`evaluate_recommenders.py` (Identified bias)
↓
`generate_interactions_v2.py`
↓
`interactions_v2.csv`
↓
`collaborative.py`
↓
Hybrid Recommender

## Explainability Dependency Chain
`final_hotel_dataset.csv` + `interactions_v2.csv`
↓
`explainer.py`
↓
Explainability Outputs
↓
`audit_explainability_b1.py`
↓
`explainability_audit_b1.md`
