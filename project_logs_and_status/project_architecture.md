# Project Architecture

## System Architecture Diagram

```mermaid
graph TD
    subgraph Data Layer
        A[Google Places API] -->|fetch_google_places.py| C(delhi_hotels_raw.csv)
        B[Google Reviews API] -->|fetch_google_reviews.py| D(reviews_raw.csv)
        S1[Synthetic Users] -->|generate_users.py| S2(users.csv)
    end

    subgraph Processing Layer
        C -->|clean_hotel_metadata.py| E(delhi_hotels_cleaned.csv)
        D -->|clean_reviews.py| F(reviews_cleaned.csv)
    end

    subgraph NLP Layer
        F -->|analyze_sentiment.py| G1(Sentiment Scores)
        F -->|extract_absa_features.py| G2(Aspect-Based Sentiments)
        G1 --> H(review_features.csv)
        G2 --> H
    end

    subgraph Feature Engineering Layer
        E -->|engineer_features.py| I(hotel_features.csv)
        H -->|aggregate_reviews.py| J(hotel_review_summary.csv)
        I --> K{merge_dataset.py}
        J --> K
        K --> L[final_hotel_dataset.csv]
    end

    subgraph Interaction Layer
        S2 -->|generate_interactions.py| M1(interactions.csv)
        M1 -->|generate_interactions_v2.py| M2(interactions_v2.csv)
    end

    subgraph Recommendation Layer
        L -->|content_based.py| N1[Content-Based Model]
        M2 -->|collaborative.py| N2[Collaborative Model]
        M2 -->|baseline.py| N3[Baseline Model]
        N1 -->|hybrid.py| O[Hybrid RRF Model]
        N2 -->|hybrid.py| O
    end

    subgraph Explainability Layer
        L -->|explainer.py| P[Analytical Explainer]
        O -->|explainer.py| P
        P --> Q[Explainability Features / Text]
    end

    subgraph Evaluation Layer
        P -->|audit_explainability_b1.py| R[Audit Reports]
    end

    subgraph Future Layers
        Q --> Z1[RAG Layer]
        Q --> Z2[Dashboard Layer]
        Z1 --> Z3[Deployment Layer]
        Z2 --> Z3
    end
```

## Layer Details

### 1. Data Layer
Responsible for data acquisition. Interfaces with external APIs (Google Places) and handles raw data storage. Also responsible for generating synthetic user profiles to simulate a live platform.

### 2. Processing Layer
Handles all data sanitization, missing value imputation, string standardization, and duplicate removal. Ensures downstream pipelines receive robust data.

### 3. NLP Layer
Extracts semantic meaning from raw text. Utilizes pre-trained models to derive overall sentiment polarity and aspect-specific sentiments (e.g., cleanliness, location, service).

### 4. Feature Engineering Layer
Derives composite metrics (like Trust Score) and scales continuous variables. Aggregates NLP outputs at the hotel level and merges all data streams into a single `final_hotel_dataset.csv`.

### 5. Recommendation Layer
The core algorithmic engine. Utilizes a hybrid approach relying on Reciprocal Rank Fusion (RRF) to blend Content-Based filtering (metadata/NLP features) with Collaborative Filtering (matrix factorization on synthetic interactions).

### 6. Explainability Layer
An analytical rule engine that decouples from the ML inference. It compares the user's latent preference vectors to the recommended hotel's top features, generating natural language explanations for the recommendation.

### 7. Evaluation Layer
A suite of validation scripts and notebooks that compute offline metrics (Precision, Recall, NDCG), evaluate fairness/bias, and programmatically audit the explainability logic for hallucinations.

### 8. Future RAG Layer (Pending)
Will implement Retrieval-Augmented Generation using a Vector Database (e.g., FAISS, Pinecone) to allow users to query the hotel database via conversational LLM interface.

### 9. Future Dashboard Layer (Pending)
Will implement a UI (e.g., Streamlit, Next.js) to visualize recommendations and explanations interactively.

### 10. Future Deployment Layer (Pending)
Will containerize the API (Docker/FastAPI) and deploy the system to cloud infrastructure.
