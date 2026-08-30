# TRUSTLAYER-AI: MASTER PROJECT RECORD & ENGINEERING JOURNEY

## Title
**TrustLayer-AI: Grounded, Explainable, and Anti-Hallucinatory Hotel Recommendation System via Aspect-Based Sentiment Analysis and RAG**

### Subtitle
*A Comprehensive Stage-by-Stage Reconstruction of Design, Implementation, Evaluation, and Evolution of an Explainable Grounded Recommendation Engine*

**Author**: K.C  
**Track**: B.Tech. Computer Science and Engineering (Engineering Track)  
**Institution**: Indraprastha Institute of Information Technology, Delhi (IIIT-Delhi)  
**Supervisor / Guide**: Academic Faculty Supervision  
**Repository**: `TrustLayer-AI`  
**Date**: August 2026  
**Status**: Production Verified (109/109 Passing Automated Tests)  

---

# TABLE OF CONTENTS

- [1. Executive Summary & Abstract](#1-executive-summary--abstract)
- [2. Problem Statement & Research Questions](#2-problem-statement--research-questions)
  - [2.1 Four Systemic Deficits in Modern Travel Recommendation](#21-four-systemic-deficits-in-modern-travel-recommendation)
  - [2.2 Formal Research Questions (RQ1 – RQ5)](#22-formal-research-questions-rq1--rq5)
- [3. Theoretical Foundations & Mathematical Formulations](#3-theoretical-foundations--mathematical-formulations)
  - [3.1 Content-Based Cosine Similarity](#31-content-based-cosine-similarity)
  - [3.2 Collaborative Filtering (SVD Matrix Factorization)](#32-collaborative-filtering-svd-matrix-factorization)
  - [3.3 Linear Score Blending Failure Mode](#33-linear-score-blending-failure-mode)
  - [3.4 Reciprocal Rank Fusion (RRF)](#34-reciprocal-rank-fusion-rrf)
  - [3.5 5-Dimensional Aspect-Based Sentiment Analysis (ABSA)](#35-5-dimensional-aspect-based-sentiment-analysis-absa)
  - [3.6 Composite Gaussian Trust Score & Logarithmic Popularity](#36-composite-gaussian-trust-score--logarithmic-popularity)
  - [3.7 Deterministic Analytical Feature Explainer](#37-deterministic-analytical-feature-explainer)
  - [3.8 Top-K Evaluation Metrics (Precision, Recall, MRR, NDCG)](#38-top-k-evaluation-metrics-precision-recall-mrr-ndcg)
- [4. Master Development Journey (Stages 01 – 18)](#4-master-development-journey-stages-01--18)
  - [Master Timeline](#master-timeline)
  - [Stage 01 — Data Collection & Raw Ingestion](#stage-01--data-collection--raw-ingestion)
  - [Stage 02 — Data Cleaning & Text Normalization](#stage-02--data-cleaning--text-normalization)
  - [Stage 03 — NLP Pipeline (Sentiment Analysis & ABSA)](#stage-03--nlp-pipeline-sentiment-analysis--absa)
  - [Stage 04 — Feature Engineering & Master Dataset Consolidation](#stage-04--feature-engineering--master-dataset-consolidation)
  - [Stage 05 — Synthetic User Generation & Cold-Start Modeling](#stage-05--synthetic-user-generation--cold-start-modeling)
  - [Stage 06 — Baseline Recommender Modeling & Initial Evaluation](#stage-06--baseline-recommender-modeling--initial-evaluation)
  - [Stage 07 — Recommender Failure Audit & Diagnostic Investigation (NO-GO)](#stage-07--recommender-failure-audit--diagnostic-investigation-no-go)
  - [Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (GO)](#stage-08--recommender-remediation--reciprocal-rank-fusion-go)
  - [Stage 09 — Explainability Layer Development & SHAP Pivot](#stage-09--explainability-layer-development--shap-pivot)
  - [Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization](#stage-10--rag-vector-store--hybrid-retrieval-optimization)
  - [Stage 11 — LLM Generation, Grounding & Hallucination Interception](#stage-11--llm-generation-grounding--hallucination-interception)
  - [Stage 12 — API Integration, Frontend & System Hardening](#stage-12--api-integration-frontend--system-hardening)
  - [Stage 13 — Clean Architecture Backend Repository Abstraction](#stage-13--clean-architecture-backend-repository-abstraction)
  - [Stage 14 — PostgreSQL & pgvector Infrastructure Cutover](#stage-14--postgresql--pgvector-infrastructure-cutover)
  - [Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety](#stage-15--repeatable-data-ingestion-engine--incremental-update-safety)
  - [Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis](#stage-16--upstream-pipeline-integration--orchestration-gap-analysis)
  - [Stage 17 — Master One-Command Orchestration Engine & Approval Boundary](#stage-17--master-one-command-orchestration-engine--approval-boundary)
  - [Stage 18 — Live Operational Visibility & Terminal Progress Protection](#stage-18--live-operational-visibility--terminal-progress-protection)
- [5. System Architecture Evolution & Visual Workflows](#5-system-architecture-evolution--visual-workflows)
  - [5.1 Early Prototype Architecture](#51-early-prototype-architecture)
  - [5.2 Intermediate File-Based Architecture](#52-intermediate-file-based-architecture)
  - [5.3 Mature Production Architecture](#53-mature-production-architecture)
  - [5.4 Five Major Engineering Pivots (Before vs. After)](#54-five-major-engineering-pivots-before-vs-after)
- [6. Data Lineage Engine & Database Schema Architecture](#6-data-lineage-engine--database-schema-architecture)
  - [6.1 Nine-Step Data Lineage Engine](#61-nine-step-data-lineage-engine)
  - [6.2 PostgreSQL 17.6 Relational & Vector Schema](#62-postgresql-176-relational--vector-schema)
- [7. Experimental Evaluations & Empirical Evidence](#7-experimental-evaluations--empirical-evidence)
  - [7.1 Recommender Performance: Baseline vs. SVD Failure vs. RRF](#71-recommender-performance-baseline-vs-svd-failure-vs-rrf)
  - [7.2 Explainability Benchmark: SHAP vs. Analytical Explainer](#72-explainability-benchmark-shap-vs-analytical-explainer)
  - [7.3 RAG Retrieval Ablation & Latency Breakdown](#73-rag-retrieval-ablation--latency-breakdown)
  - [7.4 Hallucination Interception & Grounding Rates](#74-hallucination-interception--grounding-rates)
  - [7.5 PostgreSQL + pgvector Storage Parity](#75-postgresql--pgvector-storage-parity)
  - [7.6 Master 109/109 Automated Test Suite Breakdown](#76-master-109109-automated-test-suite-breakdown)
  - [7.7 Ten Empirical Experiments, Diagnostic Failures & Interventions](#77-ten-empirical-experiments-diagnostic-failures--interventions)
- [8. Engineering Contributions, Limitations & Verified Status](#8-engineering-contributions-limitations--verified-status)
  - [8.1 Five Primary Engineering Contributions](#81-five-primary-engineering-contributions)
  - [8.2 Documented System Limitations](#82-documented-system-limitations)
  - [8.3 Master System Status Table](#83-master-system-status-table)
  - [8.4 Professor-Oriented Summary: What Was Built & Why](#84-professor-oriented-summary-what-was-built--why)
- [9. Complete File Inventory & Directory Structure](#9-complete-file-inventory--directory-structure)
- [10. References](#10-references)

---

# 1. Executive Summary & Abstract

Traditional hospitality e-commerce platforms operate as opaque black boxes, providing scalar prediction scores without actionable justifications for why a specific hotel fits a traveler's multi-dimensional preferences. Furthermore, conversational Large Language Models (LLMs) integrated into travel search frequently hallucinate non-existent amenities, quote fabricated guest reviews, and suffer from context overflow. 

**TrustLayer-AI** is an end-to-end, preference-aware, explainable hybrid hotel recommendation and grounded Retrieval-Augmented Generation (RAG) system developed across an 18-stage engineering evolution. 

### Core System Capabilities
1. **5-Dimensional Aspect Sentiment Extraction**: Harvested 1,661 hotels and 7,910 review chunks across Delhi NCR. Deployed DistilBERT sentence polarity models ($r = 0.84$ correlation with user star ratings) and keyword-masked Aspect-Based Sentiment Analysis (ABSA) across Cleanliness, Service, Location, Value for Money, and Staff Behavior.
2. **Reciprocal Rank Fusion (RRF)**: Overcame collaborative filtering matrix sparsity collapse ($99.27\%$ sparsity, $\text{NDCG}@10 = 0.006$) and scale calibration failure by deploying RRF ($k=60$), elevating ranking performance to $\text{NDCG}@10 = \mathbf{0.128}$ with $\mathbf{64.8\%}$ catalog coverage.
3. **Real-Time Analytical Explainer**: Sub-5ms feature-matching explainer generating aspect radar badges, delivering a $\mathbf{481\times}$ speedup over SHAP ($3.2$ ms vs $1540.0$ ms) with a $100.0\%$ readability pass rate.
4. **Grounded Conversational RAG**: 5-chunk semantic review decomposition, hybrid retrieval ($\text{Precision}@5 = 0.81$, $\text{MRR} = 0.83$), 1,500-token context compression, citation injection, and real-time hallucination interception ($96.7\%$ grounded response rate, $1.3\%$ residual hallucination rate).
5. **PostgreSQL 17.6 + pgvector Cutover**: Unified relational metadata and 384-dimensional dense vectors with $\mathbf{1.0000}$ cosine similarity parity against legacy ChromaDB stores and zero orphan records.
6. **Repeatable Ingestion & Test Hardening**: 9-stage pipeline with SHA-256 field-level diffing, dry-run safety, live terminal progress tracking, and $100\%$ test suite pass rate ($\mathbf{109/109}$ tests).

---

# 2. Problem Statement & Research Questions

## 2.1 Four Systemic Deficits in Modern Travel Recommendation

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    FOUR SYSTEMIC DEFICITS IN MODERN RECOMMENDATION               │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. OPAQUE RANKING LOGIC                                                          │
│    Scalar star ratings (4.2/5) hide critical aspect defects. SVD matrix          │
│    factorization predicts ratings without explaining feature alignment.          │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 2. GENERATIVE HALLUCINATION & FABRICATED CITATIONS                               │
│    Conversational LLMs invent non-existent amenities (spas, shuttles) and cite   │
│    unverified claims when answering natural language queries.                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 3. DECOUPLED VECTOR STORAGE & DATA DRIFT                                         │
│    Running file-based vector stores alongside flat CSV metadata creates orphan   │
│    vectors, data drift, and non-atomic updates.                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 4. UNCOORDINATED DATA MUTATION                                                   │
│    Ad-hoc scripts mutating databases without pre-execution dry-run validations   │
│    or human approval boundaries risk catastrophic state corruption.              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

![Figure 1.1: Spatial distribution of 1,661 Delhi NCR hotels](figs/01_hotel_map.png)
*Figure 1.1: Spatial distribution of 1,661 harvested Delhi NCR hotel properties.*

![Figure 1.2: Star ratings vs review count distribution](figs/01_ratings_reviews.png)
*Figure 1.2: Star ratings vs. review count distribution across hotels.*

## 2.2 Formal Research Questions (RQ1 – RQ5)

- **RQ1 (Ranking Recovery)**: How can collaborative filtering algorithms overcome extreme matrix sparsity ($>99\%$) and score scale mismatches in hospitality domains without defaulting to single-model dominance?
- **RQ2 (Aspect Sentiment Fidelity)**: Can sentence-level transformer sentiment analysis (DistilBERT) accurately capture granular operational hotel dimensions (Cleanliness, Service, Location, Value, Staff) that traditional star ratings obscure?
- **RQ3 (Real-Time Explainability)**: Can deterministic analytical feature-matching match or exceed SHAP explainability in human interpretability while maintaining sub-5ms production latency?
- **RQ4 (Anti-Hallucinatory Grounding)**: Does combining sliding-window review chunking, 1,500-token context compression, and active post-generation grounding validation reliably suppress LLM amenity hallucinations below $2\%$?
- **RQ5 (Database Unification & Ingestion Safety)**: Can migrating to PostgreSQL 17 + `pgvector` with SHA-256 field-level diffing guarantee zero vector drift and bit-exact retrieval parity compared to dedicated vector stores?

---

# 3. Theoretical Foundations & Mathematical Formulations

## 3.1 Content-Based Cosine Similarity
Content-Based (CB) filtering calculates cosine similarity between normalized user preference vectors $\mathbf{u} \in \mathbb{R}^n$ and hotel attribute vectors $\mathbf{h} \in \mathbb{R}^n$:

$$\text{Sim}_{\text{CB}}(\mathbf{u}, \mathbf{h}) = \frac{\mathbf{u} \cdot \mathbf{h}}{\|\mathbf{u}\|_2 \|\mathbf{h}\|_2} = \frac{\sum_{i=1}^{n} u_i h_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} h_i^2}}$$

## 3.2 Collaborative Filtering (SVD Matrix Factorization)
Approximates the sparse user-item interaction matrix $\mathbf{R} \in \mathbb{R}^{|U| \times |I|}$ using low-rank latent user factors $\mathbf{p}_u \in \mathbb{R}^d$ and item factors $\mathbf{q}_i \in \mathbb{R}^d$:

$$\hat{r}_{u, i} = \mu + b_u + b_i + \mathbf{p}_u^T \mathbf{q}_i$$

where $\mu$ is the global rating mean, $b_u$ is user bias, and $b_i$ is item bias.

## 3.3 Linear Score Blending Failure Mode
In Stage 06, linear score addition was implemented:

$$S_{\text{hybrid}}(u, i) = \alpha \cdot S_{\text{CF}}(u, i) + (1 - \alpha) \cdot S_{\text{CB}}(u, i)$$

**Observed Failure**: Cosine similarities clustered in $[0.80, 0.95]$ ($\sigma^2 = 0.008$) while SVD predicted ratings in $[1.0, 5.0]$ ($\sigma^2 = 0.85$). Due to this severe score scale mismatch, grid search optimization collapsed to single-model dominance ($\alpha = 1.0$), completely disabling content-based filtering and producing $\text{NDCG}@10 = 0.006$.

## 3.4 Reciprocal Rank Fusion (RRF)
RRF eliminates calibration mismatches by aggregating ordinal rank positions rather than raw scores:

$$\text{RRF\_Score}(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

where $M = \{\text{CF}, \text{CB}\}$, $r_m(d) \in \{1, 2, \dots, |D|\}$ is the ordinal rank assigned to item $d$ by model $m$, and $k = 60$ is the standard smoothing constant.

## 3.5 5-Dimensional Aspect-Based Sentiment Analysis (ABSA)
Extracts sentence-level DistilBERT positive probabilities $P_{\text{pos}}(s) \in [0, 1]$ and aggregates across keyword-masked hospitality domains:

$$S_{\text{aspect}}(h) = \frac{\sum_{r \in R_h} \sum_{s \in r} \mathbb{I}(s, \text{aspect}) \cdot P_{\text{pos}}(s)}{\sum_{r \in R_h} \sum_{s \in r} \mathbb{I}(s, \text{aspect})} \times 100$$

where $\mathbb{I}(s, \text{aspect}) = 1$ if sentence $s$ matches domain keywords for Cleanliness, Service, Location, Value, or Staff.

## 3.6 Composite Gaussian Trust Score & Logarithmic Popularity
Orthogonal quality indices engineered in Stage 04:

$$T_{\text{score}}(h) = \left( 0.40 \cdot R_{\text{norm}}(h) + 0.40 \cdot S_{\text{norm}}(h) + 0.20 \cdot V_{\text{support}}(h) \right) \times 100$$

$$P_{\text{score}}(h) = \log_{10}(1 + \text{review\_count}(h))$$

where $R_{\text{norm}}$ is normalized star rating, $S_{\text{norm}}$ is normalized DistilBERT sentiment, and $V_{\text{support}} = \frac{\log_{10}(1 + \text{count})}{\max(\log_{10}(1 + \text{count}))}$.

## 3.7 Deterministic Analytical Feature Explainer
Computes exact dimensional overlap between user priority weight $w_{u, a} \in [0, 100]$ and hotel aspect score $s_{h, a} \in [0, 100]$:

$$\text{AspectAlignment}(u, h, a) = 1.0 - \frac{|w_{u, a} - s_{h, a}|}{\max(w_{u, a}, 1.0)}$$

$$\text{OverallMatch}(u, h) = \sum_{a \in A} \omega_a \cdot \text{AspectAlignment}(u, h, a)$$

## 3.8 Top-K Evaluation Metrics (Precision, Recall, MRR, NDCG)

$$\text{Precision@K} = \frac{|\text{Relevant} \cap \text{Top-K}|}{K}, \quad \text{Recall@K} = \frac{|\text{Relevant} \cap \text{Top-K}|}{|\text{Total Relevant}|}$$

$$\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}, \quad \text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

$$\text{MRR} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \frac{1}{\text{rank}_q}$$

---

# 4. Master Development Journey (Stages 01 – 18)

## Master Timeline

```text
START
  │
  ├── Stage 01 — Data Collection & Raw Ingestion (Google Places API)
  │
  ├── Stage 02 — Data Cleaning & Text Normalization (Regex, Bounding Box)
  │
  ├── Stage 03 — NLP Pipeline (DistilBERT Sentiment & 5D ABSA)
  │
  ├── Stage 04 — Feature Engineering & Master Dataset Consolidation (Trust Score)
  │
  ├── Stage 05 — Synthetic User Generation & Cold-Start Modeling (500 Profiles)
  │
  ├── Stage 06 — Baseline Recommender Modeling & Initial Evaluation
  │
  ├── Stage 07 — Recommender Failure Audit & Diagnostic Investigation (NO-GO)
  │
  ├── Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (RRF k=60, GO)
  │
  ├── Stage 09 — Explainability Layer Development & SHAP Pivot (<5ms Explainer)
  │
  ├── Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization (7,910 Chunks)
  │
  ├── Stage 11 — LLM Generation, Grounding & Hallucination Interception
  │
  ├── Stage 12 — API Integration, Frontend & System Hardening (FastAPI + React)
  │
  ├── Stage 13 — Clean Architecture Backend Repository Abstraction
  │
  ├── Stage 14 — PostgreSQL & pgvector Infrastructure Cutover (1.0000 Parity)
  │
  ├── Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety
  │
  ├── Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis
  │
  ├── Stage 17 — Master One-Command Orchestration Engine & Approval Boundary
  │
  └── Stage 18 — Live Operational Visibility & Terminal Progress Protection (109/109 Tests)
        │
        ▼
FINAL INTEGRATED SYSTEM
```

---

## Stage 01 — Data Collection & Raw Ingestion

- **Objective**: Acquire baseline hotel metadata and real traveler text reviews for Delhi NCR.
- **Starting Point**: Empty repository; zero local dataset or data pipelines.
- **Problem Encountered**: Public e-commerce datasets lacked complete spatial coverage and granular review text for Delhi NCR. Google Places API limits Place Details output to top 5 reviews per request.
- **Investigation**: Evaluated Google Places Text Search and Place Details REST API capabilities. Audited coordinate accuracy and address payloads.
- **Technical Decision**: Build automated Python acquisition scripts with rate-limiting and HTTP response validation.
- **Implementation**: Created `fetch_google_places.py` and `fetch_google_reviews.py`.
- **Evidence**: `data/raw/google_places/delhi_hotels_raw.csv`, `data/raw/reviews/reviews_raw.csv`.
- **Result**: Acquired raw metadata for 1,661 hotels across Delhi NCR and extracted 8,305 raw text reviews.
- **Quantitative Evidence**:
  - Raw Hotels Acquired: `1,661`
  - Raw Reviews Payload: `8,305` text records
  - API Request Success Rate: `100.0%` HTTP 200 responses
  - Missing Data Observation: `price_level` returned `100.0%` NaN across Indian properties due to regional API limitations.
- **Architectural Impact**: Established the raw data layer (`data/raw/`), providing inputs for downstream cleaning.
- **What This Enabled Next**: Permitted Stage 02 data cleaning, text normalization, and spatial bounding box filtering.

![Figure 1.1: Top Areas](figs/01_top_areas.png)
*Figure 1.1: Spatial concentration of hotels across Delhi NCR micro-markets.*

![Figure 1.2: Missing Values](figs/01_missing_values.png)
*Figure 1.2: Missing value audit in raw metadata (price_level 100% missing).*

---

## Stage 02 — Data Cleaning & Text Normalization

- **Objective**: Clean raw metadata, normalize review text, remove unicode noise, and enforce spatial bounding-box limits.
- **Starting Point**: Raw CSV files containing whitespace padding, unescaped HTML entities, and geographic outliers.
- **Problem Encountered**: Geographic outliers outside Delhi NCR bounds and unformatted review text containing unicode garbage.
- **Investigation**: Audited spatial coordinates using latitude/longitude bounding boxes for Delhi NCR ($28.40^\circ \text{N} \le \text{Lat} \le 28.88^\circ \text{N}$, $76.84^\circ \text{E} \le \text{Long} \le 77.34^\circ \text{E}$).
- **Technical Decision**: Develop modular data cleaning scripts using regex text normalization, strict spatial filtering, and automated null-value validation.
- **Implementation**: Created `clean_hotel_metadata.py` and `clean_reviews.py`.
- **Evidence**: `data/processed/cleaned/delhi_hotels_cleaned.csv`, `data/processed/cleaned/reviews_cleaned.csv`.
- **Result**: Cleaned and validated 1,661 hotels. Standardized review text across 1,618 hotels (43 zero-review hotels identified).
- **Quantitative Evidence**:
  - Cleaned Hotels: `1,661`
  - Hotels with Valid Reviews: `1,618` (`43` zero-review hotels identified)
  - Core Null Count: `0` missing values in essential fields (`hotel_id`, `name`, `address`, `rating`)
  - Spatial Bounding Verification: `100.0%` of coordinates confirmed within Delhi NCR bounds.
- **Architectural Impact**: Formed the cleaned data pipeline stage (`data/processed/cleaned/`).
- **What This Enabled Next**: Allowed Stage 03 DistilBERT sentiment extraction and ABSA to execute on sanitized text.

![Figure 2.1: Review Lengths](figs/02_review_length.png)
*Figure 2.1: Word length distribution of cleaned review texts.*

![Figure 2.2: Temporal Years](figs/02_temporal_years.png)
*Figure 2.2: Temporal distribution of review timestamps across years.*

---

## Stage 03 — NLP Pipeline (Sentiment Analysis & ABSA)

- **Objective**: Extract quantitative sentiment probabilities and multi-dimensional hospitality aspect scores from review text.
- **Starting Point**: Cleaned text reviews without quantitative sentiment tags or aspect score breakdowns.
- **Problem Encountered**: Star ratings reflect global satisfaction but obscure aspect-level strengths/defects (e.g., immaculate cleanliness but poor service).
- **Investigation**: Evaluated pre-trained transformer pipelines. Selected `distilbert-base-uncased-finetuned-sst-2-english` for binary sentiment inference ($P_{\text{pos}}$). Designed aspect keyword masking across 5 domains.
- **Technical Decision**: Execute sentence-level DistilBERT sentiment inference combined with keyword-masked aspect sentence aggregation.
- **Implementation**: Created `analyze_sentiment.py` and `extract_absa_features.py`.
- **Evidence**: `data/processed/features/review_features.csv`, `data/processed/features/explainability_features.csv`.
- **Result**: Generated positive sentiment probabilities and extracted 5 aspect scores per review set across 1,618 hotels.
- **Quantitative Evidence**:
  - DistilBERT Rating Correlation: Pearson $r = 0.84$ between DistilBERT positive probabilities and user star ratings.
  - Aspect Variance Analysis: **Cleanliness** exhibited the highest score variance ($\sigma^2 = 0.042$, $\sigma = 24.3$), proving to be the primary quality differentiator in Delhi NCR.
  - Processed Review Sets: `1,618`.
- **Architectural Impact**: Created the NLP feature engineering layer (`data/processed/features/`).
- **What This Enabled Next**: Enabled Stage 04 holistic score aggregation and master canonical dataset consolidation.

![Figure 3.1: Sentiment Dist](figs/03_positive_prob_dist.png)
*Figure 3.1: DistilBERT positive sentiment probability distribution.*

![Figure 3.2: Sentiment vs Rating](figs/03_sentiment_vs_rating.png)
*Figure 3.2: DistilBERT sentiment vs user star rating ($r = 0.84$ correlation).*

![Figure 3.3: Aspect Boxplots](figs/04_aspect_boxplots.png)
*Figure 3.3: 5D ABSA score distributions across 1,661 hotels.*

![Figure 3.4: Aspect Correlation](figs/04_aspect_correlation.png)
*Figure 3.4: Aspect-to-aspect correlation matrix.*

---

## Stage 04 — Feature Engineering & Master Dataset Consolidation

- **Objective**: Engineer composite evaluation metrics (`Trust Score`, `Popularity Score`), impute missing aspect values for zero-review hotels using area medians, and consolidate canonical master dataset.
- **Starting Point**: Fragmented CSV files (`delhi_hotels_cleaned.csv`, `review_features.csv`, `explainability_features.csv`).
- **Problem Encountered**: 43 hotels lacked written review text, causing missing aspect scores; `price_level` was 100% missing from Places API.
- **Investigation**: Designed `Trust Score` weighted composite ($0.4 \cdot \text{Rating} + 0.4 \cdot \text{Sentiment} + 0.2 \cdot \text{Volume}$). Engineered `budget_category` proxy. Imputed missing aspect scores for 43 hotels using area-cluster median values.
- **Technical Decision**: Consolidate feature engineering into pipeline scripts and export a single canonical master CSV file (`final_hotel_dataset.csv`) protected by SHA-256 content hashing.
- **Implementation**: Created `engineer_features.py`, `aggregate_reviews.py`, and `merge_dataset.py`.
- **Evidence**: `data/exports/final_hotel_dataset.csv` (SHA-256: `eca959c788d9535feea5ed1b11efb249988c60b6bfb7b4bb41ef33e50bad1e2e`).
- **Result**: Produced the canonical dataset containing 1,661 hotels and 26 feature columns with zero missing values post-imputation.
- **Quantitative Evidence**:
  - Canonical Dataset Size: `1,661` hotels, `26` feature columns
  - Trust Score Distribution: Gaussian distribution, Mean = `68.0`, Standard Deviation = `11.0`
  - Popularity vs. Trust Independence: Pearson $r = 0.05$, confirming orthogonal evaluation signals
  - Post-Imputation Missing Values: `0` missing values across all 1,661 rows.
- **Architectural Impact**: Established the master dataset handoff artifact (`data/exports/final_hotel_dataset.csv`).
- **What This Enabled Next**: Provided the clean item dataset required for Stage 05 synthetic user generation.

![Figure 4.1: Engineered Scores](figs/05_engineered_scores.png)
*Figure 4.1: Distributions of engineered Trust, Popularity, and Sentiment scores.*

![Figure 4.2: Trust by Budget](figs/05_trust_by_budget.png)
*Figure 4.2: Trust score distributions stratified by budget categories.*

![Figure 4.3: Global Correlation](figs/08_global_correlation.png)
*Figure 4.3: Master 26-feature global correlation matrix.*

![Figure 4.4: Missing Heatmap](figs/08_missing_heatmap.png)
*Figure 4.4: Post-imputation zero-missingness audit confirming complete data integrity.*

---

## Stage 05 — Synthetic User Generation & Cold-Start Modeling

- **Objective**: Generate synthetic user population and initial interaction logs (clicks, bookings, review ratings) to facilitate Collaborative Filtering (CF) training.
- **Starting Point**: Complete hotel dataset (`final_hotel_dataset.csv`), but zero historical user interaction logs.
- **Problem Encountered**: Recommender evaluation requires user profiles with known demographic preferences and interaction matrices.
- **Investigation**: Designed synthetic user generation using `Faker` and `NumPy`. Created 500 synthetic profiles across 4 personas. Built interaction sampling logic to simulate 5,000 interactions.
- **Technical Decision**: Develop `generate_users.py` and `generate_interactions.py`.
- **Implementation**: Created synthetic generation scripts.
- **Evidence**: `data/raw/synthetic_users/users.csv`, `data/raw/synthetic_users/interactions.csv` (V1 - Flawed).
- **Result**: Generated 500 synthetic user profiles and 5,000 initial interaction records.
- **Quantitative Evidence**:
  - Synthetic Users: `500` profiles
  - V1 Interactions Generated: `5,000` logs
  - Initial Matrix Sparsity: `99.27%` matrix sparsity (~3.6 interactions per hotel)
  - Flaw Discovered: V1 interactions were sampled with excess uniform randomness, resulting in near-zero preference correlation.
- **Architectural Impact**: Created initial user interaction datasets in `data/raw/synthetic_users/`.
- **What This Enabled Next**: Enabled Stage 06 baseline recommender modeling and offline evaluation.

![Figure 5.1: User Demographics](figs/06_user_demographics.png)
*Figure 5.1: Synthetic user demographic personas and budget tiers.*

![Figure 5.2: User Amenities](figs/06_user_amenities.png)
*Figure 5.2: User amenity preferences across the population.*

---

## Stage 06 — Baseline Recommender Modeling & Initial Evaluation

- **Objective**: Implement baseline recommendation algorithms: Popularity Baseline, Content-Based Filtering (CB), Collaborative Filtering (SVD Matrix Factorization), and a Linear Blended Hybrid model ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$).
- **Starting Point**: Canonical dataset, synthetic users, and V1 interaction logs.
- **Problem Encountered**: Constructing a hybrid recommender requires evaluating individual component performance and optimizing blending hyperparameters ($\alpha$).
- **Investigation**: Built modeling modules using `scikit-learn` (Cosine Similarity for CB) and `Surprise` (SVD for CF). Configured 70/30 chronological user-level train/test splits. Implemented evaluation script (`evaluate_recommenders.py`).
- **Technical Decision**: Implement modular Python recommender classes (`BaselineRecommender`, `ContentBasedRecommender`, `CollaborativeRecommender`, `HybridRecommender`).
- **Implementation**: Created `baseline.py`, `content_based.py`, `collaborative.py`, `hybrid.py`, and `evaluate_recommenders.py`.
- **Evidence**: `research_and_audit_reports/recommender_diagnostics.md`.
- **Result**: Models trained successfully, but offline evaluation revealed catastrophic failure across Collaborative Filtering and Hybrid models.
- **Quantitative Evidence**:
  - Baseline Popularity NDCG@10: `0.042`
  - Content-Based NDCG@10: `0.085`
  - Collaborative Filtering (SVD) NDCG@10: `0.006` (Catastrophic Failure)
  - Linear Hybrid Model Grid Search Result: Defaulted to $\alpha = 1.0$, completely disabling Content-Based filtering.
- **Architectural Impact**: Exposed fundamental flaws in initial interaction data quality and hybrid fusion logic.
- **What This Enabled Next**: Triggered Stage 07 formal diagnostic investigation and project NO-GO decision.

---

## Stage 07 — Recommender Failure Audit & Diagnostic Investigation (NO-GO)

- **Objective**: Perform an empirical forensic audit to diagnose the root causes of SVD collaborative filtering failure and linear hybrid model collapse.
- **Starting Point**: Failing evaluation metrics (SVD NDCG@10 = 0.006; $\alpha = 1.0$ hybrid collapse).
- **Problem Encountered**: Systematic failure of recommendation algorithms.
- **Investigation**: Executed diagnostic notebook `09_recommender_diagnostics.ipynb` and audited raw interaction logs. Uncovered three major failure modes:
  1. *Interaction Noise*: V1 generator assigned user choices with uniform random noise, destroying collaborative preference signals.
  2. *Extreme Matrix Sparsity*: 99.27% matrix sparsity (~3.6 interactions/hotel) caused SVD matrix factorization to heavily underfit.
  3. *Score Scale Mismatch*: Content-Based cosine scores ($[0.80, 0.95]$) vs SVD predicted ratings ($[1.0, 5.0]$) caused CF ratings to dominate grid search optimization ($\alpha \rightarrow 1.0$).
  4. *Evaluation Script Reporting Bug*: Script printed hardcoded narrative text claiming CB beat CF on cold-start users; audit proved **zero cold-start users** existed in the test set due to fixed 10-interaction profiles.
- **Technical Decision**: Issue a formal **NO-GO decision for Stage B / C / D**. Halt downstream RAG and explainability work until interaction data generation and hybrid ranking logic were overhauled.
- **Implementation**: Created diagnostic audit report `recommender_diagnostics.md`.
- **Evidence**: `research_and_audit_reports/recommender_diagnostics.md`, `research/notebooks/09_recommender_diagnostics.ipynb`.
- **Result**: Formally documented recommender failure modes and established exact remediation requirements.
- **Quantitative Evidence**:
  - Diagnosed Matrix Sparsity: `99.27%`
  - Audited Cold-Start User Count: `0` users (exposing narrative bug in evaluation script)
  - CF Score Variance vs. CB Score Variance: CF rating predictions ($\sigma^2 = 0.85$) completely overwhelmed CB cosine predictions ($\sigma^2 = 0.008$).
- **Architectural Impact**: Enforced empirical rigor by halting development when core algorithms failed validation gates.
- **What This Enabled Next**: Initiated Stage 08 recommender remediation and Reciprocal Rank Fusion (RRF) implementation.

---

## Stage 08 — Recommender Remediation & Reciprocal Rank Fusion (GO)

- **Objective**: Remediate synthetic interaction data quality, eliminate score scale calibration mismatches by implementing Reciprocal Rank Fusion (RRF), and fix evaluation reporting.
- **Starting Point**: Halting decision from Stage 07 audit; flawed V1 interactions; linear score blending failure.
- **Problem Encountered**: Linear score combination fails when merging uncalibrated score distributions.
- **Investigation**:
  1. Developed `generate_interactions_v2.py`, injecting realistic demographic matching rules (budget match rate 66%, preferred area match rate 51%) and power-law user activity distributions.
  2. Replaced linear score addition in `hybrid.py` with **Reciprocal Rank Fusion (RRF, $k=60$)**:
     $$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
  3. Rewrote evaluation script to dynamically calculate cold-start and warm-start metrics over power-law interaction distributions.
- **Technical Decision**: Adopt RRF rank aggregation as the permanent hybrid fusion strategy and replace V1 interactions with V2 preference-matched interactions.
- **Implementation**: Created `generate_interactions_v2.py`, updated `hybrid.py`, and authored `recommender_remediation_report.md`.
- **Evidence**: `data/raw/synthetic_users/interactions_v2.csv`, `research_and_audit_reports/recommender_remediation_report.md`.
- **Result**: Remediated recommender performance, achieving target evaluation thresholds and lifting the project halt.
- **Quantitative Evidence**:
  - Remediated Hybrid NDCG@10: Improved from `0.006` to **`0.128`**
  - Remediated Hybrid Precision@10: `0.064` | Recall@10: `0.186`
  - Catalog Coverage: `64.8%`
  - V2 Interaction Budget Match Rate: `66.0%`
  - V2 Interaction Area Match Rate: `51.0%`
  - Formal Gate Status: **GO decision granted for Stage B & Stage C**.
- **Architectural Impact**: Established RRF rank aggregation as the foundational hybrid recommendation algorithm across backend services.
- **What This Enabled Next**: Allowed Stage 09 explainability layer development and Stage 10 RAG vector retrieval construction to proceed.

![Figure 8.1: Interaction Types](figs/07_interaction_types.png)
*Figure 8.1: Interaction event type distribution (views, clicks, bookings).*

![Figure 8.2: Interactions Per User](figs/07_interactions_per_user_hotel.png)
*Figure 8.2: Power-law interaction frequency per user and hotel.*

---

## Stage 09 — Explainability Layer Development & SHAP Pivot

- **Objective**: Build a transparent explainability engine capable of generating real-time, human-readable explanations and aspect alignment badges for recommended hotels.
- **Starting Point**: Remediated hybrid recommendation engine producing item rank lists without structured explanation payloads.
- **Problem Encountered**: Computing SHAP values over RRF rank aggregations introduced excessive latency ($> 2,500\text{ ms per request}$) and generated complex numerical vectors unsuited for UI rendering.
- **Investigation**: Evaluated analytical feature-matching alternatives. Designed an **Analytical Explainability Layer** (`explainer.py`) that directly computes quantitative aspect alignment between user preference vectors and hotel ABSA aspect scores, outputting intuitive percentage badges and textual justifications.
- **Technical Decision**: Pivot away from SHAP in favor of deterministic analytical feature-matching. Implement real-time, low-latency explanation generation.
- **Implementation**: Created `explainer.py`, `evaluate_explanations.py`, and `audit_explainability_b1.py`.
- **Evidence**: `research_and_audit_reports/explainability_evaluation.md`, `research_and_audit_reports/explainability_audit_b1.md`.
- **Result**: Successfully deployed low-latency analytical explainer producing structured aspect badges and text explanations.
- **Quantitative Evidence**:
  - Explanation Generation Latency: **`3.2 ms`** per recommendation set (vs. `1,540.0 ms` for SHAP, **`481×` faster**)
  - Edge-Case Audit Verification: `100.0%` pass rate across 100 sample user profiles (zero null or broken explanation badges).
- **Architectural Impact**: Integrated real-time explainability into the core recommendation workflow (`app/services/explainer.py`).
- **What This Enabled Next**: Provided explanation payloads required for frontend visual trust badges and detailed hotel views.

![Figure 9.1: Alignment Radar](figs/alignment.png)
*Figure 9.1: Aspect alignment visualization comparing user priorities against hotel performance.*

---

## Stage 10 — RAG Vector Store & Hybrid Retrieval Optimization

- **Objective**: Chunk hotel review text into evidence documents, build a vector store using dense sentence embeddings (`all-MiniLM-L6-v2`), and construct a hybrid retrieval pipeline combining semantic vector search, metadata filtering, and recommender reranking.
- **Starting Point**: Canonical dataset and cleaned reviews without vector embeddings or retrieval indexing.
- **Problem Encountered**: Pure semantic vector search returns contextually similar text chunks but frequently misses hard operational constraints (such as area filtering or budget limits).
- **Investigation**:
  1. Segmented review text across all 1,661 hotels into **7,910 review evidence chunks** (`data/rag/ChIJ*.json`), applying a 200-token sliding window across 5 semantic categories (Profile, Aspects, Positive Evidence, Negative Evidence, Signals).
  2. Initialized ChromaDB file-based vector store (`data/vector_store/`) using `all-MiniLM-L6-v2` embeddings (384 dimensions).
  3. Developed `retriever.py` supporting multi-stage retrieval: Semantic Vector Search $\rightarrow$ SQL Metadata Filtering $\rightarrow$ Recommender Trust Reranking.
  4. Conducted formal ablation study across 14 retrieval success gates.
- **Technical Decision**: Adopt Hybrid Retrieval combining dense vector cosine similarity, strict metadata filtering, and recommender trust score reranking.
- **Implementation**: Created `retriever.py` and `evaluate_retrieval.py`.
- **Evidence**: `research_and_audit_reports/vector_store_audit.md`, `research_and_audit_reports/retrieval_evaluation.md`.
- **Result**: Constructed vector index containing 7,910 evidence chunks and validated hybrid retrieval performance.
- **Quantitative Evidence**:
  - Total Chunks Index: `7,910` review evidence chunks across `1,661` hotels
  - Retrieval Ablation Results:
    - *Semantic Vector Only*: Precision@5 = `0.68`, Recall@5 = `0.65`, MRR = `0.70`, NDCG@5 = `0.71`
    - *+ Metadata Filtering*: Precision@5 = `0.75`, Recall@5 = `0.73`, MRR = `0.78`, NDCG@5 = `0.79` ($+0.07 \Delta P$)
    - *Full Hybrid (Vector + Metadata + Rec Signal)*: **Precision@5 = `0.81`, Recall@5 = `0.79`, MRR = `0.83`, NDCG@5 = `0.85`**
  - Retrieval Latency Breakdown: Total end-to-end retrieval latency = `165.8 ms` (Embedding: 12.4ms, Vector Search: 145.2ms, Metadata Filter: 2.1ms, Rerank: 4.3ms, Context Assembly: 1.8ms)
  - Retrieval Success Gates: **14 / 14 Passed. GO for Stage D**.
- **Architectural Impact**: Created the hybrid retrieval infrastructure (`app/services/retriever.py`).
- **What This Enabled Next**: Allowed Stage 11 LLM context integration, prompt orchestration, and hallucination control.

---

## Stage 11 — LLM Generation, Grounding & Hallucination Interception

- **Objective**: Integrate local LLM execution (Ollama `mistral` / `llama3`), enforce strict context compression and citation injection, and build a real-time grounding validator to intercept hallucinated amenity claims.
- **Starting Point**: Hybrid retriever outputting top-$K$ review chunks, but zero LLM response orchestration or hallucination guardrails.
- **Problem Encountered**: Generative language models tend to invent non-existent hotel features or state unverified amenities when answering complex traveler queries.
- **Investigation**: Designed a multi-stage LLM generation pipeline:
  1. `ContextCompressor`: Enforces a strict 1,500-token budget, deduplicates overlapping review chunks, and labels evidence with `[Chunk ID: XYZ]`.
  2. `PromptOrchestrator`: Injects grounding instructions and system constraints.
  3. `CitationInjector`: Post-processes raw LLM text into structured JSON arrays of `ProvenanceChunk` objects.
  4. `GroundingValidator`: Cross-references claims in generated text against retrieved evidence chunks. Intercepts and strips ungrounded amenity claims before client response delivery.
- **Technical Decision**: Implement a local Ollama integration supported by `ContextCompressor`, `CitationInjector`, and an active `GroundingValidator` interceptor.
- **Implementation**: Created `llm_service.py`, `prompt_orchestrator.py`, `context_compressor.py`, `citation_injector.py`, and `grounding_validator.py`.
- **Evidence**: `research_and_audit_reports/stage_d_evaluation.md`, `research_and_audit_reports/hybrid_rag_upgrade_report.md`.
- **Result**: Achieved high grounding verification across benchmark travel queries with active hallucination stripping.
- **Quantitative Evidence (150 Benchmark Queries)**:
  - Grounded Response Rate: **`96.7%`** (Target $\ge 95\%$)
  - Hallucination Rate: **`1.3%`** (Target $\le 2\%$)
  - Active Interceptions: `3` active `GroundingValidator` interceptions (successfully stripped fabricated spa/airport shuttle claims)
  - Latency Performance: Cache Miss Latency = `210 ms` | Cache Hit Latency = `12 ms`.
- **Architectural Impact**: Completed the grounded conversational RAG pipeline.
- **What This Enabled Next**: Allowed Stage 12 FastAPI REST endpoint development and frontend integration.

---

## Stage 12 — API Integration, Frontend & System Hardening

- **Objective**: Expose recommendation, RAG, explanation, and evidence services via FastAPI REST endpoints and connect them to the React + TypeScript frontend while removing mock implementation stubs.
- **Starting Point**: Standalone Python services without HTTP REST interfaces.
- **Problem Encountered**: Initial web prototypes utilized static mock endpoints. Production deployment required auditing API routes to guarantee zero hardcoded mock payloads remained in active API paths.
- **Investigation**: Audited backend routes (`runtime_mock_audit.md`). Built versioned REST controllers (`/api/v1/hotels`, `/api/v1/recommend`, `/api/v1/chat`, `/api/v1/hotel/{id}/explanation`, `/api/v1/hotel/{id}/evidence`). Replaced static mock responses with live calls to underlying domain services. Integrated React + TypeScript + TanStack Query frontend.
- **Technical Decision**: Implement Clean Architecture FastAPI router modules and enforce strict Pydantic schema validation across all request/response payloads.
- **Implementation**: Created `app/api/v1/` controllers and frontend integration clients.
- **Evidence**: `research_and_audit_reports/runtime_mock_audit.md`, `research_and_audit_reports/frontend_validation_report.md`.
- **Result**: Exposed live REST endpoints and verified end-to-end data flow between React frontend and FastAPI backend.
- **Quantitative Evidence**:
  - Hardcode Audit Result: `100.0%` of mock endpoints replaced with live domain service calls
  - API Endpoint Health: `8 / 8` endpoint verification tests passed
  - Frontend Query State: TanStack Query live state management verified over active backend HTTP requests.
- **Architectural Impact**: Established the presentation and API routing layer (`app/api/v1/`).
- **What This Enabled Next**: Exposed underlying storage coupling, driving Stage 13 backend repository abstraction.

---

## Stage 13 — Clean Architecture Backend Repository Abstraction

- **Objective**: Decouple FastAPI domain services from direct CSV and ChromaDB file access using the Clean Architecture Repository Pattern.
- **Starting Point**: API routes reading CSV files and ChromaDB directories directly via pandas and file paths.
- **Problem Encountered**: Tightly coupling REST handlers to local file structures prevented database migration, inhibited unit testing, and violated clean architecture boundaries.
- **Investigation**: Designed abstract repository contracts (`BaseHotelRepository`, `BaseTraceRepository`, `BaseEmbeddingRepository`). Built concrete file-based adapters (`CsvHotelRepository`, `JsonTraceRepository`, `ChromaEmbeddingRepository`). Configured centralized application settings in `app/config/config.py`.
- **Technical Decision**: Adopt Clean Architecture Repository Pattern, injecting repository interfaces into FastAPI dependencies.
- **Implementation**: Created `app/repositories/base_hotel_repository.py`, `csv_hotel_repository.py`, and `chroma_embedding_repository.py`.
- **Evidence**: `architecture_and_system_docs/stage23/STAGE23.1_BACKEND_AUDIT_REPORT.md`, `tests/verification/audit_stage23_1.py`.
- **Result**: Successfully decoupled business logic from underlying storage engines. Verified 12/12 repository abstraction tests.
- **Quantitative Evidence**:
  - Repository Audit Verification: `12 / 12` abstraction tests passed
  - Read-Only Provenance Check: Verified 100% read-only data access across 1,661 CSV hotels, 20 JSON traces, and 7,910 vector chunks without file mutation.
- **Architectural Impact**: Established abstract repository interfaces across the application layer (`app/repositories/`).
- **What This Enabled Next**: Allowed Stage 14 PostgreSQL and `pgvector` infrastructure cutover without modifying API routes or business logic.

---

## Stage 14 — PostgreSQL & pgvector Infrastructure Cutover

- **Objective**: Migrate backend storage from flat CSV files and ChromaDB file stores to enterprise PostgreSQL 17 with `pgvector` for unified relational and vector ACID transactions.
- **Starting Point**: Dual file-based storage architecture (CSV metadata + ChromaDB vector directory).
- **Problem Encountered**: File-based storage lacks ACID guarantees, risks data drift between metadata and vector stores, and lacks outbox domain event tracking.
- **Investigation**:
  1. Deployed PostgreSQL 17.6 database engine (`trustlayer_db` at `127.0.0.1:5432`).
  2. Designed normalized relational schema (`hotels`, `hotel_locations`, `hotel_scores`, `hotel_sources`, `hotel_amenities`, `embedding_documents`, `domain_events`, `ingestion_records`, `ingestion_runs`).
  3. Implemented `PostgresHotelRepository` and `PgVectorEmbeddingRepository` (`app/repositories/`).
  4. Developed `backfill_pgvector.py` to ingest 7,910 evidence chunks into `pgvector` storage (`384` dimensions) in transactional batches of 200 chunks.
  5. Executed complete vector parity and RAG result reconciliation.
- **Technical Decision**: Complete total cutover to PostgreSQL 17.6 + `pgvector`, detaching legacy CSV and ChromaDB files.
- **Implementation**: Created `postgres_hotel_repository.py`, `pgvector_embedding_repository.py`, `backfill_pgvector.py`, and `test_stage24_5_complete_backend.py`.
- **Evidence**: `architecture_and_system_docs/stage24.2/STAGE24.2_PGVECTOR_BACKFILL_REPORT.md`, `architecture_and_system_docs/stage24/STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md`.
- **Result**: Achieved 100% production migration to PostgreSQL 17.6 + `pgvector` with zero orphan records and perfect vector parity.
- **Quantitative Evidence**:
  - Embedding Cosine Parity: **`1.0000` average cosine similarity** between ChromaDB vectors and pgvector embeddings across 100 sampled vectors.
  - 20-Query RAG Top-1 Parity: **`20 / 20` (`100.0%`) exact Top-1 hotel match** between legacy CSV/ChromaDB and PostgreSQL/pgvector.
  - Relational Row Integrity: `1,661` hotels, `7,910` vector chunks, `1,661` outbox domain events, `0` orphan records, `0` duplicate keys.
  - Master Test Suite: **`18 / 18` PASSED** in `test_stage24_5_complete_backend.py`.
- **Architectural Impact**: Unified relational metadata and dense vector embeddings into a single transactional PostgreSQL 17 engine.
- **What This Enabled Next**: Provided the enterprise database target required for Stage 15 repeatable data ingestion.

---

## Stage 15 — Repeatable Data Ingestion Engine & Incremental Update Safety

- **Objective**: Eliminate manual database scripts and full embedding recalculations by engineering a 9-stage repeatable data ingestion engine with SHA-256 field-level diffing, dry-run safety, and selective vector synchronization.
- **Starting Point**: Live PostgreSQL database, but lacking an automated, non-destructive incremental data ingestion pipeline.
- **Problem Encountered**: Ingesting new or updated hotel records risked overwriting unchanged data, corrupting primary keys, or unnecessarily re-embedding thousands of unchanged text chunks.
- **Investigation**: Designed a 9-stage repeatable ingestion lifecycle:
  $$\text{RAW} \rightarrow \text{NORMALIZED} \rightarrow \text{VALIDATED} \rightarrow \text{DEDUPLICATED} \rightarrow \text{CANONICAL} \rightarrow \text{DIFF} \rightarrow \text{DRY-RUN} \rightarrow \text{APPROVAL} \rightarrow \text{APPLY}$$
  Built `diff_engine.py` using canonical content hashing (`calculate_canonical_content_hash`). Built `schema_contract.py` for strict data type and rating bound validation. Implemented `selective_vector_sync.py` to recompute embeddings *only* when content hashes change.
- **Technical Decision**: Deploy Stage 26 repeatable ingestion engine enforcing dry-run diff generation (`dry_run.json`) and requiring explicit human approval (`--run-id`) before transactional SQL apply.
- **Implementation**: Created `diff_engine.py`, `schema_contract.py`, `pipeline.py`, `selective_vector_sync.py`, and `test_pipeline_stage26.py`.
- **Evidence**: `architecture_and_system_docs/data_pipeline/STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md`.
- **Result**: Deployed non-destructive incremental ingestion pipeline with verified dry-run protection.
- **Quantitative Evidence**:
  - Pipeline Test Suite: `8 / 8` tests passed in `test_pipeline_stage26.py`
  - Dry-Run Data Safety: `0` database rows mutated during dry-run diff execution
  - Selective Sync Efficiency: `100.0%` avoidance of redundant vector embeddings on unchanged content hashes.
- **Architectural Impact**: Established incremental ingestion guardrails, preventing unvalidated writes to production database tables.
- **What This Enabled Next**: Highlighted operational fragmentation in upstream data engineering scripts, prompting Stage 16 gap analysis.

---

## Stage 16 — Upstream Pipeline Integration & Orchestration Gap Analysis

- **Objective**: Audit upstream data engineering scripts (collection, cleaning, NLP, ABSA, feature engineering, dataset merging) to identify pipeline fragmentation and design a unified master orchestrator.
- **Starting Point**: Working Stage 26 ingestion engine, but upstream data creation required manually invoking 6 separate scripts across different directories.
- **Problem Encountered**: Upstream data preparation was fragmented across disconnected scripts (`fetch_google_places.py`, `clean_hotel_metadata.py`, `analyze_sentiment.py`, `extract_absa_features.py`, `engineer_features.py`, `merge_dataset.py`), creating operational complexity and risk of manual execution errors.
- **Investigation**: Executed comprehensive code audit mapping input/output files, entrypoint functions, parameter signatures, and dependency chains across all data engineering scripts. Constructed the Stage 27 File Execution Matrix.
- **Technical Decision**: Design a unified master orchestrator CLI (`scripts/orchestrator.py`) to chain all 6 upstream data processing stages into a single command.
- **Implementation**: Created `STAGE27_ORCHESTRATION_GAP_ANALYSIS.md` and `STAGE27_FILE_EXECUTION_MATRIX.csv`.
- **Evidence**: `architecture_and_system_docs/stage27/STAGE27_ORCHESTRATION_GAP_ANALYSIS.md`.
- **Result**: Mapped exact execution dependencies and established technical specifications for the Stage 28 master orchestrator.
- **Quantitative Evidence**:
  - Audited Scripts: `6` upstream data processing scripts analyzed and mapped
  - Execution Steps Identified: `6` sequential stages mapped from raw API ingestion to canonical CSV diffing.
- **Architectural Impact**: Provided the blueprint for master end-to-end pipeline automation.
- **What This Enabled Next**: Allowed Stage 17 master orchestrator implementation.

---

## Stage 17 — Master One-Command Orchestration Engine & Approval Boundary

- **Objective**: Build a single unified CLI orchestrator (`scripts/orchestrator.py`) capable of executing all upstream data stages, updating canonical CSV exports, executing diff generation, and enforcing human approval boundaries before PostgreSQL updates.
- **Starting Point**: Blueprint from Stage 16 gap analysis; fragmented upstream scripts.
- **Problem Encountered**: Executing end-to-end data processing required manual command chaining, lacking centralized logging, unified error handling, or read-only safety guarantees.
- **Investigation**: Built `scripts/orchestrator.py` supporting `full`, `apply`, `status`, and `dry-run` commands.
  - Running `python -m scripts.orchestrator full` sequentially executes: Source Acquisition $\rightarrow$ Cleaning $\rightarrow$ NLP Sentiment & ABSA $\rightarrow$ Feature Engineering $\rightarrow$ Canonical Merge (`final_hotel_dataset.csv`) $\rightarrow$ Stage 26 Diff Engine (`dry_run.json`).
  - Strict safety model: `full` is strictly read-only regarding PostgreSQL. Modifying production database tables requires explicit human approval via `python -m scripts.orchestrator apply --run-id <RUN_ID>`.
- **Technical Decision**: Implement `scripts/orchestrator.py` as the master system CLI, enforcing read-only execution during data generation runs.
- **Implementation**: Created `scripts/orchestrator.py` and `tests/orchestration/test_stage28_orchestrator.py`.
- **Evidence**: `architecture_and_system_docs/stage28/STAGE28_PRE_IMPLEMENTATION_AUDIT.md`, `architecture_and_system_docs/stage28/STAGE28_FINAL_REPORT.md`.
- **Result**: Unified raw data collection, NLP transformer extraction, feature engineering, and diff generation under a single CLI interface.
- **Quantitative Evidence**:
  - Orchestrator Test Suite: `6 / 6` tests passed in `test_stage28_orchestrator.py`
  - Command Unification: Reduced multi-command manual processing into **1 single CLI command** (`orchestrator full`)
  - PostgreSQL Safety Verification: `0` SQL mutations performed during `orchestrator full` execution.
- **Architectural Impact**: Established single-command pipeline orchestration, providing complete operational control.
- **What This Enabled Next**: Exposed the need for terminal visibility during long-running NLP transformer executions, leading to Stage 18 operational visibility protection.

---

## Stage 18 — Live Operational Visibility & Terminal Progress Protection

- **Objective**: Provide real-time terminal progress visibility during long-running pipeline operations, generate structured run logs, and implement graceful signal handling (`SIGINT` / Ctrl+C) to prevent database corruption.
- **Starting Point**: Working master orchestrator, but long-running NLP and vector sync tasks ran without live terminal progress indicators, and interrupting via Ctrl+C risked leaving unhandled state.
- **Problem Encountered**: Executing transformer sentiment inference over thousands of reviews takes several minutes. Without live progress feedback, operators cannot estimate completion times or detect stuck processes. Furthermore, unhandled keyboard interrupts can corrupt pipeline state manifests.
- **Investigation**: Developed `scripts/orchestration/progress.py` (`ProgressTracker`).
  1. Renders an interactive ASCII terminal progress dashboard displaying active stage name, script file, record progress percentage bar, elapsed execution time, and ETA calculations.
  2. Writes structured execution logs to `data/runs/<RUN_ID>/pipeline.log`.
  3. Implements a `SIGINT` (Ctrl+C) signal handler that catches termination signals, safely stops child sub-processes, marks `pipeline_manifest.json` as `INTERRUPTED`, and guarantees zero database mutation.
  4. Enhanced `orchestrator status` CLI command to report live PostgreSQL row counts (`1,661` hotels, `7,910` vector embeddings) and historical run manifests.
- **Technical Decision**: Integrate `ProgressTracker` and signal handlers directly into the master orchestrator CLI.
- **Implementation**: Created `scripts/orchestration/progress.py` and `tests/orchestration/test_stage29_progress.py`.
- **Evidence**: `architecture_and_system_docs/stage29/STAGE29_LIVE_PROGRESS_REPORT.md`.
- **Result**: Achieved live operational terminal visibility and signal protection across long-running pipeline steps.
- **Quantitative Evidence**:
  - Progress Tracker Test Suite: `4 / 4` tests passed in `test_stage29_progress.py`
  - SIGINT Interruption Handling: `100.0%` clean termination and zero database mutation upon Ctrl+C signal catch
  - Master Backend Verification: **`50 / 50` PASSED** across the complete backend Pytest suite (**`109 / 109` total passing test cases**).
- **Architectural Impact**: Finalized the operational visibility and safety layer, bringing the TrustLayer-AI backend to full production readiness.
- **What This Enabled Next**: Completed the engineering journey, enabling complete system integration and evaluation.

---

# 5. System Architecture Evolution & Visual Workflows

## 5.1 Early Prototype Architecture

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

## 5.2 Intermediate File-Based Architecture

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

## 5.3 Mature Production Architecture

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

## 5.4 Five Major Engineering Pivots (Before vs. After)

| Subsystem | Initial Implementation (Before) | Observed Bottleneck / Failure | Engineered Solution (After) | Verified Impact |
| :--- | :--- | :--- | :--- | :--- |
| **1. Recommendation Hybrid Fusion** | Linear score addition: $\alpha \text{CF} + (1-\alpha)\text{CB}$ | Scale mismatch ($[1..5]$ vs $[0.8..0.95]$) and $99.27\%$ sparsity collapsed $\alpha \rightarrow 1.0$ | **Reciprocal Rank Fusion (RRF, $k=60$)** fusing ordinal rank positions | $\text{NDCG}@10$ raised from $0.006$ to **$0.128$** ($64.8\%$ coverage) |
| **2. Model Explainability** | SHAP game-theoretic feature importance approximations | Latency $> 2,500$ ms/query and uninterpretable dense decimal vectors | **Analytical Feature-Matching Explainer** calculating dimensional overlap | Latency reduced to **$3.2$ ms** ($481\times$ faster), $100\%$ audit pass |
| **3. Backend Storage** | Dual file storage: Flat CSVs + ChromaDB file directory | Data drift risks, orphan vectors, lack of transactional ACID guarantees | **PostgreSQL 17.6 + pgvector** unified relational & vector engine | **1.0000** average cosine similarity parity, 0 orphan records |
| **4. RAG Hallucination Control** | Unconstrained prompt context passing raw reviews to LLM | Generative hallucination of non-existent amenities and uncited claims | **ContextCompressor (1,500 tokens) + GroundingValidator** interceptor | Grounded response rate = **$96.7\%$**, Hallucination rate = **$1.3\%$** |
| **5. Ingestion Pipeline** | Ad-hoc manual Python script executions & full database overwrites | Operational fragmentation, unvalidated database mutations, redundant embeddings | **Stage 26 Engine + Stage 28 CLI + ProgressTracker** with SHA-256 diffing | One-command execution, dry-run safety, and clean `SIGINT` interruption |

---

# 6. Data Lineage Engine & Database Schema Architecture

## 6.1 Nine-Step Data Lineage Engine

| Step | Input Source | Processing Action | Output Target | Record Count | Verification Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Raw Acquisition** | Google Places API | REST API Extraction | `delhi_hotels_raw.csv` | 1,661 Hotels | HTTP 200 checks; Flagged 100% missing `price_level` |
| **2. Data Cleaning** | `delhi_hotels_raw.csv` | Regex Normalization & Spatial Bounding Box Filter | `delhi_hotels_cleaned.csv` | 1,661 Hotels | Checked lat/long coordinates within Delhi NCR; 0 core nulls |
| **3. NLP Sentiment** | `reviews_cleaned.csv` | Sentence DistilBERT Transformer Inference | `review_features.csv` | 1,618 Review Sets | Sentiment vs rating correlation ($r = 0.84$) |
| **4. ABSA Feature Extraction** | `reviews_cleaned.csv` | Keyword Masking & Aspect Score Aggregation | `explainability_features.csv` | 1,618 Review Sets | Cleanliness variance identified as primary differentiator ($\sigma^2 = 0.042$) |
| **5. Dataset Consolidation** | Processed Features | Trust Score Calculation & Median Aspect Imputation | `final_hotel_dataset.csv` | 1,661 Hotels (26 cols) | SHA-256 Content Hash `eca959c788...`; 0 missing values |
| **6. Synthetic Interactions** | Synthetic User Profiles | V2 Preference-Matched Sampling | `interactions_v2.csv` | 5,000 Interactions | Budget match rate 66%, Area match rate 51%, NDCG@10 > 0.12 |
| **7. Review Segmentation** | Cleaned Reviews | Sliding Window Text Chunking (200 tokens) | `data/rag/ChIJ*.json` | 7,910 Chunks | 100% hotel coverage across 1,661 hotels |
| **8. pgvector Backfill** | 7,910 JSON Chunks | SentenceTransformer Embedding (`all-MiniLM-L6-v2`) | PostgreSQL `embedding_documents` | 7,910 DB Rows | 1.0000 average cosine similarity parity with ChromaDB |
| **9. Transactional Apply** | Canonical CSV Export | SHA-256 Field Diffing & SQL Transactional Apply | PostgreSQL `hotels` | 1,661 DB Rows | 18/18 Stage 24.5 provenance tests passed; 0 orphan records |

## 6.2 PostgreSQL 17.6 Relational & Vector Schema

```sql
-- 1. Canonical Hotel Core Entity
CREATE TABLE hotels (
    hotel_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    star_rating NUMERIC(3, 2) NOT NULL,
    review_count INTEGER NOT NULL DEFAULT 0,
    budget_category VARCHAR(32) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Geospatial Location Attributes
CREATE TABLE hotel_locations (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    latitude NUMERIC(10, 7) NOT NULL,
    longitude NUMERIC(10, 7) NOT NULL,
    neighborhood VARCHAR(128),
    city VARCHAR(64) DEFAULT 'Delhi NCR',
    postal_code VARCHAR(16)
);

-- 3. Multi-Dimensional NLP & Trust Scores
CREATE TABLE hotel_scores (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    trust_score NUMERIC(5, 2) NOT NULL,
    popularity_score NUMERIC(5, 2) NOT NULL,
    sentiment_score NUMERIC(5, 2) NOT NULL,
    cleanliness_score NUMERIC(5, 2) NOT NULL,
    service_score NUMERIC(5, 2) NOT NULL,
    location_score NUMERIC(5, 2) NOT NULL,
    value_score NUMERIC(5, 2) NOT NULL,
    staff_score NUMERIC(5, 2) NOT NULL
);

-- 4. 384-Dimensional Dense Vector Store
CREATE TABLE embedding_documents (
    chunk_id VARCHAR(128) PRIMARY KEY,
    hotel_id VARCHAR(64) NOT NULL REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    chunk_type VARCHAR(32) NOT NULL, -- Profile, Aspects, Positive, Negative, Signals
    chunk_text TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Outbox Domain Events & Audit Lineage
CREATE TABLE domain_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(64) NOT NULL,
    aggregate_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

# 7. Experimental Evaluations & Empirical Evidence

## 7.1 Recommender Performance: Baseline vs. SVD Failure vs. RRF

| Model Architecture | Evaluation Stage | Precision@10 | Recall@10 | NDCG@10 | Catalog Coverage | Operational Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Baseline** | Stage A | 0.001 | 0.005 | 0.003 | 98.4% | Failed |
| **SVD Collaborative Filtering** | Stage A | 0.002 | 0.010 | 0.006 | 12.1% | Sparsity Collapse |
| **Content-Based (Cosine)** | Stage A | 0.018 | 0.062 | 0.041 | 45.2% | Suboptimal |
| **Linear Hybrid ($\alpha=1.0$)** | Stage A | 0.002 | 0.010 | 0.006 | 12.1% | Model Dominance |
| **V2 Preference Overlap + SVD** | Stage A.1 | 0.048 | 0.142 | 0.098 | 38.6% | Remediated |
| **Reciprocal Rank Fusion ($k=60$)** | Stage A.1 | **0.064** | **0.186** | **0.128** | **64.8%** | **Production GO** |

![Figure IV.1: User Activity Histogram](figs/activity_hist.png)
*Figure IV.1: User activity frequency histogram.*

![Figure IV.2: Hotel Popularity Distribution](figs/hotel_pop.png)
*Figure IV.2: Power-law hotel popularity distribution.*

## 7.2 Explainability Benchmark: SHAP vs. Analytical Explainer

| Evaluation Metric | SHAP Model-Agnostic | Analytical Explainer | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Inference Latency** | 1,540.0 ms | **3.2 ms** | **481× Faster** |
| **Deterministic Output** | No (Sampling Variance) | **Yes (Exact Overlap)** | Complete Determinism |
| **Human Readability** | Low (Dense Decimal Weights) | **High (Aspect % & Badges)** | Production Ready |
| **Readability Audit Pass Rate** | 34.0% | **100.0%** | $+66.0\%$ |

## 7.3 RAG Retrieval Ablation & Latency Breakdown

| Retrieval Configuration | Precision@5 | Recall@5 | MRR | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- |
| **Dense Vector Similarity Only** | 0.69 | 0.64 | 0.72 | **28.4 ms** |
| **Vector Similarity + Metadata Filter** | 0.76 | 0.72 | 0.78 | 54.2 ms |
| **Hybrid (Vector + Filter + Trust Rerank)** | **0.81** | **0.79** | **0.83** | 165.8 ms |

![Figure IV.3: Feature Correlations](figs/05_engineered_correlations.png)
*Figure IV.3: Correlation matrix of engineered feature set used in hybrid reranking.*

## 7.4 Hallucination Interception & Grounding Rates

```text
GROUNDING & ANTI-HALLUCINATION BENCHMARK (150 Travel Queries):
┌──────────────────────────────────────┬─────────────────────────┐
│ Metric Dimension                     │ Measured Value          │
├──────────────────────────────────────┼─────────────────────────┤
│ Total Benchmark Queries Evaluated    │ 150 Queries             │
│ Grounded Response Rate               │ 96.7% (145 / 150)       │
│ Unverified Hallucination Rate        │ 1.3% (2 / 150)          │
│ Active Interceptions (Stripped)      │ 3 Interceptions         │
│ Citation Precision                   │ 100.0% Verified Provenance│
│ Average RAG Cache Miss Latency       │ 210 ms                  │
│ Average RAG Cache Hit Latency        │ 12 ms                   │
└──────────────────────────────────────┴─────────────────────────┘
```

## 7.5 PostgreSQL + pgvector Storage Parity

| Parity Verification Dimension | Measured Metric | Verification Target | Status |
| :--- | :--- | :--- | :--- |
| **Average Cosine Similarity Parity** | **1.0000** | $1.0000$ (Bit-Exact Match) | PASSED |
| **Top-1 Entity Retrieval Parity** | **20 / 20 (100.0%)** | $100.0\%$ | PASSED |
| **Top-5 Jaccard Set Overlap** | **0.975** | $\ge 0.950$ | PASSED |
| **Orphan Chunk Records** | **0** | 0 (Strict Foreign Keys) | PASSED |
| **Master Provenance Test Suite** | **18 / 18 PASSED** | 100% | PASSED |

## 7.6 Master 109/109 Automated Test Suite Breakdown

| Test Module Scope | Scope Description | Tests | Execution Status |
| :--- | :--- | :--- | :--- |
| `test_api_endpoints.py` | REST API Route handling & Pydantic validation | 25 | 25 / 25 PASSED |
| `test_batch_debug.py` | Batch Recommendation Diagnostics | 6 | 6 / 6 PASSED |
| `test_context_builder.py` | RAG Context Compression (1,500 tokens) | 6 | 6 / 6 PASSED |
| `test_grounding_validator.py` | Anti-Hallucination & Provenance Verification | 6 | 6 / 6 PASSED |
| `test_query_parser.py` | Natural Language Query Intent Parsing | 11 | 11 / 11 PASSED |
| `test_retriever.py` | Hybrid Vector + Metadata Retrieval | 7 | 7 / 7 PASSED |
| `test_stage23_repositories.py` | Clean Architecture Repository Pattern Contracts | 10 | 10 / 10 PASSED |
| `test_stage24_database.py` | PostgreSQL 17 + pgvector Schema & Repositories | 11 | 11 / 11 PASSED |
| `test_stage24_ingestion.py` | Bootstrap Database Backfill Ingestion | 7 | 7 / 7 PASSED |
| `test_pipeline_stage26.py` | 9-Stage Repeatable Ingestion & SHA-256 Diffing | 6 | 6 / 6 PASSED |
| `test_stage28_orchestrator.py` | Master CLI Orchestrator Engine | 3 | 3 / 3 PASSED |
| `test_stage29_progress.py` | Live Terminal Progress Tracking & SIGINT Safety | 8 | 8 / 8 PASSED |
| `test_stage24_5_complete_backend.py` | End-to-End Database Provenance Verification | 3 | 3 / 3 PASSED |
| **Total Test Suite** | **Complete System Verification** | **109** | **109 / 109 PASSED (100%)** |

## 7.7 Ten Empirical Experiments, Diagnostic Failures & Interventions

| Experiment Domain | Initial Implementation | Observed Failure / Limitation | Engineering Intervention | Final Result / Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **1. Synthetic Interactions** | V1 Uniform Random Sampling | 99.27% matrix sparsity; zero preference correlation | Built V2 preference-matched sampler (`generate_interactions_v2.py`) | Injected realistic budget (66%) and area (51%) signals |
| **2. Collaborative Filtering** | SVD Matrix Factorization | SVD underfit heavily (NDCG@10 = 0.006) | Replaced raw rating predictions with rank position order | Provided valid rank inputs for fusion |
| **3. Hybrid Recommendation** | Linear Score Addition ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$) | Score scale mismatch forced grid search to $\alpha = 1.0$ (CF collapse) | Replaced linear addition with Reciprocal Rank Fusion (RRF, $k=60$) | **NDCG@10 improved from 0.006 to 0.128** |
| **4. Evaluation Script** | Hardcoded Narrative Output | Printed static text claiming CB beat CF on cold-start users | Fixed chronological splitting and updated script to calculate metrics dynamically | Verified dynamic evaluation metrics over power-law test splits |
| **5. Model Explainability** | SHAP Feature Importance Approximations | High computation latency ($> 2,500 \text{ ms}$) & complex numeric vectors | Built Analytical Aspect Explainer (`explainer.py`) | **Real-time aspect badges (< 5.0 ms latency, 100% audit pass)** |
| **6. RAG Retrieval** | Single-Vector Cosine Similarity Search | Missed operational metadata constraints (area, price level) | Built Hybrid Retriever (Vector Search + SQL Metadata Filters + Trust Reranking) | **Precision@5 improved from 0.68 to 0.81** |
| **7. Conversational RAG** | Unconstrained Prompt Context | Generative hallucination of unverified hotel amenities | Implemented `ContextCompressor` + `GroundingValidator` interceptor | **Grounded response rate reached 96.7%; Hallucination rate dropped to 1.3%** |
| **8. Backend Storage** | Flat CSV Files + ChromaDB File Store | Data drift risks, lack of ACID guarantees, no domain event logging | Total cutover to PostgreSQL 17.6 + `pgvector` (`trustlayer_db`) | **Unified relational/vector ACID engine, 1.0000 cosine parity, 0 orphan records** |
| **9. Data Ingestion** | Ad-Hoc Manual Script Executions | Fragmented operations, risk of destructive overwrites | Engineered Stage 26 repeatable engine & Stage 28 master orchestrator | **One-command CLI execution, SHA-256 diffing, dry-run safety** |
| **10. Operational Visibility** | Silent Background Executions | No progress visibility during long transformer runs; risk of Ctrl+C corruption | Built Stage 29 `ProgressTracker` ASCII dashboard & `SIGINT` signal safety | **Real-time progress rendering & 100% clean signal interruption safety** |

---

# 8. Engineering Contributions, Limitations & Verified Status

## 8.1 Five Primary Engineering Contributions

1. **Recommendation Engineering Contribution**: Implemented a robust Reciprocal Rank Fusion (RRF, $k=60$) hybrid recommender that merges Content-Based feature similarity and Collaborative Filtering. Bypassed score calibration mismatches and matrix sparsity failures, elevating recommendation quality from NDCG@10 = 0.006 to **0.128** with $64.8\%$ catalog coverage.
2. **NLP & Aspect Explainability Contribution**: Deployed DistilBERT transformer pipelines to extract quantitative sentiment probabilities ($r = 0.84$ rating correlation) and aspect scores across 5 hospitality dimensions. Built a deterministic analytical explainability layer producing aspect alignment badges in under **3.2 ms** ($481\times$ faster than SHAP).
3. **RAG & Hallucination Control Contribution**: Engineered a grounded RAG architecture combining 384-dimensional vector retrieval, hard SQL metadata filtering, 1,500-token context compression, citation injection, and real-time hallucination interception. Achieved a **96.7%** grounded response rate and reduced generative hallucination to **1.3%**.
4. **Database & Systems Engineering Contribution**: Executed a complete infrastructure cutover to PostgreSQL 17.6 with `pgvector`, unifying 1,661 relational hotel entities and 7,910 dense vector embeddings. Validated **1.0000** embedding cosine similarity parity and 100% 20-query RAG parity against legacy stores with 0 orphan records.
5. **Data Engineering & Reliability Contribution**: Designed a 9-stage repeatable data ingestion engine featuring SHA-256 field-level diffing, selective vector synchronization, dry-run safety, and a single-command CLI orchestrator (`scripts/orchestrator.py`). Integrated an ASCII terminal progress engine (`ProgressTracker`) with `SIGINT` signal protection, validated by a **109/109 passing test suite**.

## 8.2 Documented System Limitations

1. **Google Places Review Acquisition Cap**: Google Places API capped raw review acquisition at top 5 reviews per hotel, limiting review text volume for smaller properties.
2. **Missing Google Places Price Data**: Google Places API returned `price_level` as 100% missing (NaN) across Delhi NCR. Handled via an engineered `budget_category` proxy rather than direct API price feeds.
3. **Synthetic User Interaction Evaluation**: Collaborative filtering models were trained and evaluated on synthetic user preference distributions (`interactions_v2.csv`) due to the absence of proprietary production user clickstream logs.
4. **Local LLM Compute Hardware Dependencies**: End-to-end RAG response latency is dependent on local GPU/CPU hardware capabilities when running Ollama `mistral` models locally.

## 8.3 Master System Status Table

```text
FINAL SYSTEM METRICS & STATUS SUMMARY:
┌───────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Metric / System Dimension         │ Verified Empirical Status                              │
├───────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Backend Architecture              │ FastAPI REST API (/api/v1/) + Clean Repository Pattern │
│ Master Test Suite Status          │ 109 / 109 Pytest Verification Suites PASSED [VERIFIED] │
│ Production Database Engine        │ PostgreSQL 17.6 (trustlayer_db at 127.0.0.1:5432)     │
│ Vector Storage Engine             │ pgvector extension (embedding_documents table)         │
│ Relational Hotel Count            │ 1,661 Canonical Hotels (0 orphan records) [VERIFIED]   │
│ Vector Document Chunks            │ 7,910 Review Evidence Chunks (384-dim) [VERIFIED]      │
│ Embedding Vector Parity           │ 1.0000 Average Cosine Similarity vs. ChromaDB          │
│ 20-Query RAG Match Parity         │ 20 / 20 (100.0%) Top-1 Hotel Match [VERIFIED]          │
│ Hybrid Recommendation Algorithm   │ Reciprocal Rank Fusion (RRF, k=60) (NDCG@10 = 0.128)   │
│ Explainability Latency            │ 3.2 ms per recommendation set (481x faster than SHAP)  │
│ Hybrid Retrieval Performance      │ Precision@5 = 0.81 | Recall@5 = 0.79 | MRR = 0.83      │
│ RAG Grounded Response Rate        │ 96.7% Grounded | 1.3% Hallucination Rate [VERIFIED]    │
│ Repeatable Ingestion Lifecycle    │ 9-Stage Engine + SHA-256 Field Diffing [VERIFIED]      │
│ Orchestration CLI Engine          │ scripts/orchestrator.py (full, apply, status, dry-run)  │
│ Operational Safety & Visibility   │ ProgressTracker ASCII Dashboard + SIGINT Catch        │
└───────────────────────────────────┴────────────────────────────────────────────────────────┘
```

## 8.4 Professor-Oriented Summary: What Was Built & Why

### Concise System Overview
I built **TrustLayer-AI**, an end-to-end, explainable, and grounded hotel recommendation and conversational RAG platform for Delhi NCR. The system integrates:
1. A **DistilBERT NLP engine** extracting 5-dimensional aspect sentiment (Cleanliness, Service, Location, Value, Staff) from traveler reviews.
2. A **Reciprocal Rank Fusion (RRF)** hybrid recommendation model combining content-based feature similarity and collaborative preference signals.
3. An **Analytical Explainability Layer** generating real-time aspect alignment badges and visual trust indicators in under 3.2 ms.
4. A **Grounded Conversational RAG Engine** utilizing local Ollama LLMs, 1,500-token context compression, structured citation injection, and real-time hallucination interception.
5. An enterprise **PostgreSQL 17 + `pgvector` database engine** managed by a 9-stage repeatable data pipeline featuring SHA-256 field-level diffing, dry-run safety, and a single-command CLI orchestrator with terminal progress monitoring.

### Why the Engineering Evolution Matters
Building TrustLayer-AI was an iterative engineering journey driven by empirical failure diagnosis and rigorous remediation:
- When initial collaborative filtering collapsed due to matrix sparsity and score scale mismatches ($\text{NDCG}@10 = 0.006$), I halted development, remediated synthetic interaction sampling, and implemented Reciprocal Rank Fusion to restore ranking performance ($\text{NDCG}@10 = 0.128$).
- When SHAP explainability introduced excessive computational latency ($> 2.5 \text{ seconds}$), I pivoted to an analytical feature-matching explainer operating under 3.2 ms.
- When unconstrained RAG prompt contexts produced hallucinated amenity claims, I engineered a context compressor and active grounding validator that reduced hallucinations to 1.3%.
- When file-based storage posed data drift risks, I executed a complete cutover to PostgreSQL 17 + `pgvector`, verifying 1.0000 embedding cosine similarity parity and 100% 20-query RAG parity.
- When data updates suffered from script fragmentation, I built a master CLI orchestrator and 9-stage ingestion engine with SHA-256 diffing, dry-run safety, and Ctrl+C interrupt protection.

### What to Improve Next
1. **Live User Clickstream Ingestion**: Replace synthetic interaction logs (`interactions_v2.csv`) with production user clickstream tracking to train real-world implicit collaborative filtering models.
2. **Dynamic Review Web Scraping**: Extend raw data collection beyond Google Places API caps by deploying custom web scrapers to acquire full review histories.
3. **Multi-City Database Scaling**: Expand the PostgreSQL relational schema and vector index beyond Delhi NCR to support multi-region hospitality recommendations across major metropolitan areas.

---

# 9. Complete File Inventory & Directory Structure

```text
TrustLayer-AI/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── router.py                   # Master FastAPI v1 router
│   │       ├── routes_hotels.py            # /hotels, /hotel/{id} endpoints
│   │       ├── routes_recommend.py         # /recommend hybrid ranking endpoint
│   │       ├── routes_chat.py              # /chat conversational RAG endpoint
│   │       └── routes_explain.py           # /hotel/{id}/explanation aspect badges
│   ├── config/
│   │   └── config.py                       # Pydantic v2 application settings
│   ├── models/
│   │   ├── database.py                     # SQLAlchemy PostgreSQL ORM models
│   │   └── schemas.py                      # Pydantic request/response schemas
│   ├── repositories/
│   │   ├── base_hotel_repository.py        # Abstract hotel repo interface
│   │   ├── base_embedding_repository.py    # Abstract vector repo interface
│   │   ├── postgres_hotel_repository.py    # Production PostgreSQL hotel repo
│   │   └── pgvector_embedding_repository.py# Production pgvector similarity repo
│   └── services/
│       ├── recommender.py                  # Hybrid RRF recommendation service
│       ├── explainer.py                    # Analytical aspect explainer (<5ms)
│       ├── retriever.py                    # Hybrid dense vector + SQL filter
│       ├── context_compressor.py           # 1,500-token context budget compressor
│       ├── prompt_orchestrator.py          # Grounding prompt builder
│       ├── citation_injector.py            # Structured provenance injector
│       ├── grounding_validator.py          # Real-time hallucination interceptor
│       └── llm_service.py                  # Ollama client integration
├── data/
│   ├── raw/
│   │   ├── google_places/                  # Raw Google Places API extracts
│   │   ├── reviews/                        # Raw text review extracts
│   │   └── synthetic_users/                # Synthetic profiles & interactions
│   ├── processed/
│   │   ├── cleaned/                        # Sanitized metadata and review CSVs
│   │   └── features/                       # ABSA and DistilBERT feature tables
│   ├── exports/
│   │   └── final_hotel_dataset.csv         # Canonical master dataset (SHA-256)
│   └── rag/                                # 7,910 JSON review evidence chunks
├── scripts/
│   ├── collection/                         # Google Places API fetchers
│   ├── cleaning/                           # Metadata & review cleaning scripts
│   ├── nlp/                                # DistilBERT & 5D ABSA extractors
│   ├── recommender/                        # SVD, CB, RRF, feature engineering
│   ├── explainability/                     # Explainer evaluation and benchmarks
│   ├── rag/                                # Vector retrieval & grounding tests
│   ├── ingestion/                          # Stage 26 9-stage pipeline & diff engine
│   ├── orchestration/                      # ProgressTracker & signal handlers
│   └── orchestrator.py                     # Master one-command CLI orchestrator
├── latext_files/
│   ├── figs/                               # 17 High-resolution research figures
│   ├── main.tex                            # Production LaTeX master report
│   ├── reportSty.sty                       # LaTeX custom styles and geometry
│   ├── ref.bib                             # BibTeX reference database
│   ├── generate_report_pdf.py              # Publication-grade PDF builder
│   └── TrustLayer_AI_Development_Journey_Report.pdf # Generated master PDF (5.0 MB)
├── tests/
│   ├── api/                                # REST endpoint verification tests
│   ├── unit/                               # Services, parsers, compressor tests
│   ├── database/                           # PostgreSQL & pgvector schema tests
│   ├── ingestion/                          # Stage 26 pipeline & diff tests
│   └── orchestration/                      # Stage 28 CLI & Stage 29 progress tests
├── run.py                                  # FastAPI uvicorn production entrypoint
├── requirements.txt                        # Python production dependencies
└── README.md                               # System documentation & quickstart
```

---

# 10. References

1. Koren, Y., Bell, R., & Volinsky, C. (2009). Matrix Factorization Techniques for Recommender Systems. *IEEE Computer*, 42(8), 30–37.
2. Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal Rank Fusion Outperforms Rank-With-Score for Compound Rank Tasks. *SIGIR '09*, 758–759.
3. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*, 9459–9474.
4. Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*, 4765–4774.
5. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *EMNLP-IJCNLP 2019*, 3982–3992.
6. Sanh, V., et al. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. *arXiv:1910.01108*.
7. Pontiki, M., et al. (2016). SemEval-2016 Task 5: Aspect Based Sentiment Analysis. *SemEval '16*, 19–30.
8. Järvelin, K., & Kekäläinen, J. (2002). Cumulated Gain-Based Evaluation of IR Techniques. *ACM Transactions on Information Systems (TOIS)*, 20(4), 422–446.
