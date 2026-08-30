# TRUSTLAYER-AI — COMPLETE FORENSIC DEVELOPMENT HISTORY

## Executive Summary & Document Metadata
- **Project Title**: TrustLayer-AI (Explainable RAG & Hybrid Hotel Recommendation Engine)
- **Document Type**: Master Forensic Chronological Reconstruction & Development Source of Truth
- **Purpose**: Serve as the comprehensive, empirical historical source of truth for LaTeX technical report and presentation generation.
- **Verification Methodology**: Complete repository audit (Source Code, SQL Databases, JSON Artifacts, Pytest Verification Suites, Markdown Stage Reports, Jupyter Research Notebooks).
- **Final Backend Status**: **PRODUCTION READY** | **50 / 50 Pytest Verification Suites PASSED** | Real PostgreSQL 17.6 + pgvector storage engine (`trustlayer_db` at `127.0.0.1:5432`).

---

## 0. Project Origin & Foundational Vision

### 0.1 Initial Motivation & Problem Statement
TrustLayer-AI was conceived to solve critical trust, grounding, and explainability deficiencies in traditional e-commerce and hospitality recommendation platforms:
1. **Black-Box Recommendations**: Standard Collaborative Filtering (CF) and Matrix Factorization (SVD) algorithms produce item rankings without actionable or transparent justification for *why* a specific hotel was recommended to a specific user profile.
2. **Hallucination in Conversational AI**: Naive Large Language Model (LLM) interfaces tend to invent non-existent hotel amenities, exaggerate review sentiment, or cite untraceable sources when answering complex traveler queries.
3. **Data Drift & Unaudited Pipeline Updates**: Ingestion systems frequently perform destructive database overwrites and full embedding recalculations, corrupting historical data lineage and making vector searches non-deterministic.

### 0.2 Core Architectural Objectives
- **Hybrid Recommendation Engine**: Combine Content-Based (CB) feature similarity and Collaborative Filtering (CF) with Reciprocal Rank Fusion (RRF).
- **Multi-Dimensional Aspect Explainability**: Extract granular sentiment across key hospitality aspects (Cleanliness, Service, Location, Value, Staff Behavior) to generate transparent explanation badges.
- **Hybrid RAG & Grounded Generation**: Retrieve text evidence chunks via vector search and metadata filters, passing them through a token-budget aware context compressor, prompt orchestrator, and strict hallucination stripping validator.
- **Enterprise Data Platform**: Deploy PostgreSQL 17.6 with `pgvector`, clean repository patterns, a 9-stage repeatable ingestion pipeline with SHA-256 field-level diffing, dry-run safety, and a single-command master orchestrator with live terminal progress monitoring.

---

## 1. Document Inventory & Artifact Register

Below is the complete inventory of historical, operational, audit, and analytical artifacts discovered across the repository:

| Filename | Full Relative Path | File Type | Referenced Stage | Primary Purpose | Implementation State | Key Findings / Metrics |
|---|---|---|---|---|---|---|
| `delhi_hotels_raw.csv` | `data/raw/google_places/` | Data CSV | Stage 1 | Raw Google Places API payload | Historical Baseline | 1,661 raw hotel records acquired |
| `reviews_raw.csv` | `data/raw/reviews/` | Data CSV | Stage 1 | Raw Google Places text reviews | Historical Baseline | Capped at 5 reviews per hotel (Google Places API detail limit) |
| `delhi_hotels_cleaned.csv` | `data/processed/cleaned/` | Data CSV | Stage 2 | Cleaned & imputed hotel metadata | Active Source | Zero nulls in core fields; price_level 100% missing (NaN) |
| `reviews_cleaned.csv` | `data/processed/cleaned/` | Data CSV | Stage 2 | Standardized review text | Active Source | Regex string normalization applied |
| `review_features.csv` | `data/processed/features/` | Data CSV | Stage 3 | NLP sentiment extraction outputs | Active Source | DistilBERT positive sentiment probabilities |
| `explainability_features.csv`| `data/processed/features/` | Data CSV | Stage 3 | Aspect sentiment scores (ABSA) | Active Source | Aspect scores: Cleanliness, Service, Location, Value, Staff |
| `hotel_features.csv` | `data/processed/features/` | Data CSV | Stage 4 | Engineered hotel scores | Active Source | Trust score (0.68 mean), Popularity score (power-law) |
| `final_hotel_dataset.csv` | `data/exports/` | Data CSV | Stage 4 / 28 | Master canonical dataset | Canonical Handoff | 1,661 hotels, 26 features, SHA-256 `eca959c788...` |
| `users.csv` | `data/raw/synthetic_users/` | Data CSV | Stage 5 | Synthetic user demographic profiles | Historical Baseline | 500 synthetic users |
| `interactions.csv` | `data/raw/synthetic_users/` | Data CSV | Stage 5 | Initial synthetic interaction matrix | Deprecated / Flawed | 5,000 interactions; 99.27% matrix sparsity; random noise |
| `interactions_v2.csv` | `data/raw/synthetic_users/` | Data CSV | Stage 6.1 / A.1 | Remediated synthetic interactions | Active Benchmark | Power-law distribution; budget match 66%, area match 51% |
| `01_hotel_metadata_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Metadata EDA & geospatial plotting | Analytical Evidence | Identified hotel spatial density in central Delhi & airport corridor |
| `02_review_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Review distribution & length EDA | Analytical Evidence | Review positivity skew (median rating 4.10) |
| `03_sentiment_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Sentiment NLP validation | Analytical Evidence | DistilBERT sentiment vs rating Pearson correlation ~0.84 |
| `04_absa_explainability_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | ABSA aspect variance analysis | Analytical Evidence | Cleanliness identified as primary variance differentiator |
| `05_feature_engineering_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Score distribution analysis | Analytical Evidence | Trust Score normally distributed; Popularity follows power-law |
| `06_user_dataset_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | User demographic preference EDA | Analytical Evidence | Verified synthetic user preference distributions |
| `07_interaction_analysis.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Interaction matrix sparsity EDA | Analytical Evidence | Quantified interaction sparsity and user-item overlap |
| `08_final_dataset_overview.ipynb` | `research/notebooks/` | Notebook | Stage 11.75 | Master feature correlation EDA | Analytical Evidence | Heatmap confirming independence of Trust vs Popularity |
| `09_recommender_diagnostics.ipynb` | `research/notebooks/` | Notebook | Stage A | Diagnostic notebook for Stage A | Forensic Evidence | Verified SVD underfitting and CF collapse ($\alpha=1.0$) |
| `10_interaction_quality_audit.ipynb` | `research/notebooks/` | Notebook | Stage A.1 | V2 interaction quality audit | Forensic Evidence | Confirmed successful injection of CF preference signals |
| `recommender_diagnostics.md` | `research_and_audit_reports/` | Report | Stage A | Recommender diagnostic audit | Historical Audit | Triggered NO-GO decision for Stage B/C/D due to CF failure |
| `recommender_remediation_report.md`| `research_and_audit_reports/` | Report | Stage A.1 | Recommender remediation report | Historical Audit | Implemented RRF & V2 interactions; NDCG@10 improved to >0.12 |
| `explainability_evaluation.md` | `research_and_audit_reports/` | Report | Stage B | Explainability evaluation | Current Report | Replaced SHAP with analytical feature-matching explainer |
| `explainability_audit_b1.md` | `research_and_audit_reports/` | Report | Stage B.1 | Explainability audit | Current Report | Formal edge-case audit passed |
| `retrieval_evaluation.md` | `research_and_audit_reports/` | Report | Stage C.4 | Retrieval evaluation & ablation | Current Report | Precision@5 0.81, Recall@5 0.79, MRR 0.83, NDCG@5 0.85 |
| `hybrid_rag_upgrade_report.md` | `research_and_audit_reports/` | Report | Stage G / RAG | Hybrid RAG architecture upgrade | Current Report | Added PromptOrchestrator, ContextCompressor, CitationInjector |
| `stage_d_evaluation.md` | `research_and_audit_reports/` | Report | Stage D | RAG end-to-end evaluation | Current Report | Grounded response rate 96.7%, Hallucination rate 1.3% |
| `runtime_mock_audit.md` | `research_and_audit_reports/` | Report | Stage E | API route hardcode audit | Current Report | Replaced mock routes with real Stage B/C/D service calls |
| `frontend_validation_report.md`| `research_and_audit_reports/` | Report | Stage E | Frontend validation report | Current Report | TanStack Query integration verified |
| `STAGE23.1_BACKEND_AUDIT_REPORT.md` | `architecture_and_system_docs/stage23/` | Report | Stage 23.1 | Clean repository abstraction audit | Current Report | Abstract contracts defined; CSV/Chroma/JSON repositories |
| `STAGE24.1_MANUAL_BACKEND_VERIFICATION_REPORT.md` | `architecture_and_system_docs/stage24/` | Report | Stage 24.1 | SQLite baseline backend audit | Current Report | Identified vector store gap in relational SQL |
| `STAGE24.2_PGVECTOR_BACKFILL_REPORT.md` | `architecture_and_system_docs/stage24.2/` | Report | Stage 24.2 | pgvector backfill & parity report | Current Report | Backfilled 7,910 chunks to pgvector; 1.0000 cosine similarity |
| `STAGE24.4_REAL_POSTGRESQL_DEPLOYMENT_REPORT.md` | `architecture_and_system_docs/stage24/` | Report | Stage 24.4 | Real PostgreSQL 17 deployment | Current Report | Deployed PostgreSQL 17.6 `trustlayer_db` |
| `STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md` | `architecture_and_system_docs/stage24/` | Report | Stage 24.5 | Master backend provenance audit | Current Report | 18/18 tests passed; 1,661 hotels, 7,910 vectors, 0 orphans |
| `STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md` | `architecture_and_system_docs/data_pipeline/` | Report | Stage 26 | Repeatable data ingestion engine | Current Report | 9-stage ingestion lifecycle; SHA-256 diff; dry-run safety |
| `STAGE27_ORCHESTRATION_GAP_ANALYSIS.md` | `architecture_and_system_docs/stage27/` | Report | Stage 27 | Full pipeline integration audit | Current Report | Identified upstream script fragmentation |
| `STAGE28_PRE_IMPLEMENTATION_AUDIT.md` | `architecture_and_system_docs/stage28/` | Report | Stage 28 | Orchestrator call graph audit | Current Report | Mapped exact entrypoints, parameters, dependencies |
| `STAGE28_FINAL_REPORT.md` | `architecture_and_system_docs/stage28/` | Report | Stage 28 | One-command orchestrator report | Current Report | Implemented `scripts/orchestrator.py`; 6/6 tests passed |
| `STAGE29_LIVE_PROGRESS_REPORT.md` | `architecture_and_system_docs/stage29/` | Report | Stage 29 | Live progress & SIGINT report | Current Report | Implemented `ProgressTracker` ASCII dashboard & Ctrl+C safety |

---

## 3. Detailed Chronological Stage-by-Stage Reconstruction

### 3.1 Stage 1: Data Collection & Raw Ingestion
- **Stage Name**: Stage 1 — Data Collection
- **Approximate Date**: Early Project Phase
- **Objective / Problem**: Acquire baseline hotel metadata and real traveler review text for Delhi NCR.
- **Previous System State**: Empty repository; no data.
- **Work Implemented**: Wrote custom API integration scripts (`scripts/collection/fetch_google_places.py` and `fetch_google_reviews.py`) calling the Google Places API and Google Places Detail API.
- **Files Created**: `data/raw/google_places/delhi_hotels_raw.csv`, `data/raw/reviews/reviews_raw.csv`.
- **Data & Volumes Involved**: 1,661 hotels collected; reviews capped at 5 per hotel due to Google Places API Detail request limits.
- **Algorithms / Models**: Google Places Text Search and Place Details REST API integration.
- **Tests & Validation**: Checked API response HTTP 200 statuses and verified non-empty raw CSV structures.
- **Problems Encountered**: `price_level` parameter returned 100% missing (NaN) across all 1,661 hotels due to API coverage limitations in India.
- **Fixes Applied**: Flagged `price_level` for proxy engineering in Stage 4 (`budget_category`).
- **Design Decisions**: Capped review fetching to top 5 reviews per hotel to prevent API quota exhaustion while maintaining baseline text density.
- **Enablement**: Provided raw tabular metadata and review text for downstream cleaning.

---

### 3.2 Stage 2: Data Cleaning & Text Normalization
- **Stage Name**: Stage 2 — Data Cleaning
- **Approximate Date**: Post-Collection Phase
- **Objective / Problem**: Remove noisy records, handle null values, standardize string representations, and filter geographic outliers.
- **Previous System State**: Raw CSV files containing unformatted strings, trailing whitespace, missing coordinates, and inconsistent column types.
- **Work Implemented**: Developed `scripts/cleaning/clean_hotel_metadata.py` and `clean_reviews.py`. Applied regex text normalization, coordinate bounding-box filtering for Delhi NCR, and string deduplication.
- **Files Created**: `data/processed/cleaned/delhi_hotels_cleaned.csv`, `data/processed/cleaned/reviews_cleaned.csv`, `research/reports/data_quality_report.md`.
- **Data & Volumes Involved**: Cleaned 1,661 hotels; 1,618 hotels preserved valid review text (43 hotels had 0 reviews).
- **Algorithms / Models**: Regex normalization, spatial bounding-box filtering.
- **Tests & Validation**: Automated null-count verification, coordinate validity checks.
- **Results Obtained**: 100% valid lat/long coordinates within Delhi NCR; zero nulls in essential fields (`hotel_id`, `name`, `address`, `rating`).
- **Enablement**: Produced high-quality cleaned tabular data ready for NLP feature extraction.

---

### 3.3 Stage 3: NLP Pipeline (Sentiment Analysis & ABSA)
- **Stage Name**: Stage 3 — NLP Pipeline (Sentiment & Aspect Extraction)
- **Approximate Date**: NLP Research Phase
- **Objective / Problem**: Transform qualitative review text into quantitative sentiment probabilities and aspect-specific scores.
- **Previous System State**: Cleaned raw text reviews without quantitative sentiment tags.
- **Work Implemented**: Built `scripts/nlp/analyze_sentiment.py` using pre-trained DistilBERT PyTorch models (`transformers` pipeline) to compute sentence-level sentiment polarity. Built `scripts/nlp/extract_absa_features.py` using keyword matching and sentiment masking to compute 5 aspect sentiment scores (Cleanliness, Service, Location, Value for Money, Staff Behavior).
- **Files Created**: `data/processed/features/review_features.csv`, `data/processed/features/explainability_features.csv`, `research/notebooks/03_sentiment_analysis.ipynb`, `04_absa_explainability_analysis.ipynb`.
- **Data & Volumes Involved**: Evaluated reviews across 1,618 hotels.
- **Algorithms / Models**: DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`), Aspect Keyword Masking Engine.
- **Results & Findings**:
  - DistilBERT positive sentiment probabilities correlated strongly with user star ratings (**Pearson $r \approx 0.84$**).
  - **Cleanliness** exhibited the highest score variance among aspects, establishing it as the primary differentiator among Delhi NCR hotels.
- **Enablement**: Quantified review text into aspect feature vectors for downstream recommender modeling and explainability.

---

### 3.4 Stage 4: Feature Engineering & Master Dataset Consolidation
- **Stage Name**: Stage 4 — Feature Engineering
- **Approximate Date**: Pre-Modeling Phase
- **Objective / Problem**: Engineer holistic quality metrics (Trust Score, Popularity Score) and consolidate all metadata, NLP sentiment, and aspect scores into a single canonical dataset.
- **Previous System State**: Disparate feature CSVs (`delhi_hotels_cleaned.csv`, `review_features.csv`, `explainability_features.csv`).
- **Work Implemented**: Developed `scripts/recommender/engineer_features.py`, `aggregate_reviews.py`, and `merge_dataset.py`. Calculated `trust_score` (composite weighted score combining star rating, sentiment probability, and review volume) and `popularity_score` (normalized review volume). Imputed NaN aspect scores for the 43 zero-review hotels using area-cluster median imputation. Engineered `budget_category` proxy based on location and rating.
- **Files Created**: `data/processed/features/hotel_features.csv`, `data/processed/features/hotel_review_summary.csv`, `data/exports/final_hotel_dataset.csv`, `research/notebooks/05_feature_engineering_analysis.ipynb`, `08_final_dataset_overview.ipynb`.
- **Data & Volumes Involved**: **1,661 hotels, 26 feature columns**.
- **Algorithms / Models**: `scikit-learn` `MinMaxScaler`, median cluster imputation.
- **Results & Findings**:
  - `trust_score` followed a Gaussian distribution centered at **0.68**.
  - `popularity_score` followed a steep power-law distribution.
  - Correlation between Trust and Popularity was near zero ($r \approx 0.05$), proving they represent orthogonal evaluation signals.
- **Enablement**: Created canonical dataset `final_hotel_dataset.csv` (SHA-256: `eca959c788d9535feea5ed1b11efb249988c60b6bfb7b4bb41ef33e50bad1e2e`).

---

### 3.5 Stage 5: Synthetic User Generation & Cold-Start Modeling
- **Stage Name**: Stage 5 — Synthetic User Generation
- **Approximate Date**: Interaction Modeling Phase
- **Objective / Problem**: Overcome the cold-start barrier by generating synthetic traveler profiles and interaction logs (clicks, bookings, reviews).
- **Previous System State**: Hotel dataset available, but zero user interaction logs for Collaborative Filtering (CF).
- **Work Implemented**: Developed `scripts/recommender/generate_users.py` and `generate_interactions.py` using `faker` and `numpy`.
- **Files Created**: `data/raw/synthetic_users/users.csv`, `data/raw/synthetic_users/interactions.csv`, `research/notebooks/06_user_dataset_analysis.ipynb`, `07_interaction_analysis.ipynb`.
- **Data & Volumes Involved**: 500 synthetic users, 5,000 synthetic interactions.
- **Flaw Discovered**: Initial synthetic interactions were generated with excess uniform randomness, resulting in a **99.27% matrix sparsity** and zero correlation between stated user preferences and interaction choices.

---

### 3.6 Stage 6 & Stage A: Initial Recommender Development & Failure Audit
- **Stage Name**: Stage 6 / Stage A — Baseline Recommender Modeling
- **Approximate Date**: Initial Model Evaluation Phase
- **Objective / Problem**: Train Baseline, Content-Based (CB), Collaborative Filtering (SVD), and Hybrid models.
- **Work Implemented**: Built `scripts/recommender/baseline.py`, `collaborative.py`, `content_based.py`, `hybrid.py`.
- **Models Trained**: SVD Matrix Factorization, Cosine Content Similarity, Linear Blended Hybrid ($\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$).
- **Catastrophic Failure Discovered**:
  - Offline evaluation yielded abysmal metrics: **Precision@10 = 0.002, Recall@10 = 0.010, NDCG@10 = 0.006** (barely above random guessing).
  - The Hybrid model grid search defaulted to $\alpha = 1.0$, completely disabling Content-Based filtering.
  - SVD underfit heavily due to 99.27% matrix sparsity (~3.6 interactions/hotel).
  - Score calibration mismatch: CB output dense cosine similarities (0.8–0.9), while CF output raw ratings (1.0–5.0).
  - Evaluation script printed hardcoded narrative text claiming CB beat CF on cold-start users, but audit proved **zero cold-start users** existed in the test set due to strict 70/30 user-level splitting across fixed 10-interaction profiles.
- **Reports Generated**: `research_and_audit_reports/recommender_diagnostics.md`, `research/notebooks/09_recommender_diagnostics.ipynb`.
- **Formal Decision**: **NO-GO for Stage B / C / D**. Project halted until data generation and hybrid fusion logic were repaired.

---

### 3.7 Stage 6.1 & Stage A.1: Recommender Remediation & Rank Fusion
- **Stage Name**: Stage 6.1 / Stage A.1 — Recommendation Remediation
- **Approximate Date**: Model Remediation Phase
- **Objective / Problem**: Fix synthetic interaction quality, resolve score calibration mismatches, and fix evaluation reporting.
- **Work Implemented**:
  1. Overhauled interaction generator: `scripts/synthetic/generate_interactions_v2.py`. Injected realistic preference matching (budget match rate 66%, area match rate 51%) and power-law user activity distribution.
  2. Replaced linear score blending in `hybrid.py` with **Reciprocal Rank Fusion (RRF)**:
     $$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
     where $k=60$, bypassing score calibration mismatches by fusing ordinal ranks.
  3. Fixed evaluation script to dynamically compute cold-start metrics over power-law interaction distributions.
- **Files Created**: `data/raw/synthetic_users/interactions_v2.csv`, `research_and_audit_reports/recommender_remediation_report.md`, `research/notebooks/10_interaction_quality_audit.ipynb`.
- **Results Obtained**: **NDCG@10 improved from 0.006 to > 0.12**, Precision@10 and Recall@10 passed quality thresholds, popularity bias was mitigated.
- **Formal Decision**: **GO for Stage B & Stage C**.

---

### 3.8 Stage 7, Stage 7.1 & Stage B: Explainability Layer Development
- **Stage Name**: Stage 7 / Stage B — Explainability Layer & Audit
- **Approximate Date**: Explainability Phase
- **Objective / Problem**: Provide human-readable, transparent explanations for hybrid recommendations.
- **Initial Abandoned Approach**: Attempted SHAP (SHapley Additive exPlanations) approximations, but abandoned SHAP due to prohibitive computation latency and non-deterministic feature attributions over rank-fused outputs.
- **Work Implemented**: Built **Analytical Explainability Layer** (`scripts/explainability/explainer.py`). Computed direct feature alignment scores between user preference vectors and hotel aspect scores (Cleanliness, Service, Location, Value, Staff), generating transparent explanation badges.
- **Files Created**: `scripts/explainability/explainer.py`, `evaluate_explanations.py`, `audit_explainability_b1.py`, `research_and_audit_reports/explainability_evaluation.md`, `explainability_audit_b1.md`.
- **Tests & Audit**: Audited edge cases across 100 sample user profiles. 100% logic validation passed.

---

### 3.9 Stage C: RAG Vector Store & Retrieval Optimization
- **Stage Name**: Stage C — RAG Vector Store & Retrieval Pipeline
- **Approximate Date**: RAG Foundation Phase
- **Objective / Problem**: Segment hotel review data into searchable chunks and build a hybrid vector retrieval pipeline.
- **Work Implemented**:
  1. Chunked 1,661 hotels into **7,910 review evidence chunks** (`data/rag/ChIJ*.json`).
  2. Initialized ChromaDB file-based vector store (`data/vector_store/`) using `all-MiniLM-L6-v2` embeddings (384 dimensions).
  3. Built `scripts/rag/retriever.py` supporting Semantic Vector Search + Metadata Filtering (area, budget) + Recommender Reranking.
- **Files Created**: `research_and_audit_reports/hotel_document_audit.md`, `review_evidence_coverage.md`, `vector_store_audit.md`, `retrieval_evaluation.md`.
- **Ablation Study Results**:
  - Semantic Only: Precision@5 = 0.68, Recall@5 = 0.65, MRR = 0.70, NDCG@5 = 0.71
  - + Metadata Filtering: Precision@5 = 0.75, Recall@5 = 0.73, MRR = 0.78, NDCG@5 = 0.79 (+0.07 ΔP)
  - Full Hybrid (Vector + Metadata + Rec Signal): **Precision@5 = 0.81, Recall@5 = 0.79, MRR = 0.83, NDCG@5 = 0.85** (+0.05 ΔP)
- **Latency Breakdown**: Embedding generation (12.4 ms), ChromaDB search (145.2 ms), Metadata filtering (2.1 ms), Reranking (4.3 ms), Context Assembly (1.8 ms) = **Total 165.8 ms**.
- **Formal Decision**: **14/14 Retrieval Success Gates PASSED. GO for Stage D**.

---

### 3.10 Stage D & Stage G: LLM Generation, Grounding & Hybrid RAG Architecture
- **Stage Name**: Stage D / Stage G — LLM Generation, Grounding & Hybrid RAG Upgrade
- **Approximate Date**: Conversational AI Phase
- **Objective / Problem**: Orchestrate LLM answer generation with strict provenance citation and hallucination protection.
- **Work Implemented**:
  - Integrated local Ollama LLM execution (`mistral` / `llama3`).
  - Implemented `PromptOrchestrator` (`app/services/prompt_orchestrator.py`) to inject grounding constraints.
  - Implemented `ContextCompressor` (`app/services/context_compressor.py`) to enforce a 1,500-token context budget and label chunks with `[Chunk ID: XYZ]`.
  - Implemented `CitationInjector` (`app/services/citation_injector.py`) to parse inline citations into structured `ProvenanceChunk` JSON objects.
  - Built `GroundingValidator` (`app/services/grounding_validator.py`) to intercept and re-prompt responses containing ungrounded amenity claims.
- **Files Created**: `research_and_audit_reports/stage_d_evaluation.md`, `hybrid_rag_upgrade_report.md`, `ollama_integration_verification.md`.
- **Evaluation Results over 150 Benchmark Queries**:
  - Grounded Response Rate: **96.7%** (Target $\ge 95\%$)
  - Hallucination Rate: **1.3%** (Target $\le 2\%$)
  - GroundingValidator Interceptions: **3 active interceptions** (stripped fabricated spa/shuttle claims).
  - Cache Miss Latency: 210 ms | Cache Hit Latency: 12 ms.

---

### 3.11 Stage E & Stage F: API Integration, Frontend & System Hardening
- **Stage Name**: Stage E / Stage F — Frontend & API System Hardening
- **Approximate Date**: System Integration Phase
- **Objective / Problem**: Connect FastAPI backend endpoints to React frontend UI and audit runtime mocks.
- **Work Implemented**:
  - Built versioned FastAPI routes (`/api/v1/hotels`, `/api/v1/hotel/{id}`, `/api/v1/recommend`, `/api/v1/chat`, `/api/v1/hotel/{id}/explanation`, `/api/v1/hotel/{id}/evidence`).
  - Audited API endpoints for hardcoded responses (`research_and_audit_reports/runtime_mock_audit.md`, `frontend_hardcode_audit.md`). Replaced hardcoded explanation stubs with live calls to `explainer.py` and vector retriever.
  - Connected React + TypeScript + TanStack Query frontend (`frontend/`). Verified live rendering of progress bars, trust badges, trace IDs, and provenance drawers.
- **Files Created**: `research_and_audit_reports/ui_verification.md`, `frontend_validation_report.md`, `final_project_audit.md`, `final_system_report.md`.

---

### 3.12 Stage 23 & 23.1: Backend Repository Layer Abstraction
- **Stage Name**: Stage 23 / 23.1 — Backend Repository Layer Abstraction
- **Approximate Date**: Infrastructure Refactoring Phase
- **Objective / Problem**: Decouple FastAPI services from direct CSV and ChromaDB file access using the Clean Architecture Repository Pattern.
- **Work Implemented**: Defined abstract base contracts (`BaseHotelRepository`, `BaseTraceRepository`, `BaseEmbeddingRepository`). Built concrete file adapters (`CsvHotelRepository`, `JsonTraceRepository`, `ChromaEmbeddingRepository`). Configured centralized settings in `app/config/config.py`.
- **Files Created**: `architecture_and_system_docs/stage23/STAGE23.1_BACKEND_AUDIT_REPORT.md`, `app/repositories/`.
- **Audit Verification**: Verified 100% read-only data access across 1,661 CSV hotels, 20 JSON trace runs, and 7,910 ChromaDB vector chunks over 20 recommendation queries without data mutation.

---

### 3.13 Stage 24 & 24.1–24.5: PostgreSQL & pgvector Infrastructure Cutover
- **Stage Name**: Stage 24 (24.1 → 24.5) — Real PostgreSQL 17 & pgvector Deployment
- **Approximate Date**: Enterprise Database Migration Phase
- **Objective / Problem**: Migrate backend storage from CSV, ChromaDB, and SQLite to enterprise PostgreSQL 17 with `pgvector` for unified relational and vector ACID transactions.
- **Work Implemented**:
  1. Deployed PostgreSQL 17.6 database engine (`trustlayer_db` at `127.0.0.1:5432`).
  2. Created normalized relational schema (`hotels`, `hotel_locations`, `hotel_scores`, `hotel_sources`, `hotel_amenities`, `hotel_provenance`, `embedding_documents`, `domain_events`, `ingestion_records`, `ingestion_runs`).
  3. Developed `PostgresHotelRepository` and `PgVectorEmbeddingRepository` (`app/repositories/`).
  4. Executed `scripts/ingestion/backfill_pgvector.py` in transactional batches of 200 chunks. Backfilled **7,910 chunks** into pgvector storage (`384` dimensions).
- **Parity & Validation Results** (`STAGE24.2_PGVECTOR_BACKFILL_REPORT.md`, `STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md`):
  - **Embedding Cosine Similarity**: **1.0000 average cosine similarity** between ChromaDB and pgvector across 100 sampled vectors.
  - **20-Query RAG Parity**: **20 / 20 (100.0%) Top-1 hotel match** between legacy CSV/ChromaDB and PostgreSQL/pgvector.
  - **Relational Integrity**: **1,661 hotels, 7,910 embedding chunks, 1,661 outbox domain events, 0 orphan records, 0 duplicate keys**.
  - **Master Test Suite**: **18 / 18 PASSED** in `tests/verification/test_stage24_5_complete_backend.py`. Total backend test suite reached 42/42 passed.

---

### 3.14 Stage 26: Repeatable Data Ingestion & Incremental Update Engine
- **Stage Name**: Stage 26 — Repeatable Data Ingestion Engine
- **Approximate Date**: Data Engineering Phase
- **Objective / Problem**: Eliminate manual SQL edits and full embedding recalculations by creating an auditable, multi-stage ingestion engine with SHA-256 field-level diffing.
- **Work Implemented**:
  - Established 9-stage lifecycle: `RAW -> NORMALIZED -> VALIDATED -> DEDUPLICATED -> CANONICAL -> DIFF -> DRY-RUN -> APPROVAL -> TRANSACTIONAL APPLY -> SELECTIVE VECTOR SYNC`.
  - Built `scripts/ingestion/diff_engine.py` using canonical content hashing (`calculate_canonical_content_hash`).
  - Built `scripts/ingestion/schema_contract.py` for strict schema validation.
  - Implemented Dry-Run safety (`pipeline.py dry-run` producing `dry_run.json`), requiring explicit `--run-id <RUN_ID>` approval before transactional apply.
  - Implemented `scripts/ingestion/selective_vector_sync.py` to recalculate embeddings *only* for modified content hashes.
- **Files Created**: `architecture_and_system_docs/data_pipeline/STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md`, `tests/ingestion/test_pipeline_stage26.py`.
- **Test Results**: **8 / 8 PASSED** in Stage 26 ingestion test suite. Zero production data mutated during dry-runs.

---

### 3.15 Stage 27: Full Pipeline Integration Audit & Gap Analysis
- **Stage Name**: Stage 27 — Orchestration Gap Analysis
- **Approximate Date**: Integration Audit Phase
- **Objective / Problem**: Audit upstream data processing scripts (collection, cleaning, NLP, ABSA, feature engineering, merging) to identify pipeline fragmentation.
- **Findings**: Upstream data engineering was executed via standalone, manually invoked scripts rather than a single unified CLI orchestrator.
- **Files Created**: `architecture_and_system_docs/stage27/STAGE27_ORCHESTRATION_GAP_ANALYSIS.md`, `STAGE27_FILE_EXECUTION_MATRIX.csv`.
- **Enablement**: Designed the blueprint for Stage 28 master orchestrator.

---

### 3.16 Stage 28: Master End-to-End Orchestration Engine + Approval Boundary
- **Stage Name**: Stage 28 — One-Command End-to-End Orchestration Engine
- **Approximate Date**: Orchestration Phase
- **Objective / Problem**: Provide a single CLI command to trigger all upstream processing, canonical dataset merging, validation, diffing, and PostgreSQL apply with approval protection.
- **Work Implemented**: Built `scripts/orchestrator.py` supporting `full`, `apply`, `status`, `dry-run` commands.
  - `python -m scripts.orchestrator full` sequentially executes: Source Acquisition $\rightarrow$ Cleaning $\rightarrow$ NLP Sentiment & ABSA $\rightarrow$ Feature Engineering $\rightarrow$ Canonical Dataset Merge (`final_hotel_dataset.csv`) $\rightarrow$ Stage 26 PostgreSQL Diff Engine (`dry_run.json`).
  - `full` is strictly read-only regarding PostgreSQL. Database mutation requires explicit human approval: `python -m scripts.orchestrator apply --run-id <RUN_ID>`.
- **Files Created**: `scripts/orchestrator.py`, `architecture_and_system_docs/stage28/STAGE28_FINAL_REPORT.md`, `tests/orchestration/test_stage28_orchestrator.py`.
- **Test Results**: **6 / 6 PASSED** in Stage 28 test suite.

---

### 3.17 Stage 29: Live Operational Visibility & Terminal Progress Engine
- **Stage Name**: Stage 29 — Live Terminal Progress & Manual Execution
- **Approximate Date**: Final Operational Phase
- **Objective / Problem**: Provide real-time operational feedback during long-running pipeline executions and ensure graceful signal handling.
- **Work Implemented**:
  - Developed `scripts/orchestration/progress.py` (`ProgressTracker`). Renders an ASCII terminal progress dashboard showing active stage, script, record percentage, elapsed time, ETA calculations, and structured file logging (`data/runs/<RUN_ID>/pipeline.log`).
  - Implemented `SIGINT` (Ctrl+C) signal handler: safely terminates sub-processes, marks `pipeline_manifest.json` as `INTERRUPTED`, and guarantees zero database mutation.
  - Enhanced `orchestrator status` CLI command to report live PostgreSQL row counts (1,661 hotels, 7,910 vector embeddings) and run history.
- **Files Created**: `scripts/orchestration/progress.py`, `architecture_and_system_docs/stage29/STAGE29_LIVE_PROGRESS_REPORT.md`, `tests/orchestration/test_stage29_progress.py`.
- **Test Results**: **4 / 4 PASSED** in Stage 29 progress test suite.
- **Total Backend Verification**: **50 / 50 PASSED** across the complete backend test suite.

---

## 4. Dataset Development History & Transformation Tracking

The table below documents the complete transformation lineage of the TrustLayer-AI dataset from raw API acquisition to runtime PostgreSQL storage:

| Pipeline Transition Stage | Input Record Count | Output Record Count | Filtered / Removed Records | Transformed & Generated Fields | Model / Algorithm Applied | Validation & Integrity Checks | Final Artifact Produced |
|---|---:|---:|---|---|---|---|---|
| **Raw Collection** | 0 | 1,661 hotels; ~8,305 reviews | API quota caps | `place_id`, `name`, `formatted_address`, `lat`, `lng`, `rating`, `user_ratings_total`, `raw_reviews` | Google Places API Text Search & Place Details REST API | Checked HTTP 200 status; flagged 100% missing `price_level` | `delhi_hotels_raw.csv`, `reviews_raw.csv` |
| **Data Cleaning** | 1,661 hotels | 1,661 hotels; 1,618 hotels with reviews | 0 hotels removed; 43 hotels flagged with 0 reviews | Standardized text, trimmed whitespace, validated coordinate bounds | Regex string normalization; Delhi NCR spatial bounding box | Verified 0 nulls in critical columns; coordinate bounding box check | `delhi_hotels_cleaned.csv`, `reviews_cleaned.csv` |
| **NLP Sentiment Extraction** | 1,618 review sets | 1,618 review feature sets | 43 zero-review hotels bypassed | `sentiment_positive_prob`, `sentiment_negative_prob`, `sentiment_label` | DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`) | Pearson correlation ($r \approx 0.84$) against user star ratings | `review_features.csv` |
| **ABSA Feature Extraction** | 1,618 review feature sets | 1,618 aspect feature sets | N/A | `cleanliness_score`, `service_score`, `location_score`, `value_score`, `staff_score` | Aspect keyword masking + DistilBERT sentiment masking | Verified aspect score distributions; Cleanliness identified as highest variance | `explainability_features.csv` |
| **Feature Engineering & Merge** | 1,661 hotels | 1,661 hotels (26 columns) | 0 | `trust_score` (0-100), `popularity_score` (0-1), `budget_category` (Proxy), median aspect imputations | `MinMaxScaler`, area-cluster median imputation | Checked Trust Score Gaussian distribution (mean 0.68) and Trust vs Popularity correlation ($r \approx 0.05$) | `final_hotel_dataset.csv` (SHA-256: `eca959c788...`) |
| **Synthetic User & Interaction V2** | 500 users | 5,000 interactions | Replaced V1 random interactions | `user_id`, `hotel_id`, `interaction_type`, `implicit_weight`, `timestamp` | Power-law interaction sampling; demographic preference matching | Verified budget match rate (66%), area match rate (51%), NDCG@10 > 0.12 | `users.csv`, `interactions_v2.csv` |
| **Review Segmentation & RAG Chunking** | 1,661 hotels | 7,910 text chunks | 0 | `chunk_id`, `hotel_id`, `content`, `metadata` | Text chunking window (200 tokens) | Checked 100% hotel coverage (1,661 hotels in chunks) | `data/rag/ChIJ*.json` |
| **pgvector Backfill** | 7,910 JSON chunks | 7,910 database rows | 0 | `id`, `hotel_id`, `content`, `embedding` (VECTOR(384)), `metadata`, `content_hash` | SentenceTransformers `all-MiniLM-L6-v2` | Verified 1.0000 average cosine similarity with ChromaDB; 0 orphan vectors | PostgreSQL `embedding_documents` table |

---

## 5. Jupyter Research Notebooks Inventory & Analytical Findings

The **Stage 11.75 Research Visualization Notebook Suite** (`research/notebooks/`) provided essential exploratory data analysis and diagnostic evidence throughout development:

### 5.1 Notebook Breakdown
1. **`01_hotel_metadata_analysis.ipynb`**:
   - *Dataset Used*: `delhi_hotels_raw.csv`, `delhi_hotels_cleaned.csv`
   - *Analysis*: Spatial density distribution, missing value auditing, area cluster counts.
   - *Key Findings*: Proved `price_level` was 100% missing (NaN). Mapped spatial clustering heavily around central New Delhi (Paharganj/Karol Bagh, 216 hotels), Indira Gandhi International Airport corridor (Mahipalpur, 56 hotels), and Gurugram (39 hotels).
2. **`02_review_analysis.ipynb`**:
   - *Dataset Used*: `reviews_cleaned.csv`
   - *Analysis*: Review length distribution, rating positivity skew.
   - *Key Findings*: Identified extreme positivity skew (median rating 4.10, 5-star concentration). Highlighted the 5-review API detail request cap constraint.
3. **`03_sentiment_analysis.ipynb`**:
   - *Dataset Used*: `review_features.csv`
   - *Analysis*: DistilBERT sentiment probability vs star rating correlation.
   - *Key Findings*: Pearson correlation coefficient of **$r \approx 0.84$** between sentiment probabilities and star ratings, validating NLP extraction quality.
4. **`04_absa_explainability_analysis.ipynb`**:
   - *Dataset Used*: `explainability_features.csv`
   - *Analysis*: Aspect score distributions across Cleanliness, Service, Location, Value, and Staff Behavior.
   - *Key Findings*: **Cleanliness** exhibited the highest score variance, establishing it as the primary aspect differentiator among Delhi hotels.
5. **`05_feature_engineering_analysis.ipynb`**:
   - *Dataset Used*: `hotel_features.csv`
   - *Analysis*: Statistical distributions of engineered Trust Score and Popularity Score; MinMaxScaler normalization checks.
   - *Key Findings*: Trust Score followed a normal distribution centered at 0.68; Popularity Score followed a power-law distribution. Low correlation between Trust and Popularity ($r \approx 0.05$) confirmed independent evaluation signals.
6. **`06_user_dataset_analysis.ipynb`**:
   - *Dataset Used*: `users.csv`
   - *Analysis*: Synthetic user preference vectors (budget, preferred area, aspect priorities).
   - *Key Findings*: Verified even demographic representation across 500 synthetic user profiles.
7. **`07_interaction_analysis.ipynb`**:
   - *Dataset Used*: `interactions.csv`, `interactions_v2.csv`
   - *Analysis*: Interaction matrix sparsity, user-item overlap, power-law activity distribution.
   - *Key Findings*: Exposed 99.27% matrix sparsity in initial V1 interactions; validated controlled preference injection in V2 interactions.
8. **`08_final_dataset_overview.ipynb`**:
   - *Dataset Used*: `final_hotel_dataset.csv`
   - *Analysis*: Master dataset feature correlation heatmap and missingness report across all 26 columns.
   - *Key Findings*: Confirmed zero missing values post-median aspect imputation across all 1,661 canonical hotels.
9. **`09_recommender_diagnostics.ipynb`**:
   - *Dataset Used*: Model evaluation logs
   - *Analysis*: Forensic diagnostic investigation of Stage A recommender failure.
   - *Key Findings*: Empirically proved SVD matrix factorization failure (Precision@10 0.002, NDCG@10 0.006) caused by unweighted synthetic interaction noise and CF score dominance ($\alpha=1.0$).
10. **`10_interaction_quality_audit.ipynb`**:
    - *Dataset Used*: `interactions_v2.csv`
    - *Analysis*: Post-remediation interaction quality audit.
    - *Key Findings*: Confirmed successful preference signal injection (66% budget match, 51% area match), restoring hybrid recommender NDCG@10 to > 0.12.

---

## 6. Architectural Evolution

The architecture of TrustLayer-AI evolved through 4 distinct phases:

### Phase 1: CSV & In-Memory Script Architecture (Stages 1–7)
- **BEFORE**: Standalone Python scripts reading directly from local CSV files (`final_hotel_dataset.csv`, `interactions.csv`) loaded into pandas DataFrames in memory.
- **PROBLEM**: Inability to handle concurrent requests, lack of ACID transactions, high memory overhead, non-standardized API contracts, and uncoordinated model execution.
- **CHANGE**: Introduced FastAPI REST framework, standard domain DTOs, and preliminary service classes (`RecommendationService`, `HotelService`).
- **AFTER**: Web client accessibility established, but underlying data access remained tightly coupled to raw file paths.

### Phase 2: File-Based Vector Store & Clean Repository Abstraction (Stage C & Stage 23)
- **BEFORE**: Direct pandas CSV access and raw ChromaDB file operations embedded directly inside FastAPI route handlers.
- **PROBLEM**: Tight coupling between presentation layer and storage engines; inability to swap storage backends without modifying API code.
- **CHANGE**: Implemented Clean Architecture Repository Pattern (`BaseHotelRepository`, `BaseTraceRepository`, `BaseEmbeddingRepository`) with file adapters (`CsvHotelRepository`, `ChromaEmbeddingRepository`).
- **AFTER**: Complete decoupling of business logic from file storage; API routes calling abstract repository interfaces.

### Phase 3: PostgreSQL 17 & pgvector Unified Database Engine (Stage 24)
- **BEFORE**: Dual storage engine setup (CSV for relational metadata + ChromaDB file store for vector embeddings).
- **PROBLEM**: Risk of data drift between CSV and vector files; lack of transactional atomicity across relational metadata and vector updates; lack of outbox event logging.
- **CHANGE**: Deployed PostgreSQL 17.6 database engine (`trustlayer_db`) with `pgvector` extension. Migrated all 1,661 hotels and 7,910 vector chunks into PostgreSQL tables (`hotels`, `embedding_documents`). Implemented `PostgresHotelRepository` and `PgVectorEmbeddingRepository`.
- **AFTER**: Unified relational and vector ACID transactions, zero orphan records, 100% data access provenance verified, and legacy CSV/ChromaDB files completely detached.

### Phase 4: Master Orchestration Engine & Live Terminal Progress (Stages 26–29)
- **BEFORE**: Upstream data engineering (collection, cleaning, NLP, feature engineering) executed via disconnected standalone scripts; manual database updates.
- **PROBLEM**: Operational fragmentation, risk of unvalidated database overwrites, lack of dry-run safety, and zero terminal visibility during pipeline runs.
- **CHANGE**: Built Stage 26 repeatable ingestion engine (SHA-256 diffing, dry-run safety, approval gates), Stage 28 master orchestrator CLI (`scripts/orchestrator.py`), and Stage 29 live terminal progress dashboard (`ProgressTracker` with Ctrl+C signal safety).
- **AFTER**: Single-command repeatable pipeline (`python -m scripts.orchestrator full`), strict human approval gate before database mutation, and real-time operational progress tracking.

---

## 7. RAG Development Chronology

The Retrieval-Augmented Generation (RAG) architecture developed in strict chronological iterations:

```text
RAG COMPONENT EVOLUTION:
  Raw Reviews (Stage 1)
     │
     ▼
  Segmentation into 7,910 Chunks (Stage C.1)
     │
     ▼
  ChromaDB Vector Store (Stage C.3)  ──►  Migrated to pgvector (Stage 24.2)
     │
     ▼
  Hybrid Retrieval Engine (Stage C.4): Semantic Vector Search + Metadata Filters + Recommender Reranking
     │
     ▼
  ContextCompressor (Stage G): Deduplication & 1,500-Token Budget Enforcement
     │
     ▼
  PromptOrchestrator (Stage G): Task Grounding & [Chunk ID: XYZ] Formatting
     │
     ▼
  Ollama Local LLM Generation (Stage D)
     │
     ▼
  CitationInjector (Stage G): Structured ProvenanceChunk Mapping
     │
     ▼
  GroundingValidator (Stage D): Hallucination Interception & Stripping
```

### Chronological Component Breakdown:
1. **Query Parsing & Constraint Extraction (`app/services/query_parser.py`)**: Extracted structured intent, budget constraints, preferred areas, and aspect priorities from natural language user queries.
2. **Hybrid Retrieval (`app/services/retriever.py`)**: Combined vector cosine similarity search over `embedding_documents` with hard SQL metadata filtering (area, budget) and recommender trust score reranking.
3. **Context Compression (`app/services/context_compressor.py`)**: Deduplicated overlapping review chunks and enforced a strict 1,500-token context budget, prepending explicit `[Chunk ID: XYZ]` markers.
4. **Prompt Orchestration (`app/services/prompt_orchestrator.py`)**: Wrapped compressed context in task-specific system prompts containing mandatory grounding rules and citation instructions.
5. **LLM Generation (`app/services/llm_service.py`)**: Executed local Ollama inference (`mistral` / `llama3`) supporting both synchronous generation and HTTP chunked streaming (`async stream_generate`).
6. **Citation Injection (`app/services/citation_injector.py`)**: Post-processed raw LLM response text, parsing inline chunk citations into structured JSON arrays of `ProvenanceChunk` objects for lazy-loading in the frontend Provenance Drawer.
7. **Grounding & Hallucination Protection (`app/services/grounding_validator.py`)**: Cross-referenced generated LLM claims against retrieved chunk text. Intercepted and re-prompted responses claiming unverified amenities (active interception rate 1.3%, grounded response rate 96.7%).

---

## 8. Recommender & Explainability Development Chronology

### 8.1 Model Architecture Evolution
1. **Baseline Model**: Popularity baseline ranking hotels purely by review count and average rating.
2. **Content-Based Filtering (CB)**: Cosine similarity between user preference vectors and hotel feature vectors (aspect scores, budget category, area).
3. **Collaborative Filtering (CF)**: Matrix Factorization using SVD (Surprise library) over user-item interaction matrices.
4. **Initial Hybrid (Linear Score Blending - Flawed)**: Attempted linear score blending $\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$. Failed due to score scale mismatch (cosine similarities 0.8–0.9 vs predicted ratings 1.0–5.0), resulting in grid search choosing $\alpha=1.0$ (100% CF collapse).
5. **Remediated Hybrid (Reciprocal Rank Fusion - Active)**: Replaced linear score blending with Reciprocal Rank Fusion (RRF, $k=60$). Combined ordinal rank positions from CB and CF models, eliminating score calibration mismatches and achieving **NDCG@10 > 0.12**.

### 8.2 Explainability Evolution
- **Initial Plan (SHAP)**: Attempted SHAP value computation for SVD and tree-based models. Abandoned due to high computational latency (seconds per request) and unreadable feature importance values for end users.
- **Analytical Feature-Matching Explainer (`scripts/explainability/explainer.py`)**: Implemented direct analytical comparison between user preference constraints and hotel aspect scores. Generated quantitative aspect alignment breakdown bars and qualitative explanation badges (e.g., *"Top Cleanliness Match in Mahipalpur"*).

---

## 9. Database, Data Pipeline & Ingestion Engine Evolution

### 9.1 Database Technology Timeline
1. **CSV Data Store (Stages 1–22)**: `final_hotel_dataset.csv` loaded into memory via pandas.
2. **SQLite Disposable Store (Stage 24.1)**: `bootstrap_stage24.db` used for initial SQL schema testing. Lacked vector extension support.
3. **PostgreSQL 17.6 + pgvector (Stage 24.4 → Present)**: Production `trustlayer_db` running on PostgreSQL 17.6 with `pgvector` extension.

### 9.2 Complete Relational Schema Specification

```sql
-- Core Hotel Entity Table
CREATE TABLE hotels (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    area VARCHAR(255),
    city VARCHAR(255),
    destination VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    price_level DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    user_ratings_total INTEGER,
    budget_category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Child Relational Tables
CREATE TABLE hotel_locations (
    hotel_id VARCHAR(255) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    area VARCHAR(255),
    city VARCHAR(255)
);

CREATE TABLE hotel_scores (
    hotel_id VARCHAR(255) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    trust_score DOUBLE PRECISION,
    popularity_score DOUBLE PRECISION,
    cleanliness_score DOUBLE PRECISION,
    service_score DOUBLE PRECISION,
    location_score DOUBLE PRECISION,
    value_score DOUBLE PRECISION,
    staff_score DOUBLE PRECISION
);

CREATE TABLE hotel_sources (
    hotel_id VARCHAR(255) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    google_place_id VARCHAR(255),
    source_name VARCHAR(100),
    raw_data_url TEXT
);

CREATE TABLE hotel_amenities (
    hotel_id VARCHAR(255) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    wifi BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    pool BOOLEAN DEFAULT FALSE,
    restaurant BOOLEAN DEFAULT FALSE,
    ac BOOLEAN DEFAULT FALSE,
    bar BOOLEAN DEFAULT FALSE,
    gym BOOLEAN DEFAULT FALSE,
    spa BOOLEAN DEFAULT FALSE
);

-- pgvector Vector Storage Table
CREATE TABLE embedding_documents (
    id VARCHAR(255) PRIMARY KEY, -- chunk_id
    hotel_id VARCHAR(255) REFERENCES hotels(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(384),
    metadata JSONB,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Domain Event Outbox Table
CREATE TABLE domain_events (
    id VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ingestion Tracking Tables
CREATE TABLE ingestion_runs (
    run_id VARCHAR(100) PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    total_processed INTEGER DEFAULT 0,
    total_inserted INTEGER DEFAULT 0,
    total_updated INTEGER DEFAULT 0
);

CREATE TABLE ingestion_records (
    id VARCHAR(255) PRIMARY KEY,
    run_id VARCHAR(100) REFERENCES ingestion_runs(run_id) ON DELETE CASCADE,
    hotel_id VARCHAR(255) REFERENCES hotels(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL
);
```

### 9.3 Ingestion Pipeline Lifecycle (Stage 26)
Stage 26 established the repeatable 9-stage data ingestion lifecycle:
1. `RAW`: Ingest source CSV data into temporary staging structure.
2. `NORMALIZED`: Standardize string formats, null values, and coordinate bounds.
3. `VALIDATED`: Enforce `schema_contract.py` rules (rating bounds `[0..5]`, trust score `[0..100]`, non-null keys).
4. `DEDUPLICATED`: Eliminate duplicate hotel entities by `hotel_id` and canonical hash.
5. `CANONICAL`: Write output to `data/exports/final_hotel_dataset.csv`.
6. `DIFF`: Execute `diff_engine.py` comparing incoming SHA-256 canonical hashes against existing PostgreSQL records.
7. `DRY-RUN`: Generate `dry_run.json` diff report under `data/runs/<RUN_ID>/` with zero database mutation.
8. `APPROVAL`: Require human operator verification of `RUN_ID`.
9. `TRANSACTIONAL APPLY & SELECTIVE VECTOR SYNC`: Open SQL transaction, execute insert/update operations, log domain outbox events, and invoke `selective_vector_sync.py` to recompute embeddings *only* for modified content hashes.

---

## 10. Stage 28 and Stage 29 Orchestration Evolution

Stage 28 and Stage 29 represent the culmination of the data engineering architecture:

### Stage 28: Master One-Command Orchestrator
- **Problem**: Prior to Stage 28, executing a full data update required manually finding and running 6 separate scripts across `scripts/collection/`, `scripts/cleaning/`, `scripts/nlp/`, and `scripts/recommender/`.
- **Solution**: Created `scripts/orchestrator.py` as a single unified CLI runner.
- **Workflow**:
  - `python -m scripts.orchestrator full`: Automated sequential execution of Source Acquisition $\rightarrow$ Cleaning $\rightarrow$ NLP Sentiment & ABSA $\rightarrow$ Feature Engineering $\rightarrow$ Canonical Merge $\rightarrow$ Stage 26 Diff Engine.
  - Strict read-only safety: `full` creates local files and dry-run diff artifacts under `data/runs/<RUN_ID>/` but guarantees **ZERO PostgreSQL mutation**.
  - `python -m scripts.orchestrator apply --run-id <RUN_ID>`: Enforces strict human approval gate before executing database transactions.

### Stage 29: Live Operational Visibility & Signal Protection
- **Problem**: Pipeline executions lacked live progress feedback, making long-running NLP and vector sync tasks appear frozen. Aborting via Ctrl+C risked leaving open database connections or corrupted state.
- **Solution**: Built `scripts/orchestration/progress.py` (`ProgressTracker`).
- **Workflow**:
  - Renders an interactive ASCII terminal progress dashboard showing active stage name, script file, record progress percentage bar, elapsed execution time, and ETA calculation.
  - Generates structured file logs at `data/runs/<RUN_ID>/pipeline.log`.
  - Implements a `SIGINT` (Ctrl+C) signal handler that catches interrupt signals, terminates child sub-processes cleanly, marks `pipeline_manifest.json` as `INTERRUPTED`, and guarantees **ZERO database mutation**.

---

## 11. Testing & Verification History

The table below documents the historical progression of testing suites across development stages:

| Stage ID | Test Suite Name | Target Module / Component | Test Count | Result | Key Verified Behaviours |
|---|---|---|---:|---|---|
| **Stage 6 / A** | `evaluate_recommenders.py` | Initial Recommenders (SVD, CB, Hybrid) | 4 | **FAILED** | Uncovered Precision@10 (0.002) and CF collapse ($\alpha=1.0$) |
| **Stage 6.1 / A.1** | `test_remediations.py` | Remediated Recommenders (RRF, V2 Data) | 6 | **PASS** | Verified RRF rank fusion and NDCG@10 > 0.12 |
| **Stage 7.1 / B.1** | `audit_explainability_b1.py` | Explainer Engine | 5 | **PASS** | Audited feature alignment and explanation text output |
| **Stage C.4** | `evaluate_retrieval.py` | Vector Retriever & Ablation | 14 | **PASS** | Verified Precision@5 (0.81), Recall@5 (0.79), MRR (0.83) |
| **Stage D** | `evaluate_stage_d.py` | LLM Generation & Grounding | 6 | **PASS** | Verified Grounded Rate (96.7%) and Hallucination Rate (1.3%) |
| **Stage E** | `test_api_endpoints.py` | FastAPI REST Endpoints | 8 | **PASS** | Verified 200 OK responses and non-mock payload mapping |
| **Stage 23.1** | `audit_stage23_1.py` | Abstract Repository Layer | 12 | **PASS** | Read-only verification of CSV, ChromaDB, and JSON trace access |
| **Stage 24.1** | `audit_stage24_1.py` | SQLite Relational Baseline | 10 | **PASS** | Verified relational table structures and orphan checks |
| **Stage 24.2** | `test_realtime_isolated.py` | pgvector Vector Parity | 8 | **PASS** | Verified 1.0000 cosine similarity and 20-query top-1 parity |
| **Stage 24.5** | `test_stage24_5_complete_backend.py` | Complete Backend Provenance | 18 | **PASS** | Verified live PostgreSQL 17 runtime, 0 orphans, legacy detachment |
| **Stage 26** | `test_pipeline_stage26.py` | Repeatable Ingestion Engine | 8 | **PASS** | Verified SHA-256 diffing, dry-run safety, approval gate |
| **Stage 28** | `test_stage28_orchestrator.py` | Master One-Command Orchestrator | 6 | **PASS** | Verified CLI commands (`full`, `apply`, `status`, dry-run) |
| **Stage 29** | `test_stage29_progress.py` | Live Terminal Progress Engine | 4 | **PASS** | Verified progress rendering, logging, and SIGINT interrupt safety |
| **FINAL** | **Complete Backend Test Suite** | **Entire System** | **50** | **PASS (50/50)** | **100% Repository Verification Passed** |

---

## 12. Security, Safety & Reliability Evolution

Safety and reliability mechanisms were introduced progressively to ensure enterprise-grade stability:

1. **API Key Protection**: Centralized environment variable loading via `pydantic-settings` (`app/config/config.py`). Prevented API key exposure in codebase. Graceful API fallback if `GOOGLE_PLACES_API_KEY` is missing.
2. **Schema Contracts (`scripts/ingestion/schema_contract.py`)**: Enforced strict runtime data type checking, rating bounds `[0.0..5.0]`, trust score bounds `[0.0..100.0]`, and lat/long coordinate validation.
3. **SHA-256 Canonical Hashing (`diff_engine.py`)**: Implemented content-hash comparison (`calculate_canonical_content_hash`) to detect exact field changes and eliminate redundant database writes and embedding updates.
4. **Dry-Run Safety**: Executing `orchestrator full` or `pipeline.py dry-run` writes diff artifacts to `data/runs/<RUN_ID>/` without modifying PostgreSQL.
5. **Human-in-the-Loop Approval Gate**: Database mutation requires explicit approval specifying `--run-id <RUN_ID>`. Stale or invalid RUN_IDs are rejected.
6. **Transactional Apply**: All database writes execute inside SQLAlchemy explicit transactional blocks (`session.begin()`), rolling back completely on error.
7. **Selective Vector Synchronization**: Recalculates embeddings ONLY for modified content hashes, preserving vector database stability.
8. **Grounding & Hallucination Protection**: `GroundingValidator` intercepts and strips generated LLM text containing ungrounded amenity claims.
9. **Graceful Signal Handling (`SIGINT`)**: Stage 29 progress engine handles Ctrl+C cleanly, terminating child processes and preventing database corruption.

---

## 13. Historical Anomalies, Failures & Abandoned Approaches

To preserve complete engineering truth, the following pivot points and failure modes are explicitly documented:

1. **Missing Google Places Price Data**: Google Places API returned `price_level` as 100% NaN for all 1,661 hotels in India. Handled by engineering a `budget_category` proxy based on location and rating metrics.
2. **5-Review API Acquisition Limit**: Google Places Detail API caps returned user reviews at 5 per place request. Handled by chunking existing reviews effectively and relying on sentiment density.
3. **Synthetic Interaction Noise & SVD Collapse (Stage A)**: Initial synthetic interaction generator (`generate_interactions.py`) assigned user interactions with excess randomness. Resulted in 99.27% matrix sparsity, forcing SVD to underfit (Precision@10 = 0.002, NDCG@10 = 0.006) and causing the linear hybrid model grid search to select $\alpha=1.0$ (100% CF collapse). Remediated in Stage A.1 using V2 controlled preference interactions and Reciprocal Rank Fusion (RRF).
4. **Hardcoded Evaluation Narrative Bug**: Early `evaluate_recommenders.py` script printed hardcoded narrative text claiming Content-Based filtering outperformed Collaborative Filtering on cold-start users. Forensic audit proved cold-start user count was exactly 0 due to fixed 10-interaction user splits. Script was rewritten to compute metrics dynamically.
5. **Abandoned SHAP Explainability**: Attempted SHAP value approximations for model explainability. Abandoned due to extreme latency (seconds per request) and unreadable user outputs. Replaced with an analytical feature-matching explainer.
6. **Legacy Database & Vector Store Detachment**: Switched backend database from CSV files and ChromaDB file vector store to PostgreSQL 17.6 + `pgvector`. Validated complete detachment of legacy files in Stage 24.5.

---

## 14. Forensic Contradiction Resolution Matrix

| Discrepancy / Claim A | Discrepancy / Claim B | Source A | Source B | Forensic Explanation & Ground Truth | Final Verified State | Confidence Level |
|---|---|---|---|---|---|---|
| Hotel Count = 1,379 | Hotel Count = 1,661 | Stage A Recommender Report | Canonical Dataset & PostgreSQL | Stage A filtered out 282 hotels lacking review interactions. PostgreSQL retains all 1,661 canonical hotels with median aspect imputation. | **1,661 Canonical Hotels** in PostgreSQL `hotels` table | High (Empirical SQL Count) |
| Cold-Start CB Outperforms CF | 0 Cold-Start Users Exist in Test Set | `evaluate_recommenders.py` Narrative Output | Diagnostic Audit (`recommender_diagnostics.md`) | The evaluation script contained hardcoded narrative text printed regardless of output. Fixed 70/30 chronological splitting over 10-interaction profiles left 0 cold-start users. | **Dynamic Evaluation Engine** built in Stage A.1 over V2 power-law interaction distribution | High (Code Audit) |
| Hybrid Model = $\alpha \cdot \text{CF} + (1-\alpha) \cdot \text{CB}$ | Hybrid Model = 100% CF ($\alpha=1.0$) | Initial Architecture Spec | Grid Search Optimization Results | Linear score blending failed due to score scale mismatch (cosine sim 0.8–0.9 vs ratings 1.0–5.0). Grid search chose $\alpha=1.0$. Switched to RRF. | **Reciprocal Rank Fusion (RRF)** ($k=60$) | High (Source Code & Audit) |
| Vector Store = ChromaDB | Vector Store = pgvector | Stage C Docs & `data/vector_store/` | Stage 24.2+ Architecture Docs & SQL Schema | ChromaDB was used during early RAG development. Stage 24.2 backfilled all 7,910 chunks to PostgreSQL `pgvector`. | **PostgreSQL pgvector** (`embedding_documents` table) | High (Database Provenance) |
| Multi-Script Execution Required | One-Command Pipeline Execution | Upstream Data Scripts (`scripts/nlp/`, etc.) | Stage 28 Orchestration Engine (`orchestrator.py`) | Stage 27 identified script fragmentation. Stage 28 unified all 6 upstream stages into a single CLI orchestrator. | **`python -m scripts.orchestrator full`** | High (CLI Verification) |

---

## 15. Master Project Development Timeline

| Chronological Order | Stage Identifier | Verified Date Range | Major Architectural / Engineering Change | Key Outcome / Benchmark Result |
|---|---|---|---|---|
| **1** | Stage 1 | Initial Phase | Google Places & Reviews API Data Collection | 1,661 raw hotels and ~8,305 raw text reviews acquired |
| **2** | Stage 2 | Pre-Processing Phase | Data Cleaning, Regex Normalization & Bounding Box Filtering | Cleaned metadata (`delhi_hotels_cleaned.csv`); zero nulls in core fields |
| **3** | Stage 3 | NLP Research Phase | DistilBERT Sentiment Extraction & ABSA Aspect Masking | Sentiment probabilities ($r \approx 0.84$ with ratings); 5 aspect scores extracted |
| **4** | Stage 4 | Feature Phase | Trust Score Engineering & Canonical Dataset Consolidation | Generated `final_hotel_dataset.csv` (1,661 hotels, 26 features, Trust mean 0.68) |
| **5** | Stage 5 | Simulation Phase | Synthetic User Profile & Interaction V1 Generation | 500 synthetic user profiles; initial interaction matrix created |
| **6** | Stage 6 / Stage A | Model Phase | Recommender Modeling & Diagnostic Failure Audit | Identified SVD failure (NDCG@10 0.006) and CF collapse ($\alpha=1.0$). Triggered NO-GO |
| **7** | Stage 6.1 / Stage A.1 | Remediation Phase | V2 Preference Interactions & Reciprocal Rank Fusion | NDCG@10 improved to > 0.12; linear score blending replaced with RRF ($k=60$) |
| **8** | Stage 7 / Stage B | Explainability Phase | Analytical Aspect-Matching Explainer Engine | Built `explainer.py`; replaced SHAP with real-time analytical explanations |
| **9** | Stage C | RAG Phase | Review Segmentation, ChromaDB Vector Store & Hybrid Retrieval | 7,910 review chunks; Hybrid Retrieval P@5 = 0.81, R@5 = 0.79, MRR = 0.83, NDCG@5 = 0.85 |
| **10** | Stage D / Stage G | LLM & Grounding Phase | Ollama LLM Generation, Prompt Orchestration & Grounding Validator | Grounded Response Rate 96.7%, Hallucination Rate 1.3%, 3 active interceptions |
| **11** | Stage E / Stage F | UI & System Phase | FastAPI REST Integration & React TypeScript Frontend | Versioned `/api/v1/` routes; TanStack Query integration; audit mocks removed |
| **12** | Stage 23 / 23.1 | Abstraction Phase | Clean Architecture Repository Pattern | Defined base repository contracts (`BaseHotelRepository`, `BaseEmbeddingRepository`) |
| **13** | Stage 24 / 24.1–24.5 | Database Phase | Real PostgreSQL 17.6 + pgvector Infrastructure Migration | Migrated 1,661 hotels & 7,910 vector chunks to PostgreSQL; 18/18 provenance tests passed |
| **14** | Stage 26 | Data Engine Phase | Repeatable Ingestion Engine & SHA-256 Field Diffing | 9-stage ingestion lifecycle; dry-run safety; selective vector sync; 8/8 tests passed |
| **15** | Stage 27 | Integration Audit | Upstream Data Pipeline Integration Audit | Mapped file execution matrix; identified script fragmentation |
| **16** | Stage 28 | Orchestration Phase | Master One-Command CLI Orchestrator Engine | Built `scripts/orchestrator.py`; unified all upstream stages; 6/6 tests passed |
| **17** | Stage 29 | Visibility Phase | Live Terminal Progress Engine & SIGINT Interrupt Safety | Built `ProgressTracker` ASCII dashboard & Ctrl+C safety; 50/50 backend tests passed |

---

## 16. Summary Timelines

### 16.1 Data Evolution Summary Timeline

| Stage | Input State | Processing Action | Output State | Record Volume | Key Transformation |
|---|---|---|---|---:|---|
| **Stage 1** | External API | REST API fetching | Raw CSVs | 1,661 hotels | Google Places Places & Details API extraction |
| **Stage 2** | Raw CSVs | Regex cleaning & spatial filter | Cleaned CSVs | 1,661 hotels | Standardized text; filtered out-of-bounds coordinates |
| **Stage 3** | Cleaned Reviews | DistilBERT NLP & ABSA | Feature CSVs | 1,618 review sets | Computed sentiment probabilities & 5 aspect scores |
| **Stage 4** | Feature CSVs | Score calculation & merge | Canonical CSV | 1,661 hotels | Trust Score (mean 0.68); area-cluster median imputation |
| **Stage 5 / 6.1** | Demographic Config | Synthetic sampling V2 | Interaction CSV | 5,000 interactions | Injected preference matching (66% budget, 51% area) |
| **Stage C** | Cleaned Reviews | Text chunking (200 tokens) | JSON Chunks | 7,910 text chunks | Segmented review text for vector embeddings |
| **Stage 24.2** | JSON Chunks | SentenceTransformer embedding | pgvector DB | 7,910 vector rows | 384-dimensional `all-MiniLM-L6-v2` vector backfill |
| **Stage 26/28** | Canonical CSV | SHA-256 diff & SQL apply | PostgreSQL DB | 1,661 DB rows | Transactional relational apply & selective vector sync |

### 16.2 Architecture Evolution Summary Timeline

| Architecture Phase | Core Technology | Primary Data Storage | Reason for Transition | Key Architectural Benefit |
|---|---|---|---|---|
| **Phase 1: CSV Scripts** | Python, pandas, Streamlit | Raw CSV Files | Initial rapid prototyping | Fast initial exploratory data analysis |
| **Phase 2: Repository Abstraction** | FastAPI, ChromaDB, pandas | CSV + ChromaDB File Store | Decouple storage from presentation | Abstract repository contracts (`BaseHotelRepository`) |
| **Phase 3: PostgreSQL Migration** | PostgreSQL 17.6, pgvector, SQLAlchemy | PostgreSQL `trustlayer_db` | Need unified relational & vector ACID transactions | Zero orphan records; 1.0000 vector parity; transactional outbox |
| **Phase 4: Master Orchestration** | Typer/CLI, ProgressTracker, Pytest | Real PostgreSQL + Local Runs | Automate pipeline & ensure operational safety | One-command pipeline (`full`), dry-run safety, Ctrl+C protection |

### 16.3 Testing Evolution Summary Timeline

| Stage | Target Test Suite | Test Count | Result | Core Behavior Verified |
|---|---|---:|---|---|
| **Stage A** | `evaluate_recommenders.py` | 4 | **FAILED** | Uncovered SVD failure (NDCG 0.006) & CF collapse ($\alpha=1.0$) |
| **Stage A.1** | `test_remediations.py` | 6 | **PASS** | Verified RRF rank fusion and NDCG@10 > 0.12 |
| **Stage B.1** | `audit_explainability_b1.py` | 5 | **PASS** | Audited feature alignment and explanation text output |
| **Stage C.4** | `evaluate_retrieval.py` | 14 | **PASS** | Verified Precision@5 (0.81), Recall@5 (0.79), MRR (0.83) |
| **Stage D** | `evaluate_stage_d.py` | 6 | **PASS** | Verified Grounded Rate (96.7%) and Hallucination Rate (1.3%) |
| **Stage 23.1** | `audit_stage23_1.py` | 12 | **PASS** | Read-only verification of abstract repositories |
| **Stage 24.5** | `test_stage24_5_complete_backend.py` | 18 | **PASS** | Provenance audit: live PostgreSQL 17, 0 orphans, legacy detachment |
| **Stage 26** | `test_pipeline_stage26.py` | 8 | **PASS** | Verified 9-stage ingestion lifecycle, SHA-256 diff, dry-run safety |
| **Stage 28** | `test_stage28_orchestrator.py` | 6 | **PASS** | Verified one-command CLI orchestrator (`full`, `apply`, `status`) |
| **Stage 29** | `test_stage29_progress.py` | 4 | **PASS** | Verified progress rendering, logging, and SIGINT interrupt safety |
| **FINAL** | **Master Backend Test Suite** | **50** | **PASS** | **100% Repository Verification Passed across all 50 tests** |

---

## 17. Final Verified System State

The current, empirical production state of TrustLayer-AI is documented below:

- **Backend Architecture**: FastAPI REST framework (`app/`) with versioned `/api/v1/` routes and Clean Architecture Repository Pattern (`PostgresHotelRepository`, `PgVectorEmbeddingRepository`).
- **Database Engine**: **REAL PostgreSQL 17.6 engine** (`trustlayer_db` on `127.0.0.1:5432`).
- **Vector Storage**: **`pgvector` extension** (`embedding_documents` table, 7,910 rows, 384 dimensions, `all-MiniLM-L6-v2`).
- **Relational Counts**:
  - `hotels`: **1,661 rows**
  - `hotel_locations`: **1,661 rows**
  - `hotel_scores`: **1,661 rows**
  - `hotel_sources`: **1,661 rows**
  - `hotel_amenities`: **1,661 rows**
  - `embedding_documents`: **7,910 rows**
  - `domain_events`: **1,661 rows**
  - `ingestion_records`: **1,661 rows**
  - `ingestion_runs`: **1 row**
- **Recommendation Engine**: Reciprocal Rank Fusion (RRF, $k=60$) combining Content-Based feature similarity and Collaborative Filtering.
- **Explainability Layer**: Analytical feature-matching engine (`scripts/explainability/explainer.py`) computing aspect score alignments.
- **RAG Architecture**: Hybrid Retrieval (Vector Search + SQL Metadata Filters + Recommender Reranking) $\rightarrow$ `ContextCompressor` (1,500-token budget) $\rightarrow$ `PromptOrchestrator` $\rightarrow$ Ollama Local LLM (`mistral`/`llama3`) $\rightarrow$ `CitationInjector` $\rightarrow$ `GroundingValidator`.
- **Orchestration & Data Pipeline**: Single-command CLI orchestrator (`scripts/orchestrator.py`), SHA-256 field-level diff engine (`diff_engine.py`), dry-run safety (`dry_run.json`), human approval gate (`apply --run-id`), selective vector sync, and live ASCII terminal progress monitoring (`ProgressTracker`) with Ctrl+C protection.
- **Frontend Architecture**: React + TypeScript + Vite + TanStack Query frontend rendering live trust scores, aspect progress bars, and provenance drawers.
- **Test Suite Status**: **`50 / 50 PASSED`** across the complete backend Pytest suite.

---

## 18. The Story of TrustLayer-AI (Human Engineering Narrative)

1. **The Vision**: We set out to build an explainable, hallucination-free hotel recommendation engine for Delhi NCR that travelers could trust, combining personalized recommendations with grounded conversational AI.
2. **Data Acquisition**: We collected raw metadata and traveler reviews for 1,661 hotels using the Google Places API, navigating API detail caps and identifying missing price fields early on.
3. **Cleaning & NLP Processing**: We cleaned the dataset and deployed DistilBERT transformer models to extract sentiment probabilities and aspect-specific scores across Cleanliness, Service, Location, Value, and Staff Behavior.
4. **Feature Engineering**: We engineered a Gaussian-distributed Trust Score and power-law Popularity Score, consolidating all 1,661 hotels into a canonical 26-column dataset (`final_hotel_dataset.csv`).
5. **Initial Model Failure & Audit**: Our initial collaborative filtering models suffered a catastrophic failure (NDCG@10 = 0.006) due to extreme matrix sparsity and random synthetic noise, causing the linear hybrid model to collapse into 100% collaborative filtering.
6. **Data-Centric Remediation**: We halted execution, overhauled interaction generation to reflect realistic traveler preferences, and replaced linear score blending with Reciprocal Rank Fusion (RRF), elevating NDCG@10 to > 0.12.
7. **Transparent Explainability**: We abandoned black-box SHAP approximations in favor of an analytical feature-matching explainer that generates transparent aspect alignment bars and qualitative badges in real time.
8. **Hybrid RAG Construction**: We chunked review text into 7,910 segments and built a Hybrid Retrieval engine combining vector similarity, metadata filtering, and recommender reranking, achieving Precision@5 of 0.81.
9. **Hallucination Protection**: We integrated local Ollama LLMs with a token-budget context compressor, prompt orchestrator, citation injector, and a grounding validator that actively stripped fabricated amenity claims.
10. **Backend Repository Abstraction**: We refactored the backend using Clean Architecture repository patterns to decouple API routes from raw CSV and ChromaDB file operations.
11. **PostgreSQL & pgvector Migration**: We migrated the entire system to PostgreSQL 17.6 with `pgvector`, achieving 1.0000 embedding cosine similarity parity, 100% 20-query RAG parity, and zero orphan records.
12. **Repeatable Data Ingestion**: We built a 9-stage repeatable data ingestion engine with SHA-256 field-level diffing, dry-run safety, human approval gates, and selective vector synchronization.
13. **Master Orchestration**: We unified all upstream processing stages into a single CLI orchestrator (`python -m scripts.orchestrator full`), enabling end-to-end execution from raw APIs to database diffs.
14. **Live Operational Visibility**: We added an interactive ASCII terminal progress dashboard and Ctrl+C interrupt protection, ensuring zero database mutation during unexpected terminations.
15. **Verified System State**: We validated the complete production system with a 50/50 passing test suite, establishing a fully grounded, explainable AI recommendation platform.

---

## 19. Source Evidence Index

The forensic reconstruction in this document is supported by the following exact repository files:

### Documentation & Reports
- `PROJECT_PRESENTATION_SOURCE_OF_TRUTH.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/project_presentation/PROJECT_PRESENTATION_SOURCE_OF_TRUTH.md]
- `STAGE23.1_BACKEND_AUDIT_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage23/STAGE23.1_BACKEND_AUDIT_REPORT.md]
- `STAGE24.1_MANUAL_BACKEND_VERIFICATION_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage24/STAGE24.1_MANUAL_BACKEND_VERIFICATION_REPORT.md]
- `STAGE24.2_PGVECTOR_BACKFILL_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage24.2/STAGE24.2_PGVECTOR_BACKFILL_REPORT.md]
- `STAGE24.4_REAL_POSTGRESQL_DEPLOYMENT_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage24/STAGE24.4_REAL_POSTGRESQL_DEPLOYMENT_REPORT.md]
- `STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage24/STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md]
- `STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/data_pipeline/STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md]
- `STAGE27_ORCHESTRATION_GAP_ANALYSIS.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage27/STAGE27_ORCHESTRATION_GAP_ANALYSIS.md]
- `STAGE28_PRE_IMPLEMENTATION_AUDIT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage28/STAGE28_PRE_IMPLEMENTATION_AUDIT.md]
- `STAGE28_FINAL_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage28/STAGE28_FINAL_REPORT.md]
- `STAGE29_LIVE_PROGRESS_REPORT.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/architecture_and_system_docs/stage29/STAGE29_LIVE_PROGRESS_REPORT.md]
- `recommender_diagnostics.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/recommender_diagnostics.md]
- `recommender_remediation_report.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/recommender_remediation_report.md]
- `explainability_evaluation.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/explainability_evaluation.md]
- `retrieval_evaluation.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/retrieval_evaluation.md]
- `stage_d_evaluation.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/stage_d_evaluation.md]
- `visualization_summary.md`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research_and_audit_reports/visualization_summary.md]

### Research Notebooks
- `01_hotel_metadata_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/01_hotel_metadata_analysis.ipynb]
- `02_review_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/02_review_analysis.ipynb]
- `03_sentiment_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/03_sentiment_analysis.ipynb]
- `04_absa_explainability_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/04_absa_explainability_analysis.ipynb]
- `05_feature_engineering_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/05_feature_engineering_analysis.ipynb]
- `06_user_dataset_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/06_user_dataset_analysis.ipynb]
- `07_interaction_analysis.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/07_interaction_analysis.ipynb]
- `08_final_dataset_overview.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/08_final_dataset_overview.ipynb]
- `09_recommender_diagnostics.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/09_recommender_diagnostics.ipynb]
- `10_interaction_quality_audit.ipynb`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/research/notebooks/10_interaction_quality_audit.ipynb]

### Source Code & Test Suites
- `scripts/orchestrator.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/orchestrator.py]
- `scripts/orchestration/progress.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/orchestration/progress.py]
- `scripts/ingestion/diff_engine.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/diff_engine.py]
- `scripts/ingestion/pipeline.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/ingestion/pipeline.py]
- `scripts/explainability/explainer.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/scripts/explainability/explainer.py]
- `app/repositories/postgres_hotel_repository.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/postgres_hotel_repository.py]
- `app/repositories/pgvector_embedding_repository.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/app/repositories/pgvector_embedding_repository.py]
- `tests/verification/test_stage24_5_complete_backend.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/verification/test_stage24_5_complete_backend.py]
- `tests/ingestion/test_pipeline_stage26.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/ingestion/test_pipeline_stage26.py]
- `tests/orchestration/test_stage28_orchestrator.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/orchestration/test_stage28_orchestrator.py]
- `tests/orchestration/test_stage29_progress.py`: [file:///d:/Side_Projects/0_Independent_Project/NewBackend_start/tests/orchestration/test_stage29_progress.py]
