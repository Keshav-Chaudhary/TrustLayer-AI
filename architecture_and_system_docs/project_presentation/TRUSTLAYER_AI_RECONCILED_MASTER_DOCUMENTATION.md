# TrustLayer-AI: System Architecture, Engineering History, and Reconciled Technical Documentation

---

## 1. Contradiction & Reconciliation Ledger

This ledger audits every metric, date, and named quantity that appears across the project documentation (`PROJECT_PRESENTATION_SOURCE_OF_TRUTH.md`, `FORENSIC_DEVELOPMENT_HISTORY.md`, `TRUSTLAYER_AI_HISTORICAL_TECHNICAL_REPORT.md`, and individual stage reports), identifying discrepancies and establishing the reconciled baseline.

| Topic / Quantity | Document A Value & Source | Document B Value & Source | Status / Conflict Analysis | Reconciled Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **Raw Review Count** | `8,305` (`TRUSTLAYER_AI_HISTORICAL_TECHNICAL_REPORT.md`, theoretical API cap: 1,661 × 5) | `7,785` (`02_review_analysis.ipynb`, raw API payload count) / `7,634` (`clean_reviews.py`, `reviews_cleaned.csv`) | **Lineage Clarified** (Not a contradiction): 8,305 is the theoretical API ceiling; 7,785 is the actual raw API responses received; 7,634 is the final sanitized review dataset after filtering non-ASCII characters and empty entries. | **7,785 raw reviews collected; 7,634 sanitized reviews in `reviews_cleaned.csv`.** |
| **Hotel Count in Stage A Recommender Evaluation** | `1,379` (`09_recommender_diagnostics.ipynb`, `FORENSIC_DEVELOPMENT_HISTORY.md`) | `1,661` (`final_hotel_dataset.csv`, `TRUSTLAYER_AI_HISTORICAL_TECHNICAL_REPORT.md`) | **Scope Clarified**: 1,661 is the total hotel catalog size. In Stage A V1 interaction matrix, only 1,379 hotels received $\ge 1$ synthetic user interaction (resulting in 99.27% matrix sparsity). | **1,661 total catalog hotels; 1,379 hotels had active interactions in Stage A V1 test set.** |
| **Trust Score Weight Formula** | `0.50 Rating / 0.35 Sentiment / 0.15 Review Support` (`engineer_features.py`, `STAGE28_FINAL_REPORT.md`) | `0.5 Rating / 0.3 Sentiment / 0.2 Popularity` (`PROJECT_PRESENTATION_SOURCE_OF_TRUTH.md` early text draft) | **Conflict Resolved**: Code implementation in `engineer_features.py` executes `0.50 * rating_norm + 0.35 * sentiment_prob + 0.15 * review_support`. The 0.5/0.3/0.2 formula was an unexecuted proposal. | **`0.50 * Rating + 0.35 * Sentiment + 0.15 * Support` (Implemented Code Baseline).** |
| **Master Test Suite Count** | `50/50 PASSED` (`TRUSTLAYER_AI_HISTORICAL_TECHNICAL_REPORT.md`, `STAGE28_FINAL_REPORT.md`) | Itemized sum: 4 (Stage 29) + 6 (Stage 28) + 8 (Stage 26) + 18 (Stage 24.5) + 14 (API/Grounding) = 50 | **Verified Agreed**: Itemized test module counts sum exactly to 50 total automated tests. | **50 total automated backend tests across 5 test files.** |
| **Intermediate Test Milestones (42 vs. 50)** | `42/42 PASSED` (`STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md`) | `50/50 PASSED` (`STAGE28_FINAL_REPORT.md`, Stage 29) | **Milestone Sequence**: 42 tests were active at Stage 26. Stage 28 added 6 CLI orchestrator tests (48), and Stage 29 added 4 progress tracker tests while pruning 2 redundant tests, reaching 50. | **Sequential progression: 42 (Stage 26) $\rightarrow$ 48 (Stage 28) $\rightarrow$ 50 (Stage 29).** |
| **ChromaDB vs. PostgreSQL Vector Storage** | ChromaDB active in Stage C (`retriever.py`, `data/vector_store/`) | PostgreSQL + `pgvector` active in Stage 24.2 (`backfill_pgvector.py`, `trustlayer_db`) | **Architecture Pivot**: ChromaDB was used during early RAG prototyping (Stage C). Stage 24.2 migrated vector storage to PostgreSQL 17.6 `pgvector` to eliminate data drift. | **PostgreSQL 17.6 + `pgvector` is the sole production runtime backend.** |
| **SHAP vs. Analytical Explainer** | SHAP explored in Stage 7 (`shap_explainer.py`) | Analytical Feature Matching implemented in Stage 7 (`explainer.py`) | **Architecture Pivot**: SHAP was abandoned due to $> 1.5$s latency per query. Analytical explainer executes in $< 5$ms. | **Analytical Feature-Matching Explainer is the active implementation.** |

---

## 2. Project Overview & Problem Statement

### 2.1 Overview
**TrustLayer-AI** is a preference-aware, explainable hotel recommendation system integrated with a grounded Retrieval-Augmented Generation (RAG) conversational search interface. Designed for accommodation properties in Delhi NCR (1,661 properties), the system extracts 5-dimensional Aspect-Based Sentiment Analysis (ABSA) scores from guest text reviews, ranks hotels using Reciprocal Rank Fusion (RRF), generates real-time feature-alignment explanations, and answers natural language travel queries backed by review evidence citations and hallucination validation.

### 2.2 Problem Statement
Commercial travel recommendation and conversational search engines face four core engineering challenges:
1. **Opaque Item Ranking**: Standard collaborative and content-based recommendation algorithms output unexplainable scalar scores without detailing how property attributes match user preference priorities.
2. **LLM Hallucinations in Conversational Search**: Unconstrained Large Language Models (LLMs) frequently generate unsupported assertions (e.g., fabricating non-existent pool or spa amenities) when answering user queries.
3. **Storage Data Drift**: Operating separate file-based vector stores (such as ChromaDB) alongside tabular metadata CSV files creates data drift, non-atomic schema updates, and a lack of ACID guarantees.
4. **Pipeline Fragmentation**: Executing data scraping, text cleaning, sentiment extraction, and database loading through uncoordinated standalone scripts increases operational risk and leads to unvalidated database overwrites.

### 2.3 System Objectives
- Ingest and sanitize metadata for 1,661 hotels and 7,634 text reviews across Delhi NCR.
- Extract sentence sentiment probabilities using DistilBERT and compute 5 ABSA aspect scores (Cleanliness, Service, Location, Value, Staff Behavior).
- Mitigate collaborative filtering matrix sparsity using Reciprocal Rank Fusion (RRF, $k=60$).
- Provide deterministic, real-time feature alignment explanations in $< 5$ ms.
- Execute hybrid vector retrieval over 7,910 review text chunks, stripping unverified claims via post-generation grounding validation.
- Unify relational metadata and vector embeddings inside PostgreSQL 17.6 + `pgvector` using Clean Architecture repository abstractions.
- Automate pipeline execution via a 9-stage repeatable ingestion engine and a single-command CLI orchestrator (`scripts/orchestrator.py`) featuring terminal progress tracking and signal safety.

---

## 3. System Architecture

The TrustLayer-AI platform consists of five primary subsystems operating over a unified PostgreSQL database infrastructure.

```
[ External Data ]
  ├── Google Places API Metadata (1,661 Hotels)
  └── Google Places Text Reviews (7,634 Reviews)
        │
        ▼
[ Data & Sentiment Pipeline ]
  ├── Data Cleaning & Bounding Box Filter (clean_hotel_metadata.py)
  ├── DistilBERT Sentence Sentiment Polarity (analyze_sentiment.py)
  ├── 5-Aspect Sentiment Extraction (extract_absa_features.py)
  └── Feature Normalization & Trust Scoring (engineer_features.py)
        │
        ▼
[ Canonical Handoff Dataset: final_hotel_dataset.csv (1,661 rows, 26 features) ]
        │
        ▼
[ Ingestion & Orchestration Engine ]
  ├── Master CLI Orchestrator (scripts/orchestrator.py)
  ├── SHA-256 Field-Level Diff Engine (diff_engine.py)
  ├── Dry-Run Safety Boundary (dry_run.json)
  └── Transactional Apply & Selective Vector Sync (selective_vector_sync.py)
        │
        ▼
[ Enterprise Storage: PostgreSQL 17.6 + pgvector (trustlayer_db) ]
  ├── Normalized Relational Metadata (hotels, locations, scores, amenities)
  ├── Transactional Outbox Pattern (domain_events)
  └── Vector Storage (embedding_documents: 7,910 chunks, vector(384))
        │
        ▼
[ FastAPI Backend Repository Layer ]
  ├── Abstract Contracts (BaseHotelRepository, BaseEmbeddingRepository)
  ├── Repositories (PostgresHotelRepository, PgVectorEmbeddingRepository)
  ├── RRF Hybrid Recommender (hybrid.py)
  ├── Analytical Feature Explainer (explainer.py)
  └── Grounded Hybrid RAG Pipeline
        ├── Hybrid Vector Search + Metadata Filter (retriever.py)
        ├── Context Compressor (context_compressor.py: 1,500 tokens)
        ├── Local LLM Inference (llm_service.py: Ollama mistral/llama3)
        ├── Citation Injector (citation_injector.py)
        └── Hallucination Interception (grounding_validator.py)
        │
        ▼
[ React + TypeScript Frontend UI ]
```

---

## 4. Engineering Narrative & Technical Pivots

The implementation of TrustLayer-AI evolved through four major technical pivots driven by empirical observations during development.

### Pivot 1: Matrix Sparsity Failure $\rightarrow$ Reciprocal Rank Fusion (RRF) Remediation
- **Problem Observed**: Offline recommender benchmarking in Stage A yielded near-zero ranking performance ($\text{Precision}@10 = 0.002$, $\text{Recall}@10 = 0.010$, $\text{NDCG}@10 = 0.006$). Linear score blending ($\alpha \cdot S_{\text{CF}} + (1-\alpha) \cdot S_{\text{CB}}$) collapsed into 100% CF dominance ($\alpha = 1.0$).
- **Root Cause**: 
  1. Matrix sparsity in initial V1 synthetic user interactions reached **99.27%** (~3.6 interactions/hotel across 500 users), causing SVD matrix factorization to underfit and output global rating averages.
  2. Score scale mismatch: Content-based cosine similarities clustered between $0.8$ and $0.9$, while SVD predicted ratings ranged from $1.0$ to $5.0$. Linear blending over uncalibrated scales forced grid-search optimization to select $\alpha = 1.0$.
- **Fix Implemented**: 
  1. Regenerated user interactions (`generate_interactions_v2.py`) with realistic preference overlap (66% budget match, 51% area match) and power-law interaction frequency.
  2. Replaced linear score blending with Reciprocal Rank Fusion ($k=60$) in `hybrid.py`:
     $$RRF\_Score(d) = \frac{1}{60 + r_{\text{CF}}(d)} + \frac{1}{60 + r_{\text{CB}}(d)}$$
- **Resulting Measurement**: Elevated ranking quality from $\text{NDCG}@10 = 0.006$ to **$\text{NDCG}@10 > 0.12$** `[VERIFIED — 09_recommender_diagnostics.ipynb, recommender_remediation_report.md]`.

### Pivot 2: SHAP Latency Failure $\rightarrow$ Analytical Explainer Implementation
- **Problem Observed**: Initial explainability prototyping using SHAP (SHapley Additive exPlanations) in `shap_explainer.py` resulted in high computational latency ($> 1.5$ seconds per query) and non-deterministic, dense feature importance scores over rank-fused outputs.
- **Root Cause**: Game-theoretic SHAP marginal value sampling is computationally expensive and unsuitable for real-time REST API endpoints requiring sub-500 ms response times.
- **Fix Implemented**: Replaced SHAP with a deterministic **Analytical Feature-Matching Explainer** (`explainer.py`) that computes explicit aspect alignment percentages:
  $$\text{Alignment}_{\text{aspect}} = 100 \cdot \left(1 - |W_{\text{user, aspect}} - S_{\text{hotel, aspect}}|\right)$$
- **Resulting Measurement**: Reduced explanation calculation latency from $> 1,500$ ms to **$< 5$ ms** `[VERIFIED — explainer.py audit logs]`.

### Pivot 3: ChromaDB Storage $\rightarrow$ PostgreSQL + pgvector Cutover
- **Problem Observed**: Operating file-based ChromaDB vector stores alongside tabular CSV metadata files created data drift between review text embeddings and relational entity metadata.
- **Root Cause**: File-based vector databases lack ACID transaction boundaries. Updating CSV metadata without synchronous vector index updates resulted in stale vector query references.
- **Fix Implemented**: Migrated all 7,910 text review embeddings (`all-MiniLM-L6-v2`, 384 dimensions) to a unified PostgreSQL 17.6 database server using the `pgvector` extension (`backfill_pgvector.py`). Refactored data access routes using Clean Architecture repository interfaces (`PostgresHotelRepository`, `PgVectorEmbeddingRepository`).
- **Resulting Measurement**: Achieved 100% Top-1 RAG query parity between ChromaDB and `pgvector` backfill across 20 benchmark queries `[VERIFIED — STAGE24.2_PGVECTOR_BACKFILL_REPORT.md]`. *Note: Embedding cosine similarity parity across backfilled vectors is reported as 1.0000 `[UNVERIFIED — confirm by re-running backfill_pgvector.py cosine parity check for exact floating point precision]`.*

### Pivot 4: Fragmented Scripts $\rightarrow$ Master CLI Pipeline Orchestrator
- **Problem Observed**: Upstream data acquisition, text cleaning, sentiment extraction, ABSA processing, feature engineering, and database loading scripts were executed as independent, uncoordinated CLI calls.
- **Root Cause**: Lack of unified orchestration increased manual operational overhead and risks of unvalidated database overwrites.
- **Fix Implemented**: Built a single-command CLI master orchestrator (`scripts/orchestrator.py`) incorporating SHA-256 field-level diffing (`diff_engine.py`), dry-run safety reports (`dry_run.json`), human approval boundaries (`--run-id`), live ASCII progress tracking (`ProgressTracker`), and `SIGINT` (Ctrl+C) signal handlers.
- **Resulting Measurement**: Passed 6/6 orchestrator tests (`test_stage28_orchestrator.py`) and 4/4 progress tracking tests (`test_stage29_progress.py`), unifying all 6 upstream pipeline stages under a single command `[VERIFIED — STAGE28_FINAL_REPORT.md, STAGE29_LIVE_PROGRESS_REPORT.md]`.

---

## 5. Data & Pipeline Lineage

The data transformation pipeline converts raw external API payloads into normalized PostgreSQL entities and vector embeddings across 6 sequential stages.

| Stage | Script / Module | Input Artifact | Output Artifact / Target | Transformation Logic & Record Counts |
| :--- | :--- | :--- | :--- | :--- |
| **1. Scraping** | `fetch_google_places.py`, `fetch_google_reviews.py` | Google Places REST API | `delhi_hotels_raw.csv`, `reviews_raw.csv` | Grid sampling across 15 NCR area clusters. Output: **1,661 raw hotels**, **7,785 raw text reviews**. |
| **2. Cleaning** | `clean_hotel_metadata.py`, `clean_reviews.py` | `delhi_hotels_raw.csv`, `reviews_raw.csv` | `delhi_hotels_cleaned.csv`, `reviews_cleaned.csv` | Deduplication by `place_id`, spatial bounding-box filter ($28.40^\circ\text{N} \le \text{Lat} \le 28.88^\circ\text{N}$, $76.84^\circ\text{E} \le \text{Lng} \le 77.35^\circ\text{E}$), non-ASCII character stripping. Output: **1,661 cleaned hotels** (1,618 with reviews, 43 zero-review properties), **7,634 cleaned reviews**. |
| **3. Sentiment** | `analyze_sentiment.py` | `reviews_cleaned.csv` | `reviews_with_sentiment.csv` | DistilBERT sentence-level positive sentiment probability extraction ($P_{\text{pos}} \in [0, 1]$). |
| **4. ABSA** | `extract_absa_features.py` | `reviews_with_sentiment.csv` | `hotel_absa_features.csv` | Aspect keyword masking + DistilBERT sentiment masking across Cleanliness, Service, Location, Value, Staff Behavior ($S_{\text{aspect}} \in [0, 100]$). |
| **5. Features** | `engineer_features.py` | `delhi_hotels_cleaned.csv`, `hotel_absa_features.csv` | `final_hotel_dataset.csv` | Feature scaling (`MinMaxScaler`), budget tier proxying for missing `price_level`, median aspect imputation for 43 zero-review hotels, composite Trust Score calculation ($0.50 \cdot \text{Rating} + 0.35 \cdot \text{Sentiment} + 0.15 \cdot \text{Support}$). Output: **1,661 canonical rows, 26 feature columns** (SHA-256: `eca959c7...`). |
| **6. Chunking** | `prepare_rag_chunks.py` | `final_hotel_dataset.csv`, `reviews_cleaned.csv` | `data/rag/ChIJ*.json` | Text segmentation into Chunks A (Profile), B (Aspects), C (Positive), D (Negative), E (Recommender Signals). Output: **7,910 review evidence text chunks**. |

---

## 6. Authoritative Database Schema

The production PostgreSQL database (`trustlayer_db`) enforces relational integrity and vector storage across 9 primary tables.

```sql
-- 1. Master Hotel Entity Table
CREATE TABLE hotels (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    phone VARCHAR(50),
    website TEXT,
    rating NUMERIC(3, 2),
    user_ratings_total INTEGER,
    price_level INTEGER,
    budget_category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Hotel Geographic Location Table
CREATE TABLE hotel_locations (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    latitude NUMERIC(10, 7) NOT NULL,
    longitude NUMERIC(10, 7) NOT NULL,
    area_cluster VARCHAR(100) NOT NULL
);

-- 3. Hotel Quality & Sentiment Scores Table
CREATE TABLE hotel_scores (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    trust_score NUMERIC(5, 2) NOT NULL,
    popularity_score NUMERIC(5, 2) NOT NULL,
    cleanliness_score NUMERIC(5, 2) NOT NULL,
    service_score NUMERIC(5, 2) NOT NULL,
    location_score NUMERIC(5, 2) NOT NULL,
    value_score NUMERIC(5, 2) NOT NULL,
    staff_score NUMERIC(5, 2) NOT NULL
);

-- 4. Hotel External Data Sources Table
CREATE TABLE hotel_sources (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    place_id VARCHAR(255) UNIQUE NOT NULL,
    google_maps_url TEXT
);

-- 5. Hotel Amenities Table
CREATE TABLE hotel_amenities (
    hotel_id VARCHAR(64) PRIMARY KEY REFERENCES hotels(id) ON DELETE CASCADE,
    has_wifi BOOLEAN DEFAULT FALSE,
    has_parking BOOLEAN DEFAULT FALSE,
    has_pool BOOLEAN DEFAULT FALSE,
    has_restaurant BOOLEAN DEFAULT FALSE,
    has_ac BOOLEAN DEFAULT FALSE,
    has_bar BOOLEAN DEFAULT FALSE,
    has_gym BOOLEAN DEFAULT FALSE,
    has_spa BOOLEAN DEFAULT FALSE
);

-- 6. Vector Embedding Storage Table (pgvector)
CREATE TABLE embedding_documents (
    id VARCHAR(128) PRIMARY KEY,
    hotel_id VARCHAR(64) REFERENCES hotels(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    metadata JSONB,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Transactional Outbox Domain Events Table
CREATE TABLE domain_events (
    id VARCHAR(64) PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- 8. Ingestion Runs Table
CREATE TABLE ingestion_runs (
    id VARCHAR(64) PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    target_environment VARCHAR(50) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 9. Ingestion Records Change Audit Table
CREATE TABLE ingestion_records (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(64) REFERENCES ingestion_runs(id) ON DELETE CASCADE,
    hotel_id VARCHAR(64) REFERENCES hotels(id) ON DELETE CASCADE,
    action VARCHAR(20) NOT NULL,
    diff_payload JSONB
);
```

---

## 7. Testing & Evaluation Summary

The master backend automated test suite comprises **50 automated Pytest test cases** across 5 test modules.

### 7.1 Automated Backend Test Composition

| Test Module File | Stage / Area Covered | Executed Test Scope | Status | Classification |
| :--- | :--- | :--- | :---: | :--- |
| `tests/test_stage29_progress.py` | Stage 29 Progress & Signal Safety | ASCII dashboard rendering, ETA calculation, log file output, `SIGINT` handler interrupt safety | 4 / 4 PASSED | **VERIFIED** |
| `tests/test_stage28_orchestrator.py` | Stage 28 CLI Orchestration | Dry-run isolation, approval gate enforcement, manifest generation, read-only safety | 6 / 6 PASSED | **VERIFIED** |
| `tests/test_pipeline_stage26.py` | Stage 26 Ingestion & Diffing | Schema contract validation, SHA-256 content hashing, diff generation, selective vector sync | 8 / 8 PASSED | **VERIFIED** |
| `tests/test_stage24_5_complete_backend.py` | Stage 24.5 PostgreSQL Provenance | Relational integrity, FK constraints, outbox domain events, `pgvector` retrieval parity | 18 / 18 PASSED | **VERIFIED** |
| `tests/test_api_endpoints.py` & `test_grounding.py` | API, Context & Grounding | FastAPI `/recommend`, `/chat`, `/explanation` routes, context compression, citation injection | 14 / 14 PASSED | **VERIFIED** |
| **Master Suite Total** | **Complete Backend Infrastructure** | **Recomputed Sum: 4 + 6 + 8 + 18 + 14** | **50 / 50 PASSED** | **VERIFIED** |

### 7.2 System Evaluation Metrics Summary

| Evaluated Subsystem | Metric Name | Reported Value | Benchmark Target | Status / Classification |
| :--- | :--- | :---: | :---: | :--- |
| **Sentiment Analysis** | DistilBERT vs. Rating Pearson $r$ | $r \approx 0.84$ | $r \ge 0.70$ | **VERIFIED** `[03_sentiment_analysis.ipynb]` |
| **Stage A Recommender** | Offline $\text{NDCG}@10$ | $0.006$ | $\ge 0.100$ | **VERIFIED** `[09_recommender_diagnostics.ipynb]` (Failed baseline) |
| **Stage A.1 Recommender** | Remediated RRF $\text{NDCG}@10$ | $> 0.120$ | $\ge 0.100$ | **VERIFIED** `[recommender_remediation_report.md]` |
| **Aspect Explainer** | Real-Time Execution Latency | $< 5$ ms | $< 500$ ms | **VERIFIED** `[explainer.py]` |
| **Hybrid RAG Retrieval** | Precision@5 / Recall@5 / MRR | $0.81$ / $0.79$ / $0.83$ | $\ge 0.70$ | `[UNVERIFIED — confirm by re-running retrieval_evaluation.py script]` |
| **Grounding Validator** | Grounded Response Rate | $96.7\%$ (3 active interceptions) | $\ge 95.0\%$ | `[UNVERIFIED — confirm by re-running stage_d_evaluation.py benchmark script]` |
| **Grounding Validator** | Hallucination Rate | $1.3\%$ | $\le 2.0\%$ | `[UNVERIFIED — confirm by re-running stage_d_evaluation.py benchmark script]` |
| **pgvector Backfill** | Vector Cosine Similarity Parity | $1.0000$ | $= 1.0000$ | `[UNVERIFIED — confirm by re-running backfill_pgvector.py cosine parity check]` |
| **pgvector Backfill** | Top-1 RAG Query Parity | 20 / 20 ($100.0\%$) | $100.0\%$ | **VERIFIED** `[STAGE24.2_PGVECTOR_BACKFILL_REPORT.md]` |

---

## 8. Documented System Limitations

1. **Google Places API Detail Review Ceiling**: The external Google Places Details API restricts review retrieval to a maximum of 5 reviews per property (yielding 7,785 raw review records across 1,661 hotels), limiting long-tail sentiment text analysis.
2. **Missing Price Attribute**: Google Places API returned 100% missing `price_level` data across properties in India, requiring engineered `budget_category` proxy variables based on star ratings and area cluster tariffs.
3. **Synthetic User Interaction Base**: Collaborative filtering evaluation relies on synthetic user interaction profiles (V2 preference overlap model) rather than commercial booking logs.
4. **Single-Host Developer Environment**: Performance latency benchmarks ($< 5$ ms explainer latency, $165.8$ ms retrieval latency) were evaluated on single-host developer hardware rather than multi-node production clusters.

---

## 9. Open Questions & Verification Checklist

Before final submission of the IP report, the following items should be verified directly against local code execution and log files:

- [ ] **Placeholders**: Fill in `[Roll Number — TO BE FILLED BY STUDENT]` and `[Advisor Name — TO BE FILLED BY STUDENT]` in `latext_files/front/declaration.tex` and `metadata.tex`.
- [ ] **Grounding & Hallucination Benchmark**: Re-run `scripts/evaluation/stage_d_evaluation.py` to confirm whether the reported $96.7\%$ grounded response rate and $1.3\%$ hallucination rate over 150 queries match current local outputs exactly.
- [ ] **Retrieval Ablation Metrics**: Re-run `scripts/evaluation/retrieval_evaluation.py` to verify Precision@5 ($0.81$), Recall@5 ($0.79$), and MRR ($0.83$).
- [ ] **Floating Point Cosine Parity**: Re-run `backfill_pgvector.py` similarity checks to confirm whether ChromaDB vs. `pgvector` average cosine similarity is exactly $1.0000$ or $0.9999...$ under standard floating point precision.
- [ ] **BibTeX References**: Verify that all `\cite{...}` keys in LaTeX chapter files match entries in `latext_files/ref.bib`.

---

## 10. Source Evidence Index

The technical details and metrics in this document are derived from the following project repository source files:

### Data Engineering & NLP
- `scripts/scraping/fetch_google_places.py` & `fetch_google_reviews.py`
- `scripts/cleaning/clean_hotel_metadata.py` & `clean_reviews.py`
- `scripts/nlp/analyze_sentiment.py` & `extract_absa_features.py`
- `scripts/features/engineer_features.py`

### Recommender, Explainability & RAG
- `scripts/recommender/hybrid.py` & `generate_interactions_v2.py`
- `scripts/explainability/explainer.py`
- `app/services/retriever.py`, `context_compressor.py`, `llm_service.py`, `citation_injector.py`, & `grounding_validator.py`

### Database & Ingestion Engine
- `app/repositories/postgres_hotel_repository.py` & `pgvector_embedding_repository.py`
- `scripts/ingestion/diff_engine.py`, `pipeline.py`, & `selective_vector_sync.py`
- `scripts/orchestrator.py` & `scripts/orchestration/progress.py`

### Automated Pytest Suite
- `tests/test_stage29_progress.py`
- `tests/test_stage28_orchestrator.py`
- `tests/test_pipeline_stage26.py`
- `tests/test_stage24_5_complete_backend.py`
- `tests/test_api_endpoints.py` & `test_grounding.py`

### Research Notebooks
- `research/notebooks/01_hotel_metadata_analysis.ipynb` through `10_interaction_quality_audit.ipynb`
