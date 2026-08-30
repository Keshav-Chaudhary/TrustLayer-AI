# Project Decisions Log

**DEC-001**
* **Decision**: Use Google Places API
* **Alternatives**: TripAdvisor API, Booking.com API, Web Scraping
* **Reason**: Google Places offers a generous free tier, highly reliable location data, and easily accessible user reviews, making it ideal for the initial scope of Delhi hotels.
* **Impact**: Defined the primary data structure (`delhi_hotels_raw.csv`) and tied the project to Google's place ID system.
* **Affected Files**: `fetch_google_places.py`, `fetch_google_reviews.py`

**DEC-002**
* **Decision**: Use Synthetic Users
* **Alternatives**: Real user acquisition, Public datasets (e.g., Yelp, Amazon)
* **Reason**: No public dataset matches the specific geographic and feature space of our customized Delhi hotels dataset. Simulating users allows us to build the collaborative filtering pipeline immediately.
* **Impact**: Allowed the project to proceed to the Recommender stage without a live application. Introduced synthetic bias risk.
* **Affected Files**: `generate_users.py`, `generate_interactions.py`

**DEC-003**
* **Decision**: Create Trust Score
* **Alternatives**: Rely solely on raw review ratings
* **Reason**: Raw ratings are often inflated or lack volume context. A Trust Score incorporates rating, review count, and sentiment analysis to provide a more robust metric.
* **Impact**: Trust Score became a highly predictive feature for the content-based recommender.
* **Affected Files**: `engineer_features.py`, `hotel_features.csv`

**DEC-004**
* **Decision**: Use Content-Based Recommender
* **Alternatives**: Pure Collaborative Filtering
* **Reason**: Address the "cold start" problem for new hotels that lack user interaction data by recommending based on metadata and NLP features.
* **Impact**: Required extensive feature engineering (Stage 4) to ensure hotel profiles were sufficiently distinct.
* **Affected Files**: `content_based.py`

**DEC-005**
* **Decision**: Use SVD (Singular Value Decomposition)
* **Alternatives**: Neural Collaborative Filtering, k-NN
* **Reason**: SVD provides a proven, scalable baseline for matrix factorization in collaborative filtering.
* **Impact**: Implemented via the `surprise` library; formed the core of the collaborative filtering module.
* **Affected Files**: `collaborative.py`

**DEC-006**
* **Decision**: Replace Alpha-Blending Hybrid with RRF (Reciprocal Rank Fusion)
* **Alternatives**: Linear weighting (Alpha-Blending), Learning to Rank
* **Reason**: RRF is more robust when fusing scores from heterogeneous systems (Content-Based vs. Collaborative) that operate on different scales, removing the need to finely tune an alpha parameter.
* **Impact**: Simplified the hybrid recommender architecture and improved overall metrics.
* **Affected Files**: `hybrid.py`

**DEC-007**
* **Decision**: Reject SHAP
* **Alternatives**: LIME, Analytical Explainability
* **Reason**: SHAP is computationally expensive and difficult to integrate with a complex multi-stage hybrid (RRF) pipeline in a way that remains understandable to end-users.
* **Impact**: Pivot towards building a custom, rule-based analytical explainer.
* **Affected Files**: `explainer.py`

**DEC-008**
* **Decision**: Adopt Analytical Explainability
* **Alternatives**: SHAP, LIME
* **Reason**: Directly comparing a user's known preferences (e.g., high importance on "cleanliness") to a hotel's top features (e.g., high ABSA cleanliness score) produces highly readable, transparent, and auditable explanations.
* **Impact**: Explainability pipeline is decoupled from the ML model inference, improving speed.
* **Affected Files**: `explainer.py`

**DEC-009**
* **Decision**: Implement Explainability Audit
* **Alternatives**: Manual spot-checking
* **Reason**: TrustLayer-AI requires provable reliability. Automated auditing ensures that all generated explanations correctly map to underlying data without hallucination.
* **Impact**: Created a rigorous Stage B.1 validation process ensuring project health before UI development.
* **Affected Files**: `audit_explainability_b1.py`, `explainability_audit_b1.md`
