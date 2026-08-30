# Project Stage Timeline

## Stage 1: Data Collection
* **Start State**: Empty Repository. No Data.
* **Work Performed**: Identified data sources, wrote API wrappers, fetched Google Places data and Google Reviews.
* **Files Generated**: `delhi_hotels_raw.csv`, `reviews_raw.csv`, collection scripts.
* **Validation**: Verified raw data structures and volumes against targets.
* **Outcome**: Raw data successfully acquired.
* **Next Stage**: Data Cleaning.

## Stage 2: Data Cleaning
* **Start State**: Raw, noisy data with missing values.
* **Work Performed**: Imputed missing data, standardized strings, removed duplicates.
* **Files Generated**: `delhi_hotels_cleaned.csv`, `reviews_cleaned.csv`, cleaning scripts.
* **Validation**: Data quality checks, zero nulls in critical columns.
* **Outcome**: High-quality tabular data ready for feature engineering.
* **Next Stage**: NLP Pipeline.

## Stage 3: NLP Pipeline
* **Start State**: Cleaned textual review data.
* **Work Performed**: Applied sentiment analysis and Aspect-Based Sentiment Analysis (ABSA).
* **Files Generated**: `review_features.csv`, NLP scripts, sentiment notebooks.
* **Validation**: Manual review of sentiment scores against review text.
* **Outcome**: Quantitative sentiment features mapped to qualitative text.
* **Next Stage**: Feature Engineering.

## Stage 4: Feature Engineering
* **Start State**: Cleaned metadata and NLP features.
* **Work Performed**: Created Trust Score, normalized numeric variables, encoded categoricals, aggregated reviews.
* **Files Generated**: `hotel_features.csv`, `hotel_review_summary.csv`, `final_hotel_dataset.csv`, merge scripts.
* **Validation**: EDA, correlation analysis, distributions checks.
* **Outcome**: Master dataset ready for ML models.
* **Next Stage**: Synthetic User Generation.

## Stage 5: Synthetic User Generation
* **Start State**: Hotel dataset lacking user interaction data (cold start context).
* **Work Performed**: Simulated user profiles and interaction networks (clicks, bookings).
* **Files Generated**: `users.csv`, `interactions.csv`, synthetic data scripts.
* **Validation**: Checked interaction distributions (power-law, sparsity metrics).
* **Outcome**: Simulated dataset enabling collaborative filtering.
* **Next Stage**: Recommendation System.

## Stage 6: Recommendation System
* **Start State**: Final dataset and user interactions.
* **Work Performed**: Built collaborative filtering, content-based, and hybrid (RRF) models.
* **Files Generated**: Model `.pkl` files, recommender scripts.
* **Validation**: Precision, Recall, NDCG metrics evaluated on test set.
* **Outcome**: Baseline working hybrid recommendation engine.
* **Next Stage**: Recommendation Remediation.

## Stage 6.1: Recommendation Remediation
* **Start State**: Models exhibiting popularity bias.
* **Work Performed**: Regenerated interactions (v2) to smooth bias, retrained models.
* **Files Generated**: `interactions_v2.csv`, generation scripts, remediation reports.
* **Validation**: Re-evaluated fairness and coverage metrics.
* **Outcome**: More equitable recommendation distribution.
* **Next Stage**: Explainability Layer.

## Stage 7: Explainability Layer
* **Start State**: Black-box hybrid recommendations.
* **Work Performed**: Designed analytical explainability logic matching user preferences to hotel features.
* **Files Generated**: `explainer.py`, `evaluate_explanations.py`, explainability features.
* **Validation**: Evaluated logic accuracy and text output readability.
* **Outcome**: Transparent explanations for all recommendations.
* **Next Stage**: Explainability Validation (Stage B.1).

## Stage 7.1: Explainability Validation (Stage B.1)
* **Start State**: Implemented explainer.
* **Work Performed**: Conducted formal audit of explainability outputs for edge cases.
* **Files Generated**: `audit_explainability_b1.py`, `explainability_audit_b1.md`.
* **Validation**: Automated audit passed successfully.
* **Outcome**: Validated, audit-ready explainability pipeline.
* **Next Stage**: Future (RAG / Dashboard / Deployment).
