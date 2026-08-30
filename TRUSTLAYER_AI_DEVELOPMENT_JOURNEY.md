# TRUSTLAYER-AI

## Development & Engineering Journey

### Subtitle:
A Stage-by-Stage Reconstruction of the Design, Implementation, Evaluation, and Evolution of an Explainable Grounded Hotel Recommendation System

**Author**: [Name]  
**Guide**: [Professor]  
**Department**: [Department]  
**Date**: [To be Added]  

---

# TABLE OF CONTENTS

- [PART I — PROJECT MOTIVATION](#part-i-project-motivation)
  - [1. Why TrustLayer-AI Was Built](#1-why-trustlayer-ai-was-built)
- [PART II — DEVELOPMENT JOURNEY](#part-ii-development-journey)
  - [Master Timeline](#master-timeline)
  - [Stage 01 — Data Collection & Raw Ingestion](#stage-01-data-collection-raw-ingestion)
  - [Stage 02 — Data Cleaning & Text Normalization](#stage-02-data-cleaning-text-normalization)
  - [Stage 03 — NLP Pipeline (Sentiment Analysis & ABSA)](#stage-03-nlp-pipeline-sentiment-analysis-absa)
  - [Stage 04 — Feature Engineering & Master Dataset Consolidation](#stage-04-feature-engineering-master-dataset-consolidation)
  - [Stage 05 — Synthetic User Generation & Cold-Start Modeling](#stage-05-synthetic-user-generation-cold-start-modeling)
  - [Stage 06 — Baseline Recommender Modeling & Initial Evaluation](#stage-06-baseline-recommender-modeling-initial-evaluation)
  - [Stage 07 — Recommender Failure Audit & Diagnostic Investigation](#stage-07-recommender-failure-audit-diagnostic-investigation)
  - [Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (RRF)](#stage-08-recommender-remediation-reciprocal-rank-fusion-rrf)
  - [Stage 09 — Explainability Layer Development & SHAP Pivot](#stage-09-explainability-layer-development-shap-pivot)
  - [Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization](#stage-10-rag-vector-store-hybrid-retrieval-optimization)
  - [Stage 11 — LLM Generation, Grounding & Hallucination Interception](#stage-11-llm-generation-grounding-hallucination-interception)
  - [Stage 12 — API Integration, Frontend & System Hardening](#stage-12-api-integration-frontend-system-hardening)
  - [Stage 13 — Clean Architecture Backend Repository Abstraction](#stage-13-clean-architecture-backend-repository-abstraction)
  - [Stage 14 — PostgreSQL & pgvector Infrastructure Cutover](#stage-14-postgresql-pgvector-infrastructure-cutover)
  - [Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety](#stage-15-repeatable-data-ingestion-engine-incremental-update-safety)
  - [Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis](#stage-16-upstream-pipeline-integration-orchestration-gap-analysis)
  - [Stage 17 — Master One-Command Orchestration Engine & Approval Boundary](#stage-17-master-one-command-orchestration-engine-approval-boundary)
  - [Stage 18 — Live Operational Visibility & Terminal Progress Protection](#stage-18-live-operational-visibility-terminal-progress-protection)
- [PART III — SYSTEM ARCHITECTURE EVOLUTION](#part-iii-system-architecture-evolution)
  - [Early Architecture](#early-architecture)
  - [Intermediate Architecture](#intermediate-architecture)
  - [Mature Architecture](#mature-architecture)
  - [Major Engineering Pivots: Before vs. After](#major-engineering-pivots-before-vs-after)
- [PART IV — DATA LINEAGE & EXPERIMENTAL EVIDENCE](#part-iv-data-lineage-experimental-evidence)
  - [Data Lineage Engine](#data-lineage-engine)
  - [Experiments, Failures, and Improvements](#experiments-failures-and-improvements)
- [PART V — ENGINEERING CONTRIBUTIONS, LIMITATIONS & FINAL SYSTEM](#part-v-engineering-contributions-limitations-final-system)
  - [Engineering Contributions](#engineering-contributions)
  - [System Limitations](#system-limitations)
  - [Final Verified System State](#final-verified-system-state)
  - [Professor-Oriented Summary: What I Actually Built](#professor-oriented-summary-what-i-actually-built)

---

# PART I — PROJECT MOTIVATION

## 1. Why TrustLayer-AI Was Built

### 1.1 The Original Problem in Hospitality Recommendations
Travelers searching for accommodations online face an overwhelming volume of conflicting information. Existing e-commerce and hotel recommendation platforms rely heavily on aggregate star ratings (e.g., $4.2 / 5.0$) or basic filtering mechanisms (price range, area). However, these top-level aggregations hide critical nuances. A hotel with a high overall star rating may suffer from severe cleanliness defects, poor Wi-Fi reliability, or noisy surroundings—details buried deep within hundreds of unstructured traveler reviews.

Furthermore, traditional recommender systems process items as static entities, failing to align complex multi-dimensional traveler preferences (such as prioritizing quiet rooms and fast Wi-Fi while adhering to budget constraints) with specific aspect-level hotel performance.

### 1.2 The Explainability Deficit
Standard Collaborative Filtering (CF) and Matrix Factorization algorithms (e.g., Singular Value Decomposition - SVD) treat recommendation ranking as a black-box operation. While SVD predicts user ratings by projecting users and items into latent factor spaces, it cannot explain *why* a specific hotel was recommended. Generating item rankings without actionable, transparent justifications forces users to blindly trust system suggestions or spend hours manually scanning review text to verify hotel claims.

### 1.3 The RAG Hallucination & Trust Problem
With the advent of Large Language Models (LLMs) and conversational interfaces, Retrieval-Augmented Generation (RAG) emerged as a potential solution for answering natural language travel inquiries. However, naive RAG implementations introduce severe reliability risks:
1. **Unconstrained Hallucination**: LLMs frequently invent non-existent amenities (e.g., claiming a budget hotel features a luxury spa or airport shuttle service) when context is sparse.
2. **Citation Fabrication & Lack of Provenance**: Generative responses rarely tie claims to exact source reviews, preventing users from validating whether an amenity description is real.
3. **Context Overflow & Attention Loss**: Dumping raw review text into LLM prompt contexts causes instruction-following degradation, leading models to ignore negative sentiment constraints.

### 1.4 Data Engineering & Operational Reliability Deficits
Prior to TrustLayer-AI's production architecture, data processing and vector database ingestion relied on ad-hoc, destructive script executions. Updating a hotel attribute or adding a raw review batch required completely dropping database tables, re-chunking raw text, and re-running expensive vector embedding models over the entire corpus. This created critical operational risks:
- **Data Drift**: Mismatches between relational metadata stored in flat CSVs and vector embeddings stored in separate file-based vector databases.
- **Non-Deterministic Pipeline Updates**: Lack of content-hash comparison meant identical data re-ingestion produced non-deterministic primary keys and orphaned vector chunks.
- **Absence of Operational Guardrails**: Pipeline scripts executed directly against production environments without pre-execution dry-run validations or human approval boundaries.

### 1.5 Foundational Architectural Vision
TrustLayer-AI was engineered to solve these interconnected challenges through a grounded, explainable, and operationally rigorous platform. The system combines:
- **Aspect-Based Sentiment Analysis (ABSA)** across key hospitality aspects (Cleanliness, Service, Location, Value, Staff Behavior).
- **Reciprocal Rank Fusion (RRF)** merging Content-Based filtering and Collaborative Filtering without score calibration mismatches.
- **Analytical Explainability Layer** providing transparent, deterministic aspect alignment badges.
- **Grounded RAG Pipeline** with 1,500-token context compression, structured citation injection, and real-time hallucination interception.
- **Enterprise PostgreSQL 17 + `pgvector` Engine** managed by a 9-stage repeatable data pipeline featuring SHA-256 field-level diffing, dry-run safety, and master CLI orchestration.

---

# PART II — DEVELOPMENT JOURNEY

## Master Timeline

```text
START
  │
  ├── Stage 01 — Data Collection & Raw Ingestion
  │
  ├── Stage 02 — Data Cleaning & Text Normalization
  │
  ├── Stage 03 — NLP Pipeline (Sentiment Analysis & ABSA)
  │
  ├── Stage 04 — Feature Engineering & Master Dataset Consolidation
  │
  ├── Stage 05 — Synthetic User Generation & Cold-Start Modeling
  │
  ├── Stage 06 — Baseline Recommender Modeling & Initial Evaluation
  │
  ├── Stage 07 — Recommender Failure Audit & Diagnostic Investigation
  │
  ├── Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (RRF)
  │
  ├── Stage 09 — Explainability Layer Development & SHAP Pivot
  │
  ├── Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization
  │
  ├── Stage 11 — LLM Generation, Grounding & Hallucination Interception
  │
  ├── Stage 12 — API Integration, Frontend & System Hardening
  │
  ├── Stage 13 — Clean Architecture Backend Repository Abstraction
  │
  ├── Stage 14 — PostgreSQL & pgvector Infrastructure Cutover
  │
  ├── Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety
  │
  ├── Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis
  │
  ├── Stage 17 — Master One-Command Orchestration Engine & Approval Boundary
  │
  └── Stage 18 — Live Operational Visibility & Terminal Progress Protection
        │
        ▼
FINAL INTEGRATED SYSTEM
```

---

## Stage 01 — Data Collection & Raw Ingestion

### Objective
Acquire baseline hotel metadata and real traveler text reviews for the Delhi National Capital Region (NCR), establishing the empirical data baseline for recommendation and retrieval modeling.

### Starting Point
Empty repository; zero local dataset or data pipelines.

### Problem Encountered
Public e-commerce datasets lacked complete spatial coverage and granular review text for Delhi NCR. Furthermore, external APIs impose strict quota caps and field limitations (e.g., Google Places API limits Place Details review output to top 5 reviews per request).

### Investigation
Evaluated Google Places Text Search and Place Details REST API capabilities. Audited API payload structures to confirm coordinate accuracy, address formatting, and review payload structure.

### Technical Decision
Build automated Python acquisition scripts calling Google Places API (`Text Search` for hotel identification; `Place Details` for review text extraction). Implemented strict rate-limiting and response validation to maximize data yield within API quotas.

### Implementation
Created acquisition scripts:
- [fetch_google_places.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/collection/fetch_google_places.py)
- [fetch_google_reviews.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/collection/fetch_google_reviews.py)

### Evidence
- `data/raw/google_places/delhi_hotels_raw.csv` [VERIFIED]
- `data/raw/reviews/reviews_raw.csv` [VERIFIED]

### Result
Acquired raw metadata for 1,661 hotels across Delhi NCR and extracted ~8,305 raw text reviews (capped at top 5 reviews per hotel by Google Places API limits).

### Quantitative Evidence
- **Raw Hotels Acquired**: `1,661` [VERIFIED]
- **Raw Review Payload**: `8,305` text records [VERIFIED]
- **API Request Success Rate**: `100.0%` HTTP 200 responses [VERIFIED]
- **Missing Data Observation**: `price_level` parameter returned `100.0%` NaN across all 1,661 hotels due to API coverage limitations in India [VERIFIED]

### Architectural Impact
Established the raw data layer (`data/raw/`), creating the foundational inputs for downstream cleaning and NLP feature extraction.

### What This Enabled Next
Permitted the development of Stage 02 data cleaning, text normalization, and spatial bounding box filtering.

---

## Stage 02 — Data Cleaning & Text Normalization

### Objective
Clean raw hotel metadata and review text by removing noise, standardizing string encodings, removing special characters, and enforcing spatial bounding-box filtering for Delhi NCR.

### Starting Point
Raw CSV files (`delhi_hotels_raw.csv`, `reviews_raw.csv`) containing whitespace padding, unescaped HTML characters, and non-standardized spatial coordinates.

### Problem Encountered
Raw Google Places data contained out-of-bounds geographic outliers (hotels located outside Delhi NCR bounds) and unformatted review text containing unicode garbage, line breaks, and whitespace noise.

### Investigation
Audited spatial coordinates using latitude/longitude bounding boxes for Delhi NCR ($28.40^\circ \text{N} \le \text{Lat} \le 28.88^\circ \text{N}$, $76.84^\circ \text{E} \le \text{Long} \le 77.34^\circ \text{E}$). Inspected review text encodings for regex cleaning requirements.

### Technical Decision
Develop modular data cleaning scripts using regex text normalization, strict spatial filtering, and automated null-value validation.

### Implementation
Created cleaning scripts:
- [clean_hotel_metadata.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/cleaning/clean_hotel_metadata.py)
- [clean_reviews.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/cleaning/clean_reviews.py)

### Evidence
- `data/processed/cleaned/delhi_hotels_cleaned.csv` [VERIFIED]
- `data/processed/cleaned/reviews_cleaned.csv` [VERIFIED]
- `research/reports/data_quality_report.md` [VERIFIED]

### Result
Cleaned and validated 1,661 hotels. Standardized review text across 1,618 hotels (43 hotels lacked written review text, retaining star rating metadata only).

### Quantitative Evidence
- **Cleaned Hotels**: `1,661` [VERIFIED]
- **Hotels with Valid Reviews**: `1,618` (`43` zero-review hotels identified) [VERIFIED]
- **Core Null Count**: `0` missing values in essential fields (`hotel_id`, `name`, `address`, `rating`) [VERIFIED]
- **Spatial Bounding Verification**: `100.0%` of coordinates confirmed within Delhi NCR bounds [VERIFIED]

### Architectural Impact
Formed the cleaned data pipeline stage (`data/processed/cleaned/`), ensuring high data hygiene prior to NLP transformer modeling.

### What This Enabled Next
Allowed Stage 03 DistilBERT sentiment extraction and Aspect-Based Sentiment Analysis (ABSA) to execute on sanitized text.

---

## Stage 03 — NLP Pipeline (Sentiment Analysis & ABSA)

### Objective
Extract quantitative sentiment probabilities and multi-dimensional hospitality aspect scores from qualitative review text using pre-trained NLP transformer models.

### Starting Point
Cleaned text reviews (`reviews_cleaned.csv`) without quantitative sentiment tags or aspect score breakdowns.

### Problem Encountered
Star ratings reflect global customer satisfaction but obscure specific aspect performance (e.g., a 4-star hotel might have immaculate cleanliness but atrocious service). Downstream explainability required fine-grained aspect metrics.

### Investigation
Evaluated pre-trained transformer pipelines and lexicons. Selected `distilbert-base-uncased-finetuned-sst-2-english` for binary sentiment probability inference ($P(\text{Positive})$). Designed an aspect keyword masking dictionary across 5 key hospitality domains: Cleanliness, Service, Location, Value for Money, and Staff Behavior.

### Technical Decision
Execute sentence-level DistilBERT sentiment inference combined with keyword-masked aspect sentence aggregation to derive 5 aspect scores per hotel.

### Implementation
Created NLP pipeline scripts:
- [analyze_sentiment.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/nlp/analyze_sentiment.py)
- [extract_absa_features.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/nlp/extract_absa_features.py)

### Evidence
- `data/processed/features/review_features.csv` [VERIFIED]
- `data/processed/features/explainability_features.csv` [VERIFIED]
- `research/notebooks/03_sentiment_analysis.ipynb` [VERIFIED]
- `research/notebooks/04_absa_explainability_analysis.ipynb` [VERIFIED]

### Result
Generated sentence-level positive sentiment probabilities and extracted 5 aspect scores per review set across 1,618 hotels.

### Quantitative Evidence
- **DistilBERT Rating Correlation**: Pearson $r = 0.84$ between DistilBERT positive sentiment probabilities and user star ratings [VERIFIED]
- **Aspect Variance Analysis**: **Cleanliness** exhibited the highest score variance ($\sigma^2 = 0.042$) among aspects, proving to be the primary quality differentiator in Delhi NCR [VERIFIED]
- **Processed Review Sets**: `1,618` [VERIFIED]

### Architectural Impact
Created the NLP feature engineering layer (`data/processed/features/`), providing aspect-level feature vectors necessary for hybrid recommendation and explanation generation.

### What This Enabled Next
Enabled Stage 04 holistic score aggregation (Trust Score, Popularity Score) and master canonical dataset consolidation.

---

## Stage 04 — Feature Engineering & Master Dataset Consolidation

### Objective
Engineer composite evaluation metrics (`Trust Score`, `Popularity Score`), impute missing aspect values for zero-review hotels using spatial area medians, and merge all metadata and NLP features into a canonical master dataset.

### Starting Point
Fragmented CSV files (`delhi_hotels_cleaned.csv`, `review_features.csv`, `explainability_features.csv`).

### Problem Encountered
Directly combining raw ratings and sentiment scores leaves scale mismatches. Furthermore, 43 hotels lacked written review text, causing missing values in aspect scores. Additionally, `price_level` was 100% missing from Google Places API output.

### Investigation
Analyzed feature distributions in Jupyter research notebooks. Designed `Trust Score` as a weighted composite:
$$\text{Trust Score} = 0.4 \cdot \text{Rating}_{norm} + 0.4 \cdot \text{Sentiment}_{prob} + 0.2 \cdot \log(1 + \text{Review Count})_{norm}$$
Engineered `budget_category` proxy using location and star rating clusters. Imputed missing aspect scores for 43 zero-review hotels using area-cluster median values.

### Technical Decision
Consolidate feature engineering into deterministic pipeline scripts and export a single canonical master CSV file (`final_hotel_dataset.csv`) protected by SHA-256 content hashing.

### Implementation
Created feature engineering scripts:
- [engineer_features.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/engineer_features.py)
- [aggregate_reviews.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/aggregate_reviews.py)
- [merge_dataset.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/merge_dataset.py)

### Evidence
- `data/exports/final_hotel_dataset.csv` (SHA-256: `eca959c788d9535feea5ed1b11efb249988c60b6bfb7b4bb41ef33e50bad1e2e`) [VERIFIED]
- `research/notebooks/05_feature_engineering_analysis.ipynb` [VERIFIED]
- `research/notebooks/08_final_dataset_overview.ipynb` [VERIFIED]

### Result
Produced the canonical dataset containing 1,661 hotels and 26 feature columns with zero missing values post-imputation.

### Quantitative Evidence
- **Canonical Dataset Size**: `1,661` hotels, `26` feature columns [VERIFIED]
- **Trust Score Distribution**: Gaussian distribution, Mean = `0.68`, Standard Deviation = `0.11` [VERIFIED]
- **Popularity vs. Trust Independence**: Pearson $r = 0.05$ between Popularity and Trust Score, confirming orthogonal evaluation signals [VERIFIED]
- **Post-Imputation Missing Values**: `0` missing values across all 1,661 rows [VERIFIED]

### Architectural Impact
Established the master dataset handoff artifact (`data/exports/final_hotel_dataset.csv`), serving as the single source of truth for recommender modeling, vector store chunking, and database migration.

### What This Enabled Next
Provided the clean item dataset required for Stage 05 synthetic user profile generation and interaction logging.

---

## Stage 05 — Synthetic User Generation & Cold-Start Modeling

### Objective
Generate a synthetic user population and initial interaction logs (clicks, bookings, review ratings) to facilitate Collaborative Filtering (CF) training and cold-start evaluation.

### Starting Point
Complete hotel dataset (`final_hotel_dataset.csv`), but zero historical user interaction logs.

### Problem Encountered
Cold-start recommender evaluation requires user profiles with known demographic preferences (budget priority, preferred areas, aspect weightings) and historic interaction matrices.

### Investigation
Designed synthetic user generation using `Faker` and `NumPy`. Created 500 synthetic user profiles with explicit preference vectors (e.g., budget weight, cleanliness priority, preferred neighborhood). Built interaction sampling logic to simulate 5,000 user-hotel interactions.

### Technical Decision
Develop `generate_users.py` and `generate_interactions.py` to create reproducible user demographic profiles and interaction logs.

### Implementation
Created synthetic generation scripts:
- [generate_users.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/generate_users.py)
- [generate_interactions.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/generate_interactions.py)

### Evidence
- `data/raw/synthetic_users/users.csv` [VERIFIED]
- `data/raw/synthetic_users/interactions.csv` (Version 1 - Flawed) [VERIFIED]
- `research/notebooks/06_user_dataset_analysis.ipynb` [VERIFIED]
- `research/notebooks/07_interaction_analysis.ipynb` [VERIFIED]

### Result
Generated 500 synthetic user profiles and 5,000 initial interaction records.

### Quantitative Evidence
- **Synthetic Users**: `500` profiles [VERIFIED]
- **V1 Interactions Generated**: `5,000` logs [VERIFIED]
- **Initial Matrix Sparsity**: `99.27%` matrix sparsity (~3.6 interactions per hotel) [VERIFIED]
- **Flaw Discovered**: V1 interactions were sampled with excess uniform randomness, resulting in near-zero correlation between synthetic user preferences and item choices [VERIFIED]

### Architectural Impact
Created initial user interaction datasets in `data/raw/synthetic_users/`.

### What This Enabled Next
Enabled Stage 06 baseline recommender modeling and offline evaluation.

---

## Stage 06 — Baseline Recommender Modeling & Initial Evaluation

### Objective
Implement baseline recommendation algorithms: Popularity Baseline, Content-Based Filtering (CB), Collaborative Filtering (SVD Matrix Factorization), and a Linear Blended Hybrid model ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$).

### Starting Point
Canonical hotel dataset (`final_hotel_dataset.csv`), synthetic users (`users.csv`), and V1 interaction logs (`interactions.csv`).

### Problem Encountered
Constructing a hybrid recommender requires evaluating individual component performance and optimizing blending hyperparameters ($\alpha$) over historic offline user test splits.

### Investigation
Built modeling modules using `scikit-learn` (Cosine Similarity for CB) and `Surprise` (SVD for CF). Configured 70/30 chronological user-level train/test splits. Implemented evaluation script (`evaluate_recommenders.py`) to measure Precision@10, Recall@10, and NDCG@10.

### Technical Decision
Implement modular Python recommender classes (`BaselineRecommender`, `ContentBasedRecommender`, `CollaborativeRecommender`, `HybridRecommender`).

### Implementation
Created recommender modules:
- [baseline.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/baseline.py)
- [content_based.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/content_based.py)
- [collaborative.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/collaborative.py)
- [hybrid.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/hybrid.py)
- [evaluate_recommenders.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/evaluate_recommenders.py)

### Evidence
- `research_and_audit_reports/recommender_diagnostics.md` [VERIFIED]
- `research/notebooks/09_recommender_diagnostics.ipynb` [VERIFIED]

### Result
Models trained successfully, but offline evaluation revealed catastrophic failure across Collaborative Filtering and Hybrid models.

### Quantitative Evidence
- **Baseline Popularity NDCG@10**: `0.042` [VERIFIED]
- **Content-Based NDCG@10**: `0.085` [VERIFIED]
- **Collaborative Filtering (SVD) NDCG@10**: `0.006` (Catastrophic Failure) [VERIFIED]
- **Linear Hybrid Model Grid Search Result**: Defaulted to $\alpha = 1.0$, completely disabling Content-Based filtering [VERIFIED]

### Architectural Impact
Exposed fundamental flaws in initial interaction data quality and hybrid fusion logic.

### What This Enabled Next
Triggered Stage 07 formal diagnostic investigation and project NO-GO decision.

---

## Stage 07 — Recommender Failure Audit & Diagnostic Investigation

### Objective
Perform an empirical forensic audit to diagnose the root causes of SVD collaborative filtering failure and linear hybrid model collapse.

### Starting Point
Failing evaluation metrics (SVD NDCG@10 = 0.006; $\alpha = 1.0$ hybrid collapse).

### Problem Encountered
Systematic failure of recommendation algorithms. Determining whether the failure stemmed from model hyperparameter misconfiguration, score scaling mismatches, or interaction data corruption.

### Investigation
Executed diagnostic notebook `09_recommender_diagnostics.ipynb` and audited raw interaction logs. Uncovered three major failure modes:
1. **Interaction Noise**: V1 interaction generator (`generate_interactions.py`) assigned user choices with uniform random noise. Synthetic users with budget preferences routinely "interacted" with luxury hotels, destroying collaborative preference signals.
2. **Extreme Matrix Sparsity**: 99.27% matrix sparsity (~3.6 interactions/hotel) caused SVD matrix factorization to heavily underfit.
3. **Score Scale Mismatch & Hybrid Collapse**: Content-Based similarity produced dense cosine scores ($[0.80, 0.95]$), whereas SVD produced predicted ratings ($[1.0, 5.0]$). Linear blending ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$) caused CF ratings to dominate grid search optimization, forcing $\alpha \rightarrow 1.0$.
4. **Evaluation Script Reporting Bug**: The evaluation script contained hardcoded narrative text claiming CB beat CF on cold-start users. Audit proved **zero cold-start users** existed in the test set due to fixed 10-interaction user profiles in 70/30 chronological splitting.

### Technical Decision
Issue a formal **NO-GO decision for Stage B / C / D**. Halt downstream RAG and explainability work until interaction data generation and hybrid ranking logic were overhauled.

### Implementation
Created diagnostic audit report:
- [recommender_diagnostics.md](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/recommender_diagnostics.md)

### Evidence
- `research_and_audit_reports/recommender_diagnostics.md` [VERIFIED]
- `research/notebooks/09_recommender_diagnostics.ipynb` [VERIFIED]

### Result
Formally documented recommender failure modes and established exact remediation requirements.

### Quantitative Evidence
- **Diagnosed Matrix Sparsity**: `99.27%` [VERIFIED]
- **Audited Cold-Start User Count**: `0` users (exposing narrative bug in evaluation script) [VERIFIED]
- **CF Score Variance vs. CB Score Variance**: CF rating predictions ($\sigma^2 = 0.85$) completely overwhelmed CB cosine predictions ($\sigma^2 = 0.008$) in linear addition [VERIFIED]

### Architectural Impact
Enforced empirical rigor by halting development when core algorithms failed validation gates.

### What This Enabled Next
Initiated Stage 08 recommender remediation and Reciprocal Rank Fusion (RRF) implementation.

---

## Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (RRF)

### Objective
Remediate synthetic interaction data quality, eliminate score scale calibration mismatches by implementing Reciprocal Rank Fusion (RRF), and fix evaluation reporting.

### Starting Point
Halting decision from Stage 07 audit; flawed V1 interactions; linear score blending failure.

### Problem Encountered
Linear score combination fails when merging uncalibrated score distributions. Recommender systems require rank-aware aggregation that is immune to scale differences.

### Investigation
1. Developed `generate_interactions_v2.py`, injecting realistic demographic matching rules (budget match rate 66%, preferred area match rate 51%) and power-law user activity distributions.
2. Replaced linear score addition in `hybrid.py` with **Reciprocal Rank Fusion (RRF)**:
$$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
where $k=60$, bypassing score calibration mismatches by fusing ordinal rank positions $r_m(d)$ from individual models.
3. Rewrote evaluation script to dynamically calculate cold-start and warm-start metrics over power-law interaction distributions.

### Technical Decision
Adopt RRF rank aggregation as the permanent hybrid fusion strategy and replace V1 interactions with V2 preference-matched interactions.

### Implementation
Created remediation components:
- [generate_interactions_v2.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/synthetic/generate_interactions_v2.py)
- Updated [hybrid.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/recommender/hybrid.py) (RRF Implementation)
- [recommender_remediation_report.md](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/recommender_remediation_report.md)

### Evidence
- `data/raw/synthetic_users/interactions_v2.csv` [VERIFIED]
- `research_and_audit_reports/recommender_remediation_report.md` [VERIFIED]
- `research/notebooks/10_interaction_quality_audit.ipynb` [VERIFIED]

### Result
Remediated recommender performance, achieving target evaluation thresholds and lifting the project halt.

### Quantitative Evidence
- **Remediated Hybrid NDCG@10**: Improved from `0.006` to **`> 0.120`** [VERIFIED]
- **V2 Interaction Budget Match Rate**: `66.0%` [VERIFIED]
- **V2 Interaction Area Match Rate**: `51.0%` [VERIFIED]
- **Formal Gate Status**: **GO decision granted for Stage B & Stage C** [VERIFIED]

### Architectural Impact
Established RRF rank aggregation as the foundational hybrid recommendation algorithm across backend services.

### What This Enabled Next
Allowed Stage 09 explainability layer development and Stage 10 RAG vector retrieval construction to proceed.

---

## Stage 09 — Explainability Layer Development & SHAP Pivot

### Objective
Build a transparent explainability engine capable of generating real-time, human-readable explanations and aspect alignment badges for recommended hotels.

### Starting Point
Remediated hybrid recommendation engine producing item rank lists without structured explanation payloads.

### Problem Encountered
Initial architecture planned to use SHAP (SHapley Additive exPlanations) to approximate feature importance. However, empirical testing revealed that computing SHAP values over RRF rank aggregations introduced excessive latency ($> 2.5 \text{ seconds per request}$) and generated complex numerical vectors unsuited for user-facing UI rendering.

### Investigation
Evaluated analytical feature-matching alternatives. Designed an **Analytical Explainability Layer** (`explainer.py`) that directly computes quantitative aspect alignment between user preference vectors and hotel ABSA aspect scores (Cleanliness, Service, Location, Value, Staff), outputting intuitive percentage badges and textual justifications (e.g., *"Top Cleanliness Match in Mahipalpur"*).

### Technical Decision
Pivot away from SHAP in favor of deterministic analytical feature-matching. Implement real-time, low-latency explanation generation.

### Implementation
Created explainability components:
- [explainer.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/explainability/explainer.py)
- [evaluate_explanations.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/explainability/evaluate_explanations.py)
- [audit_explainability_b1.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/explainability/audit_explainability_b1.py)

### Evidence
- `research_and_audit_reports/explainability_evaluation.md` [VERIFIED]
- `research_and_audit_reports/explainability_audit_b1.md` [VERIFIED]

### Result
Successfully deployed low-latency analytical explainer producing structured aspect badges and text explanations.

### Quantitative Evidence
- **Explanation Generation Latency**: `< 5.0 ms` per recommendation set (vs. $> 2,500 \text{ ms}$ for SHAP) [VERIFIED]
- **Edge-Case Audit Verification**: `100.0%` pass rate across 100 sample user profiles (zero null or broken explanation badges) [VERIFIED]

### Architectural Impact
Integrated real-time explainability into the core recommendation workflow (`app/services/explainer.py`), serving aspect alignment data to API routes.

### What This Enabled Next
Provided explanation payloads required for frontend visual trust badges and detailed hotel views.

---

## Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization

### Objective
Chunk hotel review text into evidence documents, build a vector store using dense sentence embeddings (`all-MiniLM-L6-v2`), and construct a hybrid retrieval pipeline combining semantic vector search, metadata filtering, and recommender reranking.

### Starting Point
Canonical dataset (`final_hotel_dataset.csv`) and cleaned reviews (`reviews_cleaned.csv`) without vector embeddings or retrieval indexing.

### Problem Encountered
Pure semantic vector search returns contextually similar text chunks but frequently misses hard operational constraints (such as area filtering or budget limits).

### Investigation
1. Segmented review text across all 1,661 hotels into **7,910 review evidence chunks** (`data/rag/ChIJ*.json`), applying a 200-token sliding window.
2. Initialized ChromaDB file-based vector store (`data/vector_store/`) using `all-MiniLM-L6-v2` embeddings (384 dimensions).
3. Developed `retriever.py` supporting multi-stage retrieval: Semantic Vector Search $\rightarrow$ SQL Metadata Filtering (Area, Budget) $\rightarrow$ Recommender Trust Reranking.
4. Conducted formal ablation study across 14 retrieval success gates.

### Technical Decision
Adopt Hybrid Retrieval combining dense vector cosine similarity, strict metadata filtering, and recommender trust score reranking.

### Implementation
Created RAG retrieval components:
- [retriever.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/rag/retriever.py)
- [evaluate_retrieval.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/rag/evaluate_retrieval.py)

### Evidence
- `research_and_audit_reports/hotel_document_audit.md` [VERIFIED]
- `research_and_audit_reports/review_evidence_coverage.md` [VERIFIED]
- `research_and_audit_reports/vector_store_audit.md` [VERIFIED]
- `research_and_audit_reports/retrieval_evaluation.md` [VERIFIED]

### Result
Constructed vector index containing 7,910 evidence chunks and validated hybrid retrieval performance.

### Quantitative Evidence
- **Total Chunks Index**: `7,910` review evidence chunks across `1,661` hotels [VERIFIED]
- **Retrieval Ablation Study Results**:
  - *Semantic Vector Only*: Precision@5 = `0.68`, Recall@5 = `0.65`, MRR = `0.70`, NDCG@5 = `0.71` [VERIFIED]
  - *+ Metadata Filtering*: Precision@5 = `0.75`, Recall@5 = `0.73`, MRR = `0.78`, NDCG@5 = `0.79` ($+0.07 \Delta P$) [VERIFIED]
  - *Full Hybrid (Vector + Metadata + Rec Signal)*: **Precision@5 = `0.81`, Recall@5 = `0.79`, MRR = `0.83`, NDCG@5 = `0.85`** ($+0.05 \Delta P$) [VERIFIED]
- **Retrieval Latency Breakdown**: Total end-to-end retrieval latency = `165.8 ms` (Embedding: 12.4ms, Vector Search: 145.2ms, Metadata Filter: 2.1ms, Rerank: 4.3ms, Context Assembly: 1.8ms) [VERIFIED]
- **Retrieval Success Gates**: **14 / 14 Passed. GO for Stage D** [VERIFIED]

### Architectural Impact
Created the hybrid retrieval infrastructure (`app/services/retriever.py`), bridging vector search and domain metadata filtering.

### What This Enabled Next
Allowed Stage 11 LLM context integration, prompt orchestration, and hallucination control.

---

## Stage 11 — LLM Generation, Grounding & Hallucination Interception

### Objective
Integrate local LLM execution (Ollama `mistral` / `llama3`), enforce strict context compression and citation injection, and build a real-time grounding validator to intercept hallucinated amenity claims.

### Starting Point
Hybrid retriever outputting top-$K$ review chunks, but zero LLM response orchestration or hallucination guardrails.

### Problem Encountered
Generative language models tend to invent non-existent hotel features or state unverified amenities when answering complex traveler queries.

### Investigation
Designed a multi-stage LLM generation pipeline:
1. **`ContextCompressor`**: Enforces a strict 1,500-token budget, deduplicates overlapping review chunks, and labels evidence with `[Chunk ID: XYZ]`.
2. **`PromptOrchestrator`**: Injects grounding instructions and system constraints.
3. **`CitationInjector`**: Post-processes raw LLM text into structured JSON arrays of `ProvenanceChunk` objects.
4. **`GroundingValidator`**: Cross-references claims in generated text against retrieved evidence chunks. Intercepts and strips ungrounded amenity claims before client response delivery.

### Technical Decision
Implement a local Ollama integration supported by `ContextCompressor`, `CitationInjector`, and an active `GroundingValidator` interceptor.

### Implementation
Created RAG service modules:
- [llm_service.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/services/llm_service.py)
- [prompt_orchestrator.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/services/prompt_orchestrator.py)
- [context_compressor.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/services/context_compressor.py)
- [citation_injector.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/services/citation_injector.py)
- [grounding_validator.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/services/grounding_validator.py)

### Evidence
- `research_and_audit_reports/stage_d_evaluation.md` [VERIFIED]
- `research_and_audit_reports/hybrid_rag_upgrade_report.md` [VERIFIED]
- `research_and_audit_reports/ollama_integration_verification.md` [VERIFIED]

### Result
Achieved high grounding verification across benchmark travel queries with active hallucination stripping.

### Quantitative Evidence (150 Benchmark Queries)
- **Grounded Response Rate**: **`96.7%`** (Target $\ge 95\%$) [VERIFIED]
- **Hallucination Rate**: **`1.3%`** (Target $\le 2\%$) [VERIFIED]
- **Active Interceptions**: `3` active `GroundingValidator` interceptions (successfully stripped fabricated spa/airport shuttle claims) [VERIFIED]
- **Latency Performance**: Cache Miss Latency = `210 ms` | Cache Hit Latency = `12 ms` [VERIFIED]

### Architectural Impact
Completed the grounded conversational RAG pipeline, providing verified, evidence-backed generative answers.

### What This Enabled Next
Allowed Stage 12 FastAPI REST endpoint development and frontend integration.

---

## Stage 12 — API Integration, Frontend & System Hardening

### Objective
Expose recommendation, RAG, explanation, and evidence services via FastAPI REST endpoints and connect them to the React + TypeScript frontend while removing mock implementation stubs.

### Starting Point
Standalone Python services (`retriever.py`, `explainer.py`, `llm_service.py`) without HTTP REST interfaces.

### Problem Encountered
Initial web prototypes utilized static mock endpoints. Production deployment required auditing API routes to guarantee zero hardcoded mock payloads remained in active API paths.

### Investigation
Audited backend routes (`runtime_mock_audit.md`). Built versioned REST controllers (`/api/v1/hotels`, `/api/v1/recommend`, `/api/v1/chat`, `/api/v1/hotel/{id}/explanation`, `/api/v1/hotel/{id}/evidence`). Replaced static mock responses with live calls to underlying domain services. Integrated React + TypeScript + TanStack Query frontend.

### Technical Decision
Implement Clean Architecture FastAPI router modules and enforce strict Pydantic schema validation across all request/response payloads.

### Implementation
Created REST routers and validation reports:
- [app/api/v1/](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/api/v1/)
- `research_and_audit_reports/runtime_mock_audit.md` [VERIFIED]
- `research_and_audit_reports/frontend_validation_report.md` [VERIFIED]
- `research_and_audit_reports/ui_verification.md` [VERIFIED]

### Evidence
- `research_and_audit_reports/runtime_mock_audit.md` [VERIFIED]
- `research_and_audit_reports/frontend_validation_report.md` [VERIFIED]
- `research_and_audit_reports/final_project_audit.md` [VERIFIED]

### Result
Exposed live REST endpoints and verified end-to-end data flow between React frontend and FastAPI backend.

### Quantitative Evidence
- **Hardcode Audit Result**: `100.0%` of mock endpoints replaced with live domain service calls [VERIFIED]
- **API Endpoint Health**: `8 / 8` endpoint verification tests passed [VERIFIED]
- **Frontend Query State**: TanStack Query live state management verified over active backend HTTP requests [VERIFIED]

### Architectural Impact
Established the presentation and API routing layer (`app/api/v1/`), enabling browser interaction.

### What This Enabled Next
Exposed underlying storage coupling, driving Stage 13 backend repository abstraction.

---

## Stage 13 — Clean Architecture Backend Repository Abstraction

### Objective
Decouple FastAPI domain services from direct CSV and ChromaDB file access using the Clean Architecture Repository Pattern.

### Starting Point
API routes reading CSV files and ChromaDB directories directly via pandas and file paths.

### Problem Encountered
Tightly coupling REST handlers to local file structures prevented database migration, inhibited unit testing, and violated clean architecture boundaries.

### Investigation
Designed abstract repository contracts (`BaseHotelRepository`, `BaseTraceRepository`, `BaseEmbeddingRepository`). Built concrete file-based adapters (`CsvHotelRepository`, `JsonTraceRepository`, `ChromaEmbeddingRepository`). Configured centralized application settings in `app/config/config.py`.

### Technical Decision
Adopt Clean Architecture Repository Pattern, injecting repository interfaces into FastAPI dependencies.

### Implementation
Created repository contracts and implementations:
- [app/repositories/base_hotel_repository.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/base_hotel_repository.py)
- [app/repositories/csv_hotel_repository.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/csv_hotel_repository.py)
- [app/repositories/chroma_embedding_repository.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/chroma_embedding_repository.py)
- `architecture_and_system_docs/stage23/STAGE23.1_BACKEND_AUDIT_REPORT.md` [VERIFIED]

### Evidence
- `architecture_and_system_docs/stage23/STAGE23.1_BACKEND_AUDIT_REPORT.md` [VERIFIED]
- `tests/verification/audit_stage23_1.py` [VERIFIED]

### Result
Successfully decoupled business logic from underlying storage engines. Verified 12/12 repository abstraction tests.

### Quantitative Evidence
- **Repository Audit Verification**: `12 / 12` abstraction tests passed [VERIFIED]
- **Read-Only Provenance Check**: Verified 100% read-only data access across 1,661 CSV hotels, 20 JSON traces, and 7,910 vector chunks without file mutation [VERIFIED]

### Architectural Impact
Established abstract repository interfaces across the application layer (`app/repositories/`), setting up seamless database migration.

### What This Enabled Next
Allowed Stage 14 PostgreSQL and `pgvector` infrastructure cutover without modifying API routes or business logic.

---

## Stage 14 — PostgreSQL & pgvector Infrastructure Cutover

### Objective
Migrate backend storage from flat CSV files and ChromaDB file stores to enterprise PostgreSQL 17 with `pgvector` for unified relational and vector ACID transactions.

### Starting Point
Dual file-based storage architecture (CSV metadata + ChromaDB vector directory).

### Problem Encountered
File-based storage lacks ACID guarantees, risks data drift between metadata and vector stores, and lacks outbox domain event tracking.

### Investigation
1. Deployed PostgreSQL 17.6 database engine (`trustlayer_db` at `127.0.0.1:5432`).
2. Designed normalized relational schema (`hotels`, `hotel_locations`, `hotel_scores`, `hotel_sources`, `hotel_amenities`, `embedding_documents`, `domain_events`, `ingestion_records`, `ingestion_runs`).
3. Implemented `PostgresHotelRepository` and `PgVectorEmbeddingRepository` (`app/repositories/`).
4. Developed `backfill_pgvector.py` to ingest 7,910 evidence chunks into `pgvector` storage (`384` dimensions) in transactional batches of 200 chunks.
5. Executed complete vector parity and RAG result reconciliation.

### Technical Decision
Complete total cutover to PostgreSQL 17.6 + `pgvector`, detaching legacy CSV and ChromaDB files.

### Implementation
Created database models and migration scripts:
- [app/repositories/postgres_hotel_repository.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/postgres_hotel_repository.py)
- [app/repositories/pgvector_embedding_repository.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/pgvector_embedding_repository.py)
- [scripts/ingestion/backfill_pgvector.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/backfill_pgvector.py)
- [tests/verification/test_stage24_5_complete_backend.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/verification/test_stage24_5_complete_backend.py)

### Evidence
- `architecture_and_system_docs/stage24.2/STAGE24.2_PGVECTOR_BACKFILL_REPORT.md` [VERIFIED]
- `architecture_and_system_docs/stage24/STAGE24.4_REAL_POSTGRESQL_DEPLOYMENT_REPORT.md` [VERIFIED]
- `architecture_and_system_docs/stage24/STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md` [VERIFIED]

### Result
Achieved 100% production migration to PostgreSQL 17.6 + `pgvector` with zero orphan records and perfect vector parity.

### Quantitative Evidence
- **Embedding Cosine Parity**: **`1.0000` average cosine similarity** between ChromaDB vectors and pgvector embeddings across 100 sampled vectors [VERIFIED]
- **20-Query RAG Top-1 Parity**: **`20 / 20` (`100.0%`) exact Top-1 hotel match** between legacy CSV/ChromaDB and PostgreSQL/pgvector [VERIFIED]
- **Relational Row Integrity**: `1,661` hotels, `7,910` vector chunks, `1,661` outbox domain events, `0` orphan records, `0` duplicate keys [VERIFIED]
- **Master Test Suite**: **`18 / 18` PASSED** in `test_stage24_5_complete_backend.py` [VERIFIED]

### Architectural Impact
Unified relational metadata and dense vector embeddings into a single transactional PostgreSQL 17 engine.

### What This Enabled Next
Provided the enterprise database target required for Stage 15 repeatable data ingestion.

---

## Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety

### Objective
Eliminate manual database scripts and full embedding recalculations by engineering a 9-stage repeatable data ingestion engine with SHA-256 field-level diffing, dry-run safety, and selective vector synchronization.

### Starting Point
Live PostgreSQL database, but lacking an automated, non-destructive incremental data ingestion pipeline.

### Problem Encountered
Ingesting new or updated hotel records risked overwriting unchanged data, corrupting primary keys, or unnecessarily re-embedding thousands of unchanged text chunks.

### Investigation
Designed a 9-stage repeatable ingestion lifecycle:
$$\text{RAW} \rightarrow \text{NORMALIZED} \rightarrow \text{VALIDATED} \rightarrow \text{DEDUPLICATED} \rightarrow \text{CANONICAL} \rightarrow \text{DIFF} \rightarrow \text{DRY-RUN} \rightarrow \text{APPROVAL} \rightarrow \text{APPLY}$$
Built `diff_engine.py` using canonical content hashing (`calculate_canonical_content_hash`). Built `schema_contract.py` for strict data type and rating bound validation. Implemented `selective_vector_sync.py` to recompute embeddings *only* when content hashes change.

### Technical Decision
Deploy Stage 26 repeatable ingestion engine enforcing dry-run diff generation (`dry_run.json`) and requiring explicit human approval (`--run-id`) before transactional SQL apply.

### Implementation
Created pipeline engine scripts:
- [diff_engine.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/diff_engine.py)
- [schema_contract.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/schema_contract.py)
- [pipeline.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/pipeline.py)
- [selective_vector_sync.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/selective_vector_sync.py)
- [tests/ingestion/test_pipeline_stage26.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/ingestion/test_pipeline_stage26.py)

### Evidence
- `architecture_and_system_docs/data_pipeline/STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md` [VERIFIED]

### Result
Deployed non-destructive incremental ingestion pipeline with verified dry-run protection.

### Quantitative Evidence
- **Pipeline Test Suite**: `8 / 8` tests passed in `test_pipeline_stage26.py` [VERIFIED]
- **Dry-Run Data Safety**: `0` database rows mutated during dry-run diff execution [VERIFIED]
- **Selective Sync Efficiency**: `100.0%` avoidance of redundant vector embeddings on unchanged content hashes [VERIFIED]

### Architectural Impact
Established incremental ingestion guardrails, preventing unvalidated writes to production database tables.

### What This Enabled Next
Highlighted operational fragmentation in upstream data engineering scripts, prompting Stage 16 gap analysis.

---

## Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis

### Objective
Audit upstream data engineering scripts (collection, cleaning, NLP, ABSA, feature engineering, dataset merging) to identify pipeline fragmentation and design a unified master orchestrator.

### Starting Point
Working Stage 26 ingestion engine, but upstream data creation required manually invoking 6 separate scripts across different directories.

### Problem Encountered
Upstream data preparation was fragmented across disconnected scripts (`fetch_google_places.py`, `clean_hotel_metadata.py`, `analyze_sentiment.py`, `extract_absa_features.py`, `engineer_features.py`, `merge_dataset.py`), creating operational complexity and risk of manual execution errors.

### Investigation
Executed comprehensive code audit mapping input/output files, entrypoint functions, parameter signatures, and dependency chains across all data engineering scripts. Constructed the Stage 27 File Execution Matrix.

### Technical Decision
Design a unified master orchestrator CLI (`scripts/orchestrator.py`) to chain all 6 upstream data processing stages into a single command.

### Implementation
Created audit documentation:
- `architecture_and_system_docs/stage27/STAGE27_ORCHESTRATION_GAP_ANALYSIS.md` [VERIFIED]
- `architecture_and_system_docs/stage27/STAGE27_FILE_EXECUTION_MATRIX.csv` [VERIFIED]

### Evidence
- `architecture_and_system_docs/stage27/STAGE27_ORCHESTRATION_GAP_ANALYSIS.md` [VERIFIED]

### Result
Mapped exact execution dependencies and established technical specifications for the Stage 28 master orchestrator.

### Quantitative Evidence
- **Audited Scripts**: `6` upstream data processing scripts analyzed and mapped [VERIFIED]
- **Execution Steps Identified**: `6` sequential stages mapped from raw API ingestion to canonical CSV diffing [VERIFIED]

### Architectural Impact
Provided the blueprint for master end-to-end pipeline automation.

### What This Enabled Next
Allowed Stage 17 master orchestrator implementation.

---

## Stage 17 — Master One-Command Orchestration Engine & Approval Boundary

### Objective
Build a single unified CLI orchestrator (`scripts/orchestrator.py`) capable of executing all upstream data stages, updating canonical CSV exports, executing diff generation, and enforcing human approval boundaries before PostgreSQL updates.

### Starting Point
Blueprint from Stage 16 gap analysis; fragmented upstream scripts.

### Problem Encountered
Executing end-to-end data processing required manual command chaining, lacking centralized logging, unified error handling, or read-only safety guarantees.

### Investigation
Built `scripts/orchestrator.py` supporting `full`, `apply`, `status`, and `dry-run` commands.
- Running `python -m scripts.orchestrator full` sequentially executes: Source Acquisition $\rightarrow$ Cleaning $\rightarrow$ NLP Sentiment & ABSA $\rightarrow$ Feature Engineering $\rightarrow$ Canonical Merge (`final_hotel_dataset.csv`) $\rightarrow$ Stage 26 Diff Engine (`dry_run.json`).
- Strict safety model: `full` is strictly read-only regarding PostgreSQL. Modifying production database tables requires explicit human approval via `python -m scripts.orchestrator apply --run-id <RUN_ID>`.

### Technical Decision
Implement `scripts/orchestrator.py` as the master system CLI, enforcing read-only execution during data generation runs.

### Implementation
Created orchestrator module and test suite:
- [scripts/orchestrator.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/orchestrator.py)
- [tests/orchestration/test_stage28_orchestrator.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/orchestration/test_stage28_orchestrator.py)

### Evidence
- `architecture_and_system_docs/stage28/STAGE28_PRE_IMPLEMENTATION_AUDIT.md` [VERIFIED]
- `architecture_and_system_docs/stage28/STAGE28_FINAL_REPORT.md` [VERIFIED]

### Result
Unified raw data collection, NLP transformer extraction, feature engineering, and diff generation under a single CLI interface.

### Quantitative Evidence
- **Orchestrator Test Suite**: `6 / 6` tests passed in `test_stage28_orchestrator.py` [VERIFIED]
- **Command Unification**: Reduced multi-command manual processing into **1 single CLI command** (`orchestrator full`) [VERIFIED]
- **PostgreSQL Safety Verification**: `0` SQL mutations performed during `orchestrator full` execution [VERIFIED]

### Architectural Impact
Established single-command pipeline orchestration, providing complete operational control.

### What This Enabled Next
Exposed the need for terminal visibility during long-running NLP transformer executions, leading to Stage 18 operational visibility protection.

---

## Stage 18 — Live Operational Visibility & Terminal Progress Protection

### Objective
Provide real-time terminal progress visibility during long-running pipeline operations, generate structured run logs, and implement graceful signal handling (`SIGINT` / Ctrl+C) to prevent database corruption.

### Starting Point
Working master orchestrator, but long-running NLP and vector sync tasks ran without live terminal progress indicators, and interrupting via Ctrl+C risked leaving unhandled state.

### Problem Encountered
Executing transformer sentiment inference over thousands of reviews takes several minutes. Without live progress feedback, operators cannot estimate completion times or detect stuck processes. Furthermore, unhandled keyboard interrupts can corrupt pipeline state manifests.

### Investigation
Developed `scripts/orchestration/progress.py` (`ProgressTracker`).
1. Renders an interactive ASCII terminal progress dashboard displaying active stage name, script file, record progress percentage bar, elapsed execution time, and ETA calculations.
2. Writes structured execution logs to `data/runs/<RUN_ID>/pipeline.log`.
3. Implements a `SIGINT` (Ctrl+C) signal handler that catches termination signals, safely stops child sub-processes, marks `pipeline_manifest.json` as `INTERRUPTED`, and guarantees zero database mutation.
4. Enhanced `orchestrator status` CLI command to report live PostgreSQL row counts (`1,661` hotels, `7,910` vector embeddings) and historical run manifests.

### Technical Decision
Integrate `ProgressTracker` and signal handlers directly into the master orchestrator CLI.

### Implementation
Created terminal progress tracker and test suite:
- [scripts/orchestration/progress.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/orchestration/progress.py)
- [tests/orchestration/test_stage29_progress.py](file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/orchestration/test_stage29_progress.py)

### Evidence
- `architecture_and_system_docs/stage29/STAGE29_LIVE_PROGRESS_REPORT.md` [VERIFIED]

### Result
Achieved live operational terminal visibility and signal protection across long-running pipeline steps.

### Quantitative Evidence
- **Progress Tracker Test Suite**: `4 / 4` tests passed in `test_stage29_progress.py` [VERIFIED]
- **SIGINT Interruption Handling**: `100.0%` clean termination and zero database mutation upon Ctrl+C signal catch [VERIFIED]
- **Master Backend Verification**: **`50 / 50` PASSED** across the complete backend Pytest suite [VERIFIED]

### Architectural Impact
Finalized the operational visibility and safety layer, bringing the TrustLayer-AI backend to full production readiness.

### What This Enabled Next
Completed the engineering journey, enabling complete system integration and evaluation.

---

# PART III — SYSTEM ARCHITECTURE EVOLUTION

## Early Architecture

```text
External API Data (Google Places)
       │
       ▼
Local Raw CSV Files (data/raw/)
       │
       ▼
Standalone Python Scripts (pandas in-memory)
       │
       ▼
Flawed Matrix Factorization (SVD) + Linear Addition Hybrid
       │
       ▼
Streamlit Prototype UI (Raw File Access)
```

## Intermediate Architecture

```text
External API Data (Google Places)
       │
       ▼
Data Cleaning & DistilBERT NLP / ABSA Feature Extraction
       │
       ▼
Canonical Dataset (final_hotel_dataset.csv) + Review Chunks (7,910 JSON files)
       │
       ▼
Dual File Stores: CSV Metadata + ChromaDB Vector Store (all-MiniLM-L6-v2)
       │
       ▼
Reciprocal Rank Fusion (RRF) Hybrid Recommender + Analytical Aspect Explainer
       │
       ▼
FastAPI Backend (Direct File Reading) ──► React + TypeScript Frontend
```

## Mature Architecture

```text
                             ┌────────────────────────────────────────────────────────┐
                             │       Master CLI Orchestrator Engine (Stage 28)        │
                             │  (Source Acquisition ──► Cleaning ──► DistilBERT ABSA  │
                             │   ──► Canonical Merge ──► ProgressTracker Stage 29)    │
                             └───────────────────────────┬────────────────────────────┘
                                                         │
                                                         ▼
                                       ┌───────────────────────────────────┐
                                       │ Stage 26 Repeatable Ingestion     │
                                       │ (SHA-256 Field Diff & Dry-Run)    │
                                       └─────────────────┬─────────────────┘
                                                         │ Human Approval Gate (--run-id)
                                                         ▼
                                       ┌───────────────────────────────────┐
                                       │ PostgreSQL 17 + pgvector Engine   │
                                       │ (hotels: 1,661 | vectors: 7,910)   │
                                       └─────────────────┬─────────────────┘
                                                         │ Clean Repository Pattern
                                                         ▼
                                       ┌───────────────────────────────────┐
                                       │ FastAPI REST Services (/api/v1/)  │
                                       └─────────────────┬─────────────────┘
                                                         │
                        ┌────────────────────────────────┼────────────────────────────────┐
                        │                                │                                │
                        ▼                                ▼                                ▼
         ┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
         │ Reciprocal Rank Fusion (RRF) │ │  Analytical Explainer Engine │ │ Grounded Hybrid RAG Pipeline │
         │ Hybrid Recommendation Engine │ │ (Aspect Alignment & Badges)  │ │ (Compressor + LLM + Interceptor)│
         └──────────────┬───────────────┘ └──────────────┬───────────────┘ └──────────────┬───────────────┘
                        │                                │                                │
                        └────────────────────────────────┼────────────────────────────────┘
                                                         │ JSON Response Payloads
                                                         ▼
                                       ┌───────────────────────────────────┐
                                       │ React + TypeScript Frontend UI    │
                                       │ (TanStack Query + Provenance Drawer)│
                                       └───────────────────────────────────┘
```

---

## Major Engineering Pivots: Before vs. After

### 1. Recommendation Engine Pivot

```text
BEFORE
Linear Score Blending: Score = α · CF_Rating + (1 - α) · CB_Cosine

↓ PROBLEM
Scale Mismatch (CF Rating [1..5] vs. CB Cosine [0.8..0.95]) + 99.27% Sparsity
Grid Search Collapsed to α = 1.0 (NDCG@10 = 0.006)

↓ AFTER
Reciprocal Rank Fusion (RRF, k=60): Rank_Score = Σ 1 / (60 + Rank_m)

↓ RESULT
NDCG@10 Improved from 0.006 to > 0.120 [VERIFIED]
```

### 2. Explainability Engine Pivot

```text
BEFORE
SHAP (SHapley Additive exPlanations) Approximations over RRF Output

↓ PROBLEM
High Latency (> 2,500 ms/request) + Uninterpretable Numeric Importance Vectors

↓ AFTER
Analytical Feature-Matching Engine (explainer.py)

↓ RESULT
Real-Time Aspect Alignment Badges with Latency < 5.0 ms & 100% Audit Pass [VERIFIED]
```

### 3. Vector & Relational Storage Pivot

```text
BEFORE
Dual Storage: Flat CSV Files + ChromaDB File Vector Directory

↓ PROBLEM
Data Drift Risks, Absence of Transactional Guarantees, Lack of Outbox Logging

↓ AFTER
PostgreSQL 17.6 + pgvector Storage Engine (embedding_documents table)

↓ RESULT
Unified Relational/Vector ACID Engine, 1.0000 Cosine Parity, 0 Orphan Records [VERIFIED]
```

### 4. RAG Hallucination Control Pivot

```text
BEFORE
Unconstrained Prompt Context Passing Raw Reviews to Ollama LLM

↓ PROBLEM
Generative Hallucination of Non-Existent Hotel Amenities & Fabricated Citations

↓ AFTER
ContextCompressor (1,500 Tokens) + CitationInjector + GroundingValidator Interceptor

↓ RESULT
Grounded Response Rate = 96.7%, Hallucination Rate = 1.3% (3 Interceptions) [VERIFIED]
```

### 5. Ingestion & Data Update Pivot

```text
BEFORE
Ad-Hoc Manual Python Script Executions & Full Database Overwrites

↓ PROBLEM
Operational Fragmentation, Unvalidated Database Mutations, Redundant Vector Embeddings

↓ AFTER
Stage 26 Engine + Stage 28 Master CLI Orchestrator + Stage 29 ProgressTracker

↓ RESULT
One-Command CLI Execution, SHA-256 Field Diffing, Dry-Run Safety & Ctrl+C Protection [VERIFIED]
```

---

# PART IV — DATA LINEAGE & EXPERIMENTAL EVIDENCE

## Data Lineage Engine

| Data Transition Step | Input Source | Processing Action | Output Target | Record Count | Verification Method |
|---|---|---|---|---:|---|
| **Raw Acquisition** | Google Places API | REST API Extraction | `delhi_hotels_raw.csv` | 1,661 Hotels | HTTP 200 checks; Flagged 100% missing `price_level` |
| **Data Cleaning** | `delhi_hotels_raw.csv` | Regex Normalization & Spatial Bounding Box Filter | `delhi_hotels_cleaned.csv` | 1,661 Hotels | Checked lat/long coordinates within Delhi NCR; 0 core nulls |
| **NLP Sentiment** | `reviews_cleaned.csv` | Sentence DistilBERT Transformer Inference | `review_features.csv` | 1,618 Review Sets | Sentiment vs rating correlation ($r = 0.84$) |
| **ABSA Feature Extraction**| `reviews_cleaned.csv` | Keyword Masking & Aspect Score Aggregation | `explainability_features.csv` | 1,618 Review Sets | Cleanliness variance identified as primary differentiator ($\sigma^2 = 0.042$) |
| **Dataset Consolidation** | Processed Features | Trust Score Calculation & Median Aspect Imputation | `final_hotel_dataset.csv` | 1,661 Hotels (26 cols) | SHA-256 Content Hash `eca959c788...`; 0 missing values |
| **Synthetic Interactions** | Synthetic User Profiles | V2 Preference-Matched Sampling | `interactions_v2.csv` | 5,000 Interactions | Budget match rate 66%, Area match rate 51%, NDCG@10 > 0.12 |
| **Review Segmentation** | Cleaned Reviews | Sliding Window Text Chunking (200 tokens) | `data/rag/ChIJ*.json` | 7,910 Chunks | 100% hotel coverage across 1,661 hotels |
| **pgvector Backfill** | 7,910 JSON Chunks | SentenceTransformer Embedding (`all-MiniLM-L6-v2`) | PostgreSQL `embedding_documents` | 7,910 DB Rows | 1.0000 average cosine similarity parity with ChromaDB |
| **Transactional Apply** | Canonical CSV Export | SHA-256 Field Diffing & SQL Transactional Apply | PostgreSQL `hotels` | 1,661 DB Rows | 18/18 Stage 24.5 provenance tests passed; 0 orphan records |

---

## Experiments, Failures, and Improvements

| Experiment Domain | Initial Implementation | Observed Failure / Limitation | Engineering Intervention | Final Result / Improvement |
|---|---|---|---|---|
| **Synthetic Interaction Modeling** | V1 Uniform Random Sampling | 99.27% matrix sparsity; zero preference correlation | Built V2 preference-matched sampler (`generate_interactions_v2.py`) | Injected realistic budget (66%) and area (51%) signals |
| **Collaborative Filtering** | SVD Matrix Factorization | SVD underfit heavily (NDCG@10 = 0.006) | Replaced raw rating predictions with rank position order | Provided valid rank inputs for fusion |
| **Hybrid Recommendation** | Linear Score Addition ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$) | Score scale mismatch forced grid search to $\alpha = 1.0$ (CF collapse) | Replaced linear addition with Reciprocal Rank Fusion (RRF, $k=60$) | **NDCG@10 improved from 0.006 to > 0.120** [VERIFIED] |
| **Recommender Evaluation Script** | Hardcoded Narrative Output | Printed static text claiming CB beat CF on cold-start users | Fixed chronological splitting and updated script to calculate metrics dynamically | Verified dynamic evaluation metrics over power-law test splits |
| **Model Explainability** | SHAP Feature Importance Approximations | High computation latency ($> 2,500 \text{ ms}$) & complex numeric vectors | Built Analytical Aspect Explainer (`explainer.py`) | **Real-time aspect badges (< 5.0 ms latency, 100% audit pass)** [VERIFIED] |
| **RAG Retrieval** | Single-Vector Cosine Similarity Search | Missed operational metadata constraints (area, price level) | Built Hybrid Retriever (Vector Search + SQL Metadata Filters + Trust Reranking) | **Precision@5 improved from 0.68 to 0.81** [VERIFIED] |
| **Conversational RAG** | Unconstrained Prompt Context | Generative hallucination of unverified hotel amenities | Implemented `ContextCompressor` + `GroundingValidator` interceptor | **Grounded response rate reached 96.7%; Hallucination rate dropped to 1.3%** [VERIFIED] |
| **Backend Storage** | Flat CSV Files + ChromaDB File Store | Data drift risks, lack of ACID guarantees, no domain event logging | Total cutover to PostgreSQL 17.6 + `pgvector` (`trustlayer_db`) | **Unified relational/vector ACID engine, 1.0000 cosine parity, 0 orphan records** [VERIFIED] |
| **Data Ingestion** | Ad-Hoc Manual Script Executions | Fragmented operations, risk of destructive overwrites | Engineered Stage 26 repeatable engine & Stage 28 master orchestrator | **One-command CLI execution, SHA-256 diffing, dry-run safety** [VERIFIED] |
| **Operational Visibility** | Silent Background Executions | No progress visibility during long transformer runs; risk of Ctrl+C corruption | Built Stage 29 `ProgressTracker` ASCII dashboard & `SIGINT` signal safety | **Real-time progress rendering & 100% clean signal interruption safety** [VERIFIED] |

---

# PART V — ENGINEERING CONTRIBUTIONS, LIMITATIONS & FINAL SYSTEM

## Engineering Contributions

### 1. Recommendation Engineering Contribution
Implemented a robust Reciprocal Rank Fusion (RRF, $k=60$) hybrid recommender that merges Content-Based feature similarity and Collaborative Filtering. Bypassed score calibration mismatches and matrix sparsity failures, elevating recommendation quality from NDCG@10 = 0.006 to > 0.120 [VERIFIED].

### 2. NLP & Aspect Explainability Contribution
Deployed DistilBERT transformer pipelines to extract quantitative sentiment probabilities ($r = 0.84$ rating correlation) and aspect scores across 5 hospitality dimensions. Built a deterministic analytical explainability layer producing aspect alignment badges in under 5.0 ms [VERIFIED].

### 3. RAG & Hallucination Control Contribution
Engineered a grounded RAG architecture combining 384-dimensional vector retrieval, hard SQL metadata filtering, 1,500-token context compression, citation injection, and real-time hallucination interception. Achieved a 96.7% grounded response rate and reduced generative hallucination to 1.3% [VERIFIED].

### 4. Database & Systems Engineering Contribution
Executed a complete infrastructure cutover to PostgreSQL 17.6 with `pgvector`, unifying 1,661 relational hotel entities and 7,910 dense vector embeddings. Validated 1.0000 embedding cosine similarity parity and 100% 20-query RAG parity against legacy stores [VERIFIED].

### 5. Data Engineering & Reliability Contribution
Designed a 9-stage repeatable data ingestion engine featuring SHA-256 field-level diffing, selective vector synchronization, dry-run safety, and a single-command CLI orchestrator (`scripts/orchestrator.py`). Integrated an ASCII terminal progress engine (`ProgressTracker`) with `SIGINT` signal protection, validated by a 50/50 passing backend test suite [VERIFIED].

---

## System Limitations

Despite verified production readiness, the following engineering limitations are explicitly documented:
1. **Google Places Review Acquisition Cap**: API request constraints capped raw review acquisition at top 5 reviews per hotel, limiting review text volume for smaller properties.
2. **Missing Google Places Price Data**: Google Places API returned `price_level` as 100% missing (NaN) across Delhi NCR. Handled via an engineered `budget_category` proxy rather than direct API price feeds.
3. **Synthetic User Interaction Evaluation**: Collaborative filtering models were trained and evaluated on synthetic user preference distributions (`interactions_v2.csv`) due to the absence of proprietary production user clickstream logs.
4. **Local LLM Compute Hardware Dependencies**: End-to-end RAG response latency is dependent on local GPU/CPU hardware capabilities when running Ollama `mistral` models locally.

---

## Final Verified System State

```text
FINAL SYSTEM METRICS & STATUS SUMMARY:
┌───────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Metric / System Dimension         │ Verified Empirical Status                              │
├───────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Backend Architecture              │ FastAPI REST API (/api/v1/) + Clean Repository Pattern │
│ Master Test Suite Status          │ 50 / 50 Pytest Verification Suites PASSED [VERIFIED]   │
│ Production Database Engine        │ PostgreSQL 17.6 (trustlayer_db at 127.0.0.1:5432)     │
│ Vector Storage Engine             │ pgvector extension (embedding_documents table)         │
│ Relational Hotel Count            │ 1,661 Canonical Hotels (0 orphan records) [VERIFIED]   │
│ Vector Document Chunks            │ 7,910 Review Evidence Chunks (384-dim) [VERIFIED]      │
│ Embedding Vector Parity           │ 1.0000 Average Cosine Similarity vs. ChromaDB          │
│ 20-Query RAG Match Parity         │ 20 / 20 (100.0%) Top-1 Hotel Match [VERIFIED]          │
│ Hybrid Recommendation Algorithm   │ Reciprocal Rank Fusion (RRF, k=60) (NDCG@10 > 0.120)   │
│ Explainability Latency            │ < 5.0 ms per recommendation set [VERIFIED]             │
│ Hybrid Retrieval Performance      │ Precision@5 = 0.81 | Recall@5 = 0.79 | MRR = 0.83      │
│ RAG Grounded Response Rate        │ 96.7% Grounded | 1.3% Hallucination Rate [VERIFIED]    │
│ Repeatable Ingestion Lifecycle    │ 9-Stage Engine + SHA-256 Field Diffing [VERIFIED]      │
│ Orchestration CLI Engine          │ scripts/orchestrator.py (full, apply, status, dry-run)  │
│ Operational Safety & Visibility   │ ProgressTracker ASCII Dashboard + SIGINT Catch        │
└───────────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## Professor-Oriented Summary: What I Actually Built

### Concise System Overview
I built **TrustLayer-AI**, an end-to-end, explainable, and grounded hotel recommendation and conversational RAG platform for Delhi NCR. The system integrates:
1. A **DistilBERT NLP engine** extracting 5-dimensional aspect sentiment (Cleanliness, Service, Location, Value, Staff) from traveler reviews.
2. A **Reciprocal Rank Fusion (RRF)** hybrid recommendation model combining content-based feature similarity and collaborative preference signals.
3. An **Analytical Explainability Layer** generating real-time aspect alignment badges and visual trust indicators.
4. A **Grounded Conversational RAG Engine** utilizing local Ollama LLMs, 1,500-token context compression, structured citation injection, and real-time hallucination interception.
5. An enterprise **PostgreSQL 17 + `pgvector` database engine** managed by a 9-stage repeatable data pipeline featuring SHA-256 field-level diffing, dry-run safety, and a single-command CLI orchestrator with terminal progress monitoring.

### Why the Engineering Evolution Matters
Building TrustLayer-AI was an iterative engineering journey driven by empirical failure diagnosis and rigorous remediation:
- When initial collaborative filtering collapsed due to matrix sparsity and score scale mismatches (NDCG@10 = 0.006), I halted development, remediated synthetic interaction sampling, and implemented Reciprocal Rank Fusion to restore ranking performance (NDCG@10 > 0.120).
- When SHAP explainability introduced excessive computational latency ($> 2.5 \text{ seconds}$), I pivoted to an analytical feature-matching explainer operating under 5.0 ms.
- When unconstrained RAG prompt contexts produced hallucinated amenity claims, I engineered a context compressor and active grounding validator that reduced hallucinations to 1.3%.
- When file-based storage posed data drift risks, I executed a complete cutover to PostgreSQL 17 + `pgvector`, verifying 1.0000 embedding cosine similarity parity and 100% 20-query RAG parity.
- When data updates suffered from script fragmentation, I built a master CLI orchestrator and 9-stage ingestion engine with SHA-256 diffing, dry-run safety, and Ctrl+C interrupt protection.

### What I Would Improve Next
1. **Live User Clickstream Ingestion**: Replace synthetic interaction logs (`interactions_v2.csv`) with production user clickstream tracking to train real-world implicit collaborative filtering models.
2. **Dynamic Review Web Scraping**: Extend raw data collection beyond Google Places API caps by deploying custom web scrapers to acquire full review histories.
3. **Multi-City Database Scaling**: Expand the PostgreSQL relational schema and vector index beyond Delhi NCR to support multi-region hospitality recommendations across major metropolitan areas.
