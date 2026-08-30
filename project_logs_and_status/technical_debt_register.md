# Technical Debt Register

| Debt ID | Description | Stage Introduced | Impact | Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TD-001** | **Missing Amenities Data** <br> Google Places API lacks deep, granular amenities data (e.g., specific pool size, gym equipment) compared to specialized booking platforms. | Stage 1 (Collection) | Moderate. Limits the depth of content-based recommendations. | Medium | Open |
| **TD-002** | **Synthetic User Bias** <br> User interactions are simulated, meaning latent real-world behavioral quirks are not captured, potentially leading to a sterile collaborative filtering model. | Stage 5 (Simulation) | High. The model may not generalize perfectly to real user behavior upon launch. | High | Open |
| **TD-003** | **Limited Review Coverage** <br> Not all hotels have sufficient reviews to generate robust NLP and ABSA features. | Stage 3 (NLP) | Moderate. Affects explainability for cold-start hotels. | Medium | Open |
| **TD-004** | **Review Volume Cap** <br> Google API limitations meant capping the number of reviews pulled per hotel. | Stage 1 (Collection) | Low. A representative sample is usually sufficient for sentiment aggregation. | Low | Open |
| **TD-005** | **Explainability Coverage Gap** <br> For completely new users (pure cold-start), the explainer has limited preference data to match against hotel features. | Stage 7 (Explainability) | Moderate. Explanations default to global popularity metrics rather than personalized matches. | Medium | Open |
| **TD-006** | **Cold-Start Constraints** <br> Collaborative filtering still struggles with brand new hotels entering the platform. | Stage 6 (Recommender) | High. New inventory will not be recommended effectively without pure content-based boosting. | High | Open |

## Remediation Recommendations
* **TD-001**: Scrape or integrate secondary APIs (e.g., Booking.com) to enrich the `delhi_hotels_raw.csv` dataset.
* **TD-002**: Launch an A/B tested beta to collect real user telemetry, gradually phasing out `interactions_v2.csv`.
* **TD-003**: Implement fallback logic using aggregate area statistics for hotels missing review data.
* **TD-004**: Implement a periodic cron job to incrementally fetch and append new reviews over time.
* **TD-005**: Prompt new users for a 3-question onboarding survey (budget, preferred amenities) to immediately seed preferences.
* **TD-006**: Artificially boost the weight of the Content-Based recommender for items with < 5 interactions.
