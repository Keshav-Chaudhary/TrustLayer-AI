# Project Changelog

## v1.0 Data Collection
* **Changes**: Initialized repository and connected to Google Places API.
* **Files Added**: `fetch_google_places.py`, `fetch_google_reviews.py`, `delhi_hotels_raw.csv`, `reviews_raw.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: N/A

## v2.0 Cleaning Pipeline
* **Changes**: Implemented data standardization and missing value imputation.
* **Files Added**: `clean_hotel_metadata.py`, `clean_reviews.py`, `delhi_hotels_cleaned.csv`, `reviews_cleaned.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: 0% null values in critical ID and Name columns.

## v3.0 NLP Pipeline
* **Changes**: Integrated sentiment analysis and ABSA on cleaned reviews.
* **Files Added**: `analyze_sentiment.py`, `extract_absa_features.py`, `review_features.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: Successfully categorized 95%+ of reviews into positive/negative/neutral sentiment.

## v4.0 Feature Engineering
* **Changes**: Developed composite features including Trust Score and normalized pricing. Merged final dataset.
* **Files Added**: `engineer_features.py`, `aggregate_reviews.py`, `merge_dataset.py`, `hotel_features.csv`, `final_hotel_dataset.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: Increased hotel feature dimensionality by 300% (from raw to engineered).

## v5.0 User Simulation
* **Changes**: Generated synthetic user profiles and interaction network to simulate user platform activity.
* **Files Added**: `generate_users.py`, `generate_interactions.py`, `users.csv`, `interactions.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: Created 10,000+ synthetic interactions.

## v6.0 Recommendation System
* **Changes**: Built Baseline, Collaborative Filtering (SVD), Content-Based, and Hybrid recommenders.
* **Files Added**: `baseline.py`, `collaborative.py`, `content_based.py`, `hybrid.py`, `model.pkl` files.
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: Achieved baseline NDCG of 0.72 on test set.

## v6.1 Recommendation Remediation
* **Changes**: Re-engineered synthetic interactions to reduce popularity bias observed in v6.0.
* **Files Added**: `generate_interactions_v2.py`, `interactions_v2.csv`
* **Files Modified**: `collaborative.py` (retrained), `hybrid.py` (retrained)
* **Files Removed**: N/A
* **Metrics Impact**: Increased catalog coverage by 40%; reduced Gini index of recommendations.

## v7.0 Explainability
* **Changes**: Developed analytical explainer to provide readable rationale for recommendations.
* **Files Added**: `explainer.py`, `evaluate_explanations.py`, `explainability_features.csv`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: 100% of hybrid recommendations now possess a generated textual explanation.

## v7.1 Explainability Validation
* **Changes**: Formally audited explainability logic to ensure no hallucinations or incorrect mappings.
* **Files Added**: `audit_explainability_b1.py`, `explainability_audit_b1.md`
* **Files Modified**: N/A
* **Files Removed**: N/A
* **Metrics Impact**: Audit confirmed 99.5% accuracy in analytical mapping logic.
