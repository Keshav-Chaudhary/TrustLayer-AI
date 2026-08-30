# Project History

## Stage 1: Data Collection
* **Objective**: Gather raw data for hotels and their reviews in Delhi to serve as the foundation for the recommendation system.
* **Scripts Created**: `scripts/collection/fetch_google_places.py`, `scripts/collection/fetch_google_reviews.py`
* **Datasets Produced**: `data/raw/google_places/delhi_hotels_raw.csv`, `data/raw/reviews/reviews_raw.csv`
* **Reports Generated**: N/A
* **Models Trained**: N/A
* **Validation Results**: Successfully collected initial pool of hotels and corresponding reviews.
* **Key Findings**: Google Places API provides a solid baseline for hotel metadata but lacks some deeper amenities details.
* **Lessons Learned**: Rate limiting and pagination are critical when collecting large volumes of data from external APIs.
* **Dependencies Introduced**: `requests`, `googlemaps`
* **Go/No-Go Decisions**: Go. Data quality is sufficient to proceed to cleaning.

## Stage 2: Data Cleaning
* **Objective**: Clean and standardize the raw collected data, handle missing values, and prepare for NLP and feature engineering.
* **Scripts Created**: `scripts/cleaning/clean_hotel_metadata.py`, `scripts/cleaning/clean_reviews.py`
* **Datasets Produced**: `data/processed/cleaned/delhi_hotels_cleaned.csv`, `data/processed/cleaned/reviews_cleaned.csv`
* **Reports Generated**: `research/reports/data_quality_report.md`
* **Models Trained**: N/A
* **Validation Results**: Reduced null values, standardized text fields, removed duplicates.
* **Key Findings**: Significant variance in review lengths and languages.
* **Lessons Learned**: Robust regex and text normalization are essential before any NLP tasks.
* **Dependencies Introduced**: `pandas`, `numpy`
* **Go/No-Go Decisions**: Go. Clean datasets are ready for downstream processing.

## Stage 3: NLP Pipeline
* **Objective**: Extract sentiment and Aspect-Based Sentiment Analysis (ABSA) features from cleaned reviews.
* **Scripts Created**: `scripts/nlp/analyze_sentiment.py`, `scripts/nlp/extract_absa_features.py`
* **Datasets Produced**: `data/processed/features/review_features.csv`
* **Reports Generated**: `research/notebooks/03_sentiment_analysis.ipynb`, `research/notebooks/04_absa_explainability_analysis.ipynb`
* **Models Trained**: N/A (Utilized pre-trained NLP models)
* **Validation Results**: Successfully extracted sentiment polarity and aspect-specific sentiments (e.g., cleanliness, service, location).
* **Key Findings**: Service and cleanliness are the most frequently discussed aspects in Delhi hotel reviews.
* **Lessons Learned**: Off-the-shelf sentiment analyzers need fine-tuning or domain-specific context for nuanced hotel reviews.
* **Dependencies Introduced**: `nltk`, `spacy`, `transformers` (or equivalent)
* **Go/No-Go Decisions**: Go. Sentiment features add high value for recommendation explainability.

## Stage 4: Feature Engineering
* **Objective**: Create composite features, such as Trust Score, and aggregate review data to the hotel level.
* **Scripts Created**: `scripts/recommender/engineer_features.py`, `scripts/recommender/aggregate_reviews.py`, `scripts/recommender/merge_dataset.py`
* **Datasets Produced**: `data/processed/features/hotel_features.csv`, `data/processed/features/hotel_review_summary.csv`, `data/exports/final_hotel_dataset.csv`
* **Reports Generated**: `research/notebooks/05_feature_engineering_analysis.ipynb`, `research/reports/eda_report.md`
* **Models Trained**: N/A
* **Validation Results**: Features like Trust Score properly distribute and correlate with high ratings.
* **Key Findings**: Engineered features significantly differentiate otherwise similar hotels.
* **Lessons Learned**: Aggregating sentiment features requires careful handling of sparse data.
* **Dependencies Introduced**: `scikit-learn`
* **Go/No-Go Decisions**: Go. The merged dataset is ready for recommender model consumption.

## Stage 5: Synthetic User Generation
* **Objective**: Generate synthetic users and interaction data to overcome cold-start constraints and simulate user behavior.
* **Scripts Created**: `scripts/recommender/generate_users.py`, `scripts/recommender/generate_interactions.py`
* **Datasets Produced**: `data/raw/synthetic_users/users.csv`, `data/raw/synthetic_users/interactions.csv`
* **Reports Generated**: `research/notebooks/06_user_dataset_analysis.ipynb`, `research/notebooks/07_interaction_analysis.ipynb`
* **Models Trained**: N/A
* **Validation Results**: Synthetic interactions follow expected power-law distributions.
* **Key Findings**: Simulating realistic user behavior requires complex interaction probability modeling.
* **Lessons Learned**: Synthetic data can introduce artificial biases if not carefully calibrated.
* **Dependencies Introduced**: `faker`
* **Go/No-Go Decisions**: Go. Necessary for training collaborative filtering algorithms.

## Stage 6: Recommendation System
* **Objective**: Develop baseline, collaborative, content-based, and hybrid recommendation models.
* **Scripts Created**: `scripts/recommender/baseline.py`, `scripts/recommender/collaborative.py`, `scripts/recommender/content_based.py`, `scripts/recommender/hybrid.py`
* **Datasets Produced**: Model objects in `data/models/`
* **Reports Generated**: `research/reports/recommender_evaluation.md`, `research/notebooks/09_recommender_diagnostics.ipynb`
* **Models Trained**: Baseline, Collaborative (SVD), Content-Based, Hybrid
* **Validation Results**: Hybrid model outperforms individual models in precision and recall.
* **Key Findings**: Collaborative filtering struggles heavily with the cold-start problem, validating the need for the hybrid approach.
* **Lessons Learned**: Tuning the hybrid weighting (or using RRF) is critical for balanced recommendations.
* **Dependencies Introduced**: `surprise` or `implicit`
* **Go/No-Go Decisions**: Go. Models are functional but require interaction refinement.

## Stage 6.1: Recommendation Remediation
* **Objective**: Address issues identified in the initial recommender evaluation (e.g., interaction sparsity or bias).
* **Scripts Created**: `scripts/synthetic/generate_interactions_v2.py`
* **Datasets Produced**: `data/raw/synthetic_users/interactions_v2.csv`
* **Reports Generated**: `research/reports/recommender_remediation_report.md`
* **Models Trained**: Retrained Recommender Models on V2 data
* **Validation Results**: Improved coverage and reduced popularity bias in recommendations.
* **Key Findings**: Tweaking interaction generation logic significantly impacts downstream model fairness.
* **Lessons Learned**: Data-centric approaches (improving interactions) often yield better results than model hyperparameter tuning.
* **Dependencies Introduced**: None
* **Go/No-Go Decisions**: Go. Ready for explainability layer.

## Stage 7: Explainability Layer
* **Objective**: Implement mechanisms to explain *why* a hotel was recommended to a user.
* **Scripts Created**: `scripts/explainability/explainer.py`, `scripts/explainability/evaluate_explanations.py`
* **Datasets Produced**: `data/processed/features/explainability_features.csv`
* **Reports Generated**: `research/reports/explainability_evaluation.md`
* **Models Trained**: N/A (Analytical explainer implemented)
* **Validation Results**: Explanations generated successfully using analytical methods rather than complex SHAP approximations.
* **Key Findings**: Users (and audits) prefer transparent analytical explanations linking features directly to user preferences.
* **Lessons Learned**: SHAP was too slow and complex for the hybrid pipeline; analytical explainability is more practical.
* **Dependencies Introduced**: None
* **Go/No-Go Decisions**: Go. Proceed to formal validation.

## Stage 7.1: Explainability Validation (Stage B.1)
* **Objective**: Formally audit and validate the explainability layer for correctness, coverage, and human readability.
* **Scripts Created**: `scripts/explainability/audit_explainability_b1.py`
* **Datasets Produced**: N/A
* **Reports Generated**: `research/reports/explainability_audit_b1.md`
* **Models Trained**: N/A
* **Validation Results**: Explainability logic validated against a diverse set of edge cases.
* **Key Findings**: Minor coverage gaps identified for cold-start users, but overall logic is sound.
* **Lessons Learned**: Automated auditing of explanations ensures consistent system behavior before deployment.
* **Dependencies Introduced**: None
* **Go/No-Go Decisions**: Go. Current project scope completed successfully.
