# TrustLayer-AI: RAG-Enhanced Explainable AI-Based Hotel Recommendation System

**Student Name:** Keshav  
**Roll Number:** [Roll Number]  
**Degree:** B.Tech. in Computer Science & Engineering  
**Date:** August 2, 2026  
**IP Track:** Engineering  
**Advisor:** [Advisor Name]  
**Institution:** Indraprastha Institute of Information Technology, New Delhi  

---

## Student Declaration

I hereby declare that the work presented in the Independent Project report entitled **"TrustLayer-AI: RAG-Enhanced Explainable AI-Based Hotel Recommendation System"** submitted by me for the partial fulfilment of the requirements for the degree of B.Tech. in Computer Science & Engineering at Indraprastha Institute of Information Technology, Delhi, is an authentic record of my work carried out under the guidance of **[Advisor Name]**. Due acknowledgements have been given in the report for all material used. This work has not been submitted elsewhere for the award of any other degree or diploma.

**Keshav**  
Place & Date: New Delhi, August 2, 2026  

### Certificate

This is to certify that the above statement made by the candidate is correct to the best of my knowledge.

**[Advisor Name]**  
Place & Date: New Delhi, August 2, 2026  

---

## Abstract

Traditional hotel recommendation platforms operate as unexplainable black boxes, offering little transparency regarding why specific items are recommended. Moreover, integrating Large Language Models (LLMs) into conversational travel search introduces hallucination risks, such as fabricating non-existent hotel amenities or misrepresenting traveler review evidence. This Independent Project presents **TrustLayer-AI**, a preference-aware, explainable hybrid hotel recommendation and grounded Retrieval-Augmented Generation (RAG) platform developed through a 29-stage engineering evolution.

The system processes 1,661 hotel profiles and 7,910 review evidence chunks across Delhi NCR. The data pipeline extracts sentence-level sentiment probabilities using DistilBERT and computes 5-dimensional Aspect-Based Sentiment Analysis (ABSA) scores across Cleanliness, Service, Location, Value, and Staff Behavior. An engineered Gaussian Trust Score and power-law Popularity Score are combined with metadata into a canonical dataset. Early collaborative filtering experiments suffered from severe 99.27% matrix sparsity and synthetic interaction noise, causing linear score blending to collapse into single-model dominance ($\text{NDCG}@10 = 0.006$). This was remediated by overhauling interaction preference modeling and replacing linear score blending with Reciprocal Rank Fusion (RRF, $k = 60$), elevating recommendation quality ($\text{NDCG}@10 > 0.12$).

To provide real-time transparency without the high computational latency of SHAP approximations, an analytical feature-matching explainer engine calculates explicit aspect alignment scores. The RAG architecture executes Hybrid Retrieval combining 384-dimensional vector similarity (`all-MiniLM-L6-v2`), SQL metadata filtering, and recommender reranking ($\text{Precision}@5 = 0.81$). Context is passed through a token-budget compressor, prompt orchestrator, local Ollama LLM, citation injector, and a grounding validator that strips unverified amenity claims, achieving a 96.7% grounded response rate and a 1.3% hallucination rate over benchmark evaluation.

To enforce data integrity, the backend was decoupled using Clean Architecture repository patterns and migrated to a unified PostgreSQL 17.6 database engine with `pgvector`, demonstrating 1.0000 average embedding cosine similarity parity against legacy file stores. System updates are managed via a repeatable ingestion lifecycle featuring SHA-256 field-level diffing, dry-run safety, human approval gates, selective vector synchronization, and a single-command CLI orchestrator with real-time progress monitoring. TrustLayer-AI demonstrates how hybrid recommendation models, structured explainability, and validated RAG can be combined into an auditable, evidence-grounded recommendation system.

**Keywords:** Recommender Systems, Reciprocal Rank Fusion, Aspect-Based Sentiment Analysis, Retrieval-Augmented Generation, Grounding Validation, pgvector, PostgreSQL.

---

## Acknowledgments & Work Distribution

### Acknowledgments
I would like to express my sincere gratitude to my advisor, **[Advisor Name]**, for their guidance, valuable insights, and continuous support throughout the duration of this Independent Project. Their constructive feedback and technical perspective were instrumental in shaping the architecture and execution of this work.

I also extend my gratitude to Indraprastha Institute of Information Technology, Delhi (IIIT Delhi) for providing the necessary academic environment, computational infrastructure, and resources required to carry out this project.

### Work Distribution
This report presents an Independent Project (IP) conducted individually by **Keshav**. All phases of the project—including requirement formulation, data acquisition, sentiment modeling, recommendation engine implementation, empirical evaluation, database migration, and orchestration pipeline design—were carried out individually by the author under faculty supervision.

---

## Table of Contents

- **Student Declaration** `i`
- **Abstract** `ii`
- **Acknowledgments & Work Distribution** `iii`
- **Table of Contents** `iv`
- **1. Introduction** `1`
  - 1.1 Background `1`
  - 1.2 Problem Statement `1`
  - 1.3 Motivation `2`
  - 1.4 Research and Engineering Questions `3`
  - 1.5 Objectives `3`
  - 1.6 Scope of the Project `4`
  - 1.7 Contributions `4`
  - 1.8 Organization of the Report `5`
- **2. Literature Review** `7`
  - 2.1 Hotel Recommendation Systems and Filtering Paradigms `7`
  - 2.2 Recommender Evaluation and Ranking Metrics `8`
  - 2.3 Explainable Recommendation and Feature Interpretability `9`
  - 2.4 Sentiment Analysis and Aspect-Based Sentiment Analysis (ABSA) `10`
  - 2.5 Retrieval-Augmented Generation (RAG) Architecture `10`
  - 2.6 Grounded and Trustworthy Conversational AI `11`
  - 2.7 Vector Databases and Unified Database Storage Migration `12`
  - 2.8 Data Provenance and Reproducible Data Engineering `12`
  - 2.9 Research and Engineering Gap Summary `13`
- **3. Methodology and System Architecture** `14`
  - 3.1 Overall System Methodology `14`
  - 3.2 Data Acquisition `15`
  - 3.3 Data Cleaning and Preparation `15`
  - 3.4 Sentiment Analysis and Aspect-Based Sentiment Analysis (ABSA) `16`
  - 3.5 Feature Engineering and Trust Scoring `17`
  - 3.6 Recommendation Methodology and Engineering Pivots `18`
  - 3.7 Explainability Methodology `19`
  - 3.8 Retrieval-Augmented Generation (RAG) Methodology `19`
  - 3.9 Vector Retrieval Evolution and PostgreSQL Migration `20`
  - 3.10 PostgreSQL Data Architecture `21`
  - 3.11 Repository Abstraction and Backend Architecture `21`
  - 3.12 Repeatable Data Ingestion Methodology (Stage 26) `22`
  - 3.13 Master Pipeline Orchestration and Progress Tracking (Stages 28 & 29) `22`
  - 3.14 Experimental Methodology `23`
  - 3.15 End-to-End Operational Lifecycle `23`
- **4. Experimental Evaluation and Results** `25`
  - 4.1 Experimental Evaluation Overview `25`
  - 4.2 Dataset and Data Processing Results `25`
  - 4.3 Sentiment Analysis and ABSA Results `26`
  - 4.4 Trust and Feature Engineering Results `26`
  - 4.5 Initial Recommendation System Diagnostic Failure (Stage A) `27`
  - 4.6 Recommendation System Remediation and RRF Results (Stage A.1) `27`
  - 4.7 Explainability Evaluation `28`
  - 4.8 RAG Retrieval Evaluation and Ablation `28`
  - 4.9 Grounding and Hallucination Evaluation `28`
  - 4.10 ChromaDB -> PostgreSQL/pgvector Migration Results (Stage 24.2) `29`
  - 4.11 PostgreSQL Relational Integrity Results (Stage 24.5) `29`
  - 4.12 Stage 26 Ingestion Results `30`
  - 4.13 Stage 28 Master Orchestration Results `30`
  - 4.14 Stage 29 Live Progress Results `30`
  - 4.15 Master Backend Automated Testing Results `30`
  - 4.16 Jupyter Research Notebook Experimental Findings & Built-in Visualizations `31`
  - 4.17 End-to-End System Results `32`
  - 4.18 Limitations and Experimental Caveats `32`
  - 4.19 Final Evaluation Summary `32`
- **5. Conclusion and Future Work** `33`
  - 5.1 Project Summary `33`
  - 5.2 Major Technical Contributions `34`
  - 5.3 Summary of Experimental Findings `35`
  - 5.4 Engineering Lessons Learned `36`
  - 5.5 Project Limitations `36`
  - 5.6 Future Work `37`
  - 5.7 Final Conclusion `38`
- **Bibliography** `39`

---

## Chapter 1: Introduction

### 1.1 Background
Modern hospitality e-commerce and online travel platforms rely heavily on recommendation engines to assist users in navigating extensive options. In destinations such as Delhi NCR, where travelers evaluate hundreds of accommodation properties across diverse budgets, locations, and amenities, effective personalization is critical. Traditional recommendation platforms typically compute user-item affinities using collaborative filtering (CF) algorithms, matrix factorization (such as Singular Value Decomposition), or content-based similarity models.

However, conventional recommendation systems suffer from significant usability and trust limitations. Most algorithms operate as black boxes, presenting users with ranked lists of items without transparent justifications for *why* a specific hotel was selected for a specific traveler profile. Furthermore, while recent advances in conversational Artificial Intelligence and Large Language Models (LLMs) enable intuitive natural language query interfaces, deploying naive Retrieval-Augmented Generation (RAG) architectures introduces severe reliability risks. Large Language Models frequently generate plausible yet unsupported claims—commonly termed hallucinations—such as fabricating non-existent hotel amenities or misrepresenting guest review sentiment.

To address these challenges, modern recommendation platforms require a unified architecture that integrates preference-aware ranking, multi-dimensional aspect explainability, review-grounded text retrieval, automated hallucination protection, and an enterprise database infrastructure capable of enforcing auditable data lineage.

### 1.2 Problem Statement
The core problem addressed by this project is the lack of explainability, grounding, and infrastructure auditability in automated travel recommendation systems. Specifically, existing platforms exhibit four key deficiencies:
1. **Opaque Ranking Logic**: Standard recommendation models generate scalar prediction scores without exposing how individual property attributes (such as cleanliness, service, or value for money) align with user preferences.
2. **LLM Hallucination and Uncited Responses**: Conversational travel search engines frequently output ungrounded assertions regarding hotel features due to a lack of strict context compression, inline citation enforcement, and post-generation validation.
3. **Data Drift and Fragile Vector Management**: File-based vector databases and raw dataset files operating independently of relational metadata suffer from data drift, non-deterministic similarity searches, and a lack of ACID transaction guarantees.
4. **Uncoordinated Data Ingestion**: Upstream data collection, text cleaning, sentiment extraction, and database loading scripts executed in isolation create operational fragmentation, increasing the risk of unvalidated database overwrites and redundant embedding recalculations.

Operationally, *TrustLayer-AI* defines **trust** as the verifiable alignment between explicit user preference constraints, quantitative aspect-level sentiment scores, retrieved review text evidence, and deterministic database state.

### 1.3 Motivation
Developing a robust recommendation platform requires extending beyond basic model fitting to address real-world system evolution challenges. During the iterative development of TrustLayer-AI, initial collaborative filtering experiments revealed severe performance degradation ($\text{NDCG}@10 = 0.006$) caused by a 99.27% user-item matrix sparsity. Attempting to combine collaborative filtering with content-based models using linear score blending failed because cosine similarity scores (concentrated between 0.8 and 0.9) and predicted rating scores (ranging from 1.0 to 5.0) exhibited severe scale mismatches, causing optimization algorithms to completely disable the content-based component. Resolving this required implementing Reciprocal Rank Fusion (RRF), which combines ordinal ranks rather than uncalibrated raw scores.

Similarly, providing user-facing explanations using SHAP (SHapley Additive exPlanations) approximations proved computationally unfeasible due to high inference latency. This motivated the design of an analytical feature-matching explainer engine that computes direct aspect alignment scores in real time.

Finally, transitioning from legacy file-based stores (CSV files and ChromaDB) to an enterprise PostgreSQL 17.6 database engine equipped with the `pgvector` extension was motivated by the need for unified relational and vector ACID transactions. Managing this transition cleanly required building a 9-stage repeatable data ingestion engine and a single-command master CLI orchestrator equipped with live terminal progress monitoring and signal safety.

### 1.4 Research and Engineering Questions
This Independent Project is guided by five primary research and engineering questions:
- **EQ1 (Hybrid Ranking Fusion)**: How can collaborative filtering and content-based feature similarities be effectively combined using Reciprocal Rank Fusion (RRF) to resolve score calibration mismatches and mitigate extreme matrix sparsity?
- **EQ2 (Real-Time Explainability)**: How can multi-dimensional Aspect-Based Sentiment Analysis (ABSA) scores be structured to generate deterministic, real-time feature-alignment explanations without incurring the latency overhead of SHAP approximations?
- **EQ3 (Grounded Retrieval and Hallucination Protection)**: How can hybrid retrieval (combining vector similarity, metadata filtering, and recommender reranking) be coupled with token-budget context compression and post-generation grounding validation to achieve $>95\%$ grounded response rates and $<2\%$ hallucination rates?
- **EQ4 (Unified Storage Parity)**: How can legacy CSV files and vector databases be migrated to a unified PostgreSQL 17.6 + `pgvector` storage engine while maintaining 100% embedding cosine similarity and recommendation parity?
- **EQ5 (Auditable Pipeline Orchestration)**: How can a multi-stage data engineering pipeline enforce SHA-256 field-level diffing, dry-run safety, human approval gates, selective vector synchronization, and live terminal progress tracking with signal protection?

### 1.5 Objectives
To answer these engineering questions, the project fulfilled the following objectives:
1. **Data Engineering and NLP Sentiment Extraction**: Acquire and clean hotel metadata and review text for 1,661 properties across Delhi NCR; deploy DistilBERT models to extract sentence sentiment probabilities and compute 5 aspect sentiment scores (Cleanliness, Service, Location, Value, Staff Behavior).
2. **Hybrid Recommendation Modeling**: Build Content-Based filtering, Collaborative Filtering (SVD), and Reciprocal Rank Fusion (RRF, $k=60$) models to generate personalized hotel rankings.
3. **Analytical Explainability Layer**: Develop an analytical feature-matching explainer engine (`explainer.py`) to output transparent aspect alignment scores and qualitative explanation badges.
4. **Grounded RAG and Hallucination Protection**: Segment review text into 7,910 chunks, construct a Hybrid Retrieval engine, and build a grounding validation pipeline (`grounding_validator.py`) that intercepts and strips unverified amenity claims from LLM responses.
5. **PostgreSQL 17.6 and pgvector Migration**: Unified relational metadata and 384-dimensional vector embeddings (`all-MiniLM-L6-v2`) inside PostgreSQL 17.6, establishing zero orphan records across an 18-test master provenance suite.
6. **Repeatable Ingestion and CLI Orchestration**: Build a 9-stage repeatable data ingestion engine featuring SHA-256 field-level diffing, dry-run safety (`dry_run.json`), human approval gates, selective vector synchronization, and a single-command master CLI orchestrator (`scripts/orchestrator.py`) with real-time ASCII progress tracking and Ctrl+C interrupt safety.

### 1.6 Scope of the Project
The scope of this project encompasses:
- **Geographic Domain**: Accommodation properties located within the Delhi NCR region (1,661 canonical hotels).
- **Data Ingestion & NLP**: Automated processing of Google Places metadata and text reviews, DistilBERT sentiment extraction, and keyword-masked ABSA feature calculation.
- **Core Modeling**: Machine learning models including SVD matrix factorization, content similarity matching, RRF hybrid fusion, and analytical aspect alignment scoring.
- **Conversational RAG**: Vector similarity search over 7,910 review chunks, prompt orchestration, local Ollama LLM inference (`mistral`/`llama3`), inline citation injection, and post-generation grounding validation.
- **Data Infrastructure**: Enterprise PostgreSQL 17.6 database server with `pgvector`, clean repository abstraction layers (`PostgresHotelRepository`, `PgVectorEmbeddingRepository`), SHA-256 field-level diff engine, FastAPI REST backend (`/api/v1/`), and a React + TypeScript frontend.
- **Orchestration & Tooling**: Master CLI orchestrator, interactive ASCII progress monitoring dashboard (`ProgressTracker`), and structured run logging (`pipeline.log`).

Multi-city scaling outside Delhi NCR, multi-lingual NLP review parsing, and distributed database cluster deployments are outside the present implementation scope.

### 1.7 Contributions
This Independent Project delivers eight concrete system and engineering contributions:
1. **Preference-Aware Hybrid Recommendation Engine**: Demonstrated that Reciprocal Rank Fusion (RRF) resolves score scale mismatches between collaborative and content-based models, elevating recommendation quality ($\text{NDCG}@10 > 0.12$).
2. **Real-Time Analytical Explainability Engine**: Designed a deterministic feature-matching explainer that calculates aspect alignment scores without incurring the high latency of SHAP approximations.
3. **Review-Grounded RAG Pipeline**: Combined hybrid vector retrieval with token-budget context compression and inline citation injection, backing LLM travel answers with explicit review text chunks.
4. **Automated Grounding Validator**: Implemented a post-generation validation layer that cross-references LLM claims against retrieved evidence, stripping unverified amenity assertions ($96.7\%$ grounded response rate, $1.3\%$ hallucination rate).
5. **Unified PostgreSQL + pgvector Migration**: Unified relational metadata and vector storage under PostgreSQL 17.6, verifying 1.0000 average embedding cosine similarity parity and zero orphan records across an 18-test provenance suite.
6. **Repeatable Ingestion and Field-Level Diffing**: Implemented a 9-stage ingestion lifecycle utilizing SHA-256 canonical content hashing and selective vector synchronization to prevent redundant embedding recalculations.
7. **One-Command CLI Orchestrator**: Developed a single-command CLI runner (`python -m scripts.orchestrator full`) unifying all 6 upstream processing stages.
8. **Live Operational Visibility and Signal Safety**: Created an interactive ASCII terminal progress dashboard and a `SIGINT` (Ctrl+C) signal handler that terminates sub-processes cleanly, guaranteeing zero database corruption.

### 1.8 Organization of the Report
The remainder of this report is organized into four subsequent chapters:
- **Chapter 2: Literature Review** — Reviews foundational concepts and prior literature in hotel recommendation systems, collaborative filtering, aspect-based sentiment analysis, Retrieval-Augmented Generation, and vector database architectures.
- **Chapter 3: Methodology and System Architecture** — Provides a comprehensive technical breakdown of the system's 29-stage evolution, covering the data pipeline, NLP sentiment modeling, hybrid RRF recommendation logic, analytical explainability, grounded RAG architecture, PostgreSQL/pgvector database schema, and the repeatable CLI orchestration engine.
- **Chapter 4: Experimental Evaluation and Results** — Presents empirical evaluation results across recommender diagnostic benchmarks, retrieval ablation studies, grounding validator interception rates, pgvector backfill parity checks, and master backend provenance verification.
- **Chapter 5: Conclusion and Future Work** — Summarizes the primary engineering achievements of TrustLayer-AI and outlines future directions for multi-region scaling and automated vector synchronization.

---

## Chapter 2: Literature Review

### 2.1 Hotel Recommendation Systems and Filtering Paradigms
Automated recommendation systems are central to modern e-commerce and online travel platforms. In the hospitality domain, where users evaluate complex multi-attribute entities across varying geographic regions, recommendation algorithms rely on three primary paradigms: content-based filtering, collaborative filtering, and hybrid architectures.

#### 2.1.1 Content-Based Filtering
Content-based filtering (CB) models item recommendations by comparing item attribute profiles against explicit user preference vectors [1]. In hospitality applications, item attributes typically include geographic coordinates, price tiers, and amenity indicators. User profiles are constructed explicitly through preference questionnaires or implicitly by aggregating features of previously interacted properties. The primary advantage of content-based filtering is its resilience to item cold-start problems; new hotels with complete attribute metadata can be recommended immediately without historical booking data. However, content-based systems suffer from over-specialization and item serendipity limitations, as they cannot recommend items outside the user's explicit preference boundaries.

#### 2.1.2 Collaborative Filtering and Matrix Sparsity
Collaborative filtering (CF) relies on historical user-item interaction matrices (such as clicks, views, bookings, and ratings) to learn latent preference factors [2]. Matrix factorization techniques, notably Singular Value Decomposition (SVD), decompose sparse interaction matrices into low-rank user and item embeddings. While collaborative filtering captures implicit behavioral patterns independent of domain feature engineering, its effectiveness is severely constrained by interaction matrix sparsity. In hospitality datasets, where individual users interact with only a tiny fraction of available properties, matrix sparsity frequently exceeds 99%. Under extreme sparsity, SVD algorithms underfit heavily, failing to learn meaningful latent item representations and reverting to predicting global item rating biases.

#### 2.1.3 Hybrid Recommendation Architectures and Fusion Paradigms
To combine the cold-start robustness of content-based filtering with the behavioral insights of collaborative filtering, hybrid recommender systems employ model fusion strategies. Hybrid mechanisms generally fall into two categories:
1. **Score-Based Linear Blending**: Combining prediction scores from individual models via weighted linear summation ($\alpha \cdot S_{\text{CF}} + (1-\alpha) \cdot S_{\text{CB}}$).
2. **Rank-Based Fusion**: Combining ordinal item rankings produced by separate models, such as Reciprocal Rank Fusion (RRF) [3].

In practice, score-based linear blending exhibits severe calibration mismatches. Content-based models produce dense cosine similarity metrics concentrated in a narrow band (e.g., $0.8$ to $0.9$), whereas collaborative filtering models predict scalar ratings spread across wide ranges (e.g., $1.0$ to $5.0$). When grid-search optimization algorithms optimize linear blending weights over uncalibrated score distributions, the optimization process frequently defaults to single-model dominance ($\alpha=1.0$), completely nullifying the content-based signal. Reciprocal Rank Fusion resolves score calibration mismatches by fusing ordinal rank positions rather than raw prediction scores:
$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
where $M$ is the set of recommendation models, $r_m(d)$ is the ordinal rank of item $d$ in model $m$, and $k$ is a smoothing constant (typically $k=60$).

### 2.2 Recommender Evaluation and Ranking Metrics
The evaluation of recommendation algorithms has shifted from rating prediction error metrics (such as Root Mean Squared Error, RMSE) toward ranking quality metrics evaluated over top-$K$ recommendations [4].

#### 2.2.1 Top-K Ranking Quality Metrics
In hospitality e-commerce, users interact primarily with the top-ranked items presented on a search page. Consequently, recommendation models must be evaluated using top-$K$ ranking metrics:
- **Precision@K**: The proportion of recommended items in the top-$K$ list that are relevant to the user:
  $$\text{Precision@K} = \frac{|\text{Relevant Items} \cap \text{Top-K Recommended Items}|}{K}$$
- **Recall@K**: The proportion of all relevant items successfully retrieved within the top-$K$ recommendations:
  $$\text{Recall@K} = \frac{|\text{Relevant Items} \cap \text{Top-K Recommended Items}|}{|\text{Total Relevant Items}|}$$
- **Normalized Discounted Cumulative Gain (NDCG@K)**: Evaluates ranking quality by penalizing relevant items positioned lower in the recommendation list:
  $$\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}, \quad \text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$
  where $\text{IDCG@K}$ is the Ideal Discounted Cumulative Gain obtained by perfect relevance sorting.

Evaluating ranking quality via $\text{NDCG}@K$ provides a realistic measurement of recommender utility, as it reflects user browsing behavior far more accurately than offline rating error metrics.

### 2.3 Explainable Recommendation and Feature Interpretability
Providing transparent justifications for automated recommendations is essential for building user trust and supporting informed decision-making.

#### 2.3.1 Model-Agnostic vs. Analytical Explainability
Explainability approaches are broadly divided into post-hoc model-agnostic methods and deterministic analytical feature-matching methods:
- **SHAP (SHapley Additive exPlanations)**: A game-theoretic approach that computes feature importance values by evaluating marginal model predictions across feature subsets [5]. While mathematically rigorous, SHAP incurs prohibitive computational latency ($>1.5$ seconds per query) and produces non-deterministic, dense feature importance scores over rank-fused hybrid outputs that are difficult for non-technical users to interpret.
- **Analytical Feature-Matching Explainability**: Direct computation of aspect alignment scores between explicit user preference constraints and engineered entity feature vectors. Analytical explainers evaluate exact score overlaps across multi-dimensional feature categories, outputting transparent, deterministic alignment percentages and qualitative explanation badges without inference latency overhead.

### 2.4 Sentiment Analysis and Aspect-Based Sentiment Analysis (ABSA)
Unstructured traveler reviews contain rich qualitative feedback that overall star ratings cannot capture. Extracting structured sentiment signals requires sentence-level sentiment classification and Aspect-Based Sentiment Analysis (ABSA).

#### 2.4.1 Sentence-Level Sentiment Polarity
Modern natural language processing leverages pre-trained Transformer architectures, such as DistilBERT [6] and BERT [7], to classify sentence-level sentiment polarity. DistilBERT processes review text to output positive sentiment probabilities ($P_{\text{pos}} \in [0, 1]$), demonstrating high correlation with user star ratings.

#### 2.4.2 Aspect-Based Sentiment Analysis (ABSA) in Hospitality
While sentence sentiment captures general polarity, hospitality evaluation requires aspect-specific sentiment extraction [8]. Aspect-Based Sentiment Analysis decomposes review text into domain-specific aspect categories:
1. **Cleanliness**: Hygiene, room maintenance, and bathroom cleanliness.
2. **Service**: Front-desk responsiveness, check-in speed, and room service.
3. **Location**: Proximity to transit hubs, city center, and local attractions.
4. **Value for Money**: Price-to-quality ratio and perceived fairness.
5. **Staff Behavior**: Courtesy, friendliness, and helpfulness of property personnel.

ABSA systems utilize aspect-keyword masking combined with sentiment probability masking to assign independent scores ($S_{\text{aspect}} \in [0, 100]$) for each dimension. Empirically, Cleanliness exhibits the highest score variance among Delhi hotels, serving as a primary aspect differentiator in personalized recommendation matching.

### 2.5 Retrieval-Augmented Generation (RAG) Architecture
Retrieval-Augmented Generation (RAG) combines parametric knowledge stored within Large Language Models (LLMs) with non-parametric text retrieval over domain-specific document collections [9].

#### 2.5.1 Review Segmentation and Dense Vector Search
In a RAG framework, unstructured textual records are segmented into dense text chunks ($C_i$) and converted into fixed-dimensional vector embeddings using transformer models, such as SentenceTransformers (`all-MiniLM-L6-v2`, 384 dimensions) [10]. Dense vector indices compute cosine similarity scores between natural language user queries ($q$) and document chunk embeddings ($e_C$):
$$\text{Similarity}(q, C) = \frac{\mathbf{e}_q \cdot \mathbf{e}_C}{\|\mathbf{e}_q\| \|\mathbf{e}_C\|}$$

#### 2.5.2 Hybrid Retrieval Ablation and Metrics
Pure vector search often fails on queries containing explicit hard constraints (such as budget limits or specific geographic neighborhoods). Hybrid retrieval architectures address this by combining dense vector similarity search, SQL metadata filtering, and recommender trust score reranking. Retrieval performance is evaluated using standard information retrieval metrics: Precision@5, Recall@5, Mean Reciprocal Rank (MRR), and NDCG@5. Ablation studies demonstrate that adding metadata filtering and recommendation signal reranking to semantic vector search yields significant precision improvements ($\Delta \text{Precision} \approx +0.13$).

### 2.6 Grounded and Trustworthy Conversational AI
While RAG architectures enable conversational query interfaces, unconstrained LLM generation remains susceptible to hallucinations—generating plausible assertions unsupported by retrieved text chunks.

#### 2.6.1 Hallucination Mechanisms and Context Compression
LLM hallucinations in travel recommendation manifest primarily as unsupported amenity claims (e.g., asserting a budget property features a luxury spa or airport shuttle when no review evidence exists). Mitigating hallucinations requires strict prompt orchestration and token-budget context compression:
1. **Context Compression**: Deduplicating redundant review chunks and enforcing maximum token limits (e.g., 1,500 tokens) with explicit `[Chunk ID: XYZ]` markers.
2. **System-Prompt Grounding**: Enforcing strict system instructions mandating that the LLM restrict claims exclusively to facts present in the provided context markers.

#### 2.6.2 Citation Injection and Grounding Validation
To make LLM outputs fully verifiable, post-generation utility layers execute structured citation injection and automated grounding validation:
- **Citation Injector**: Post-processes raw textual LLM outputs, extracting inline chunk markers and mapping them to structured `ProvenanceChunk` JSON objects.
- **Grounding Validator**: Cross-references generated claims against retrieved review evidence chunks, actively intercepting and re-prompting responses containing unsupported assertions.

### 2.7 Vector Databases and Unified Database Storage Migration
Early RAG architectures store relational metadata in tabular CSV files and vector embeddings in file-based vector databases (such as ChromaDB).

#### 2.7.1 Limitations of Decoupled Vector Storage
Operating separate file-based vector stores alongside relational metadata leads to structural data drift, non-atomic updates, and a lack of ACID transaction guarantees. If relational metadata is modified without synchronous vector updates, similarity queries return stale or orphaned document chunks.

#### 2.7.2 Unified PostgreSQL 17.6 and pgvector Architecture
Migrating relational metadata and vector embeddings to a unified PostgreSQL 17.6 database server equipped with the `pgvector` extension resolves data drift. Storing 384-dimensional vector embeddings directly inside PostgreSQL tables (`embedding_documents`) enables single-transaction ACID operations across hotel attributes, scores, outbox events, and vector embeddings. Vector parity verification ensures $1.0000$ average cosine similarity parity between legacy file stores and `pgvector` instances.

### 2.8 Data Provenance and Reproducible Data Engineering
Enterprise recommendation platforms require auditable data lineage and safe, repeatable ingestion workflows.

#### 2.8.1 Canonical Hashing and Field-Level Diffing
To prevent destructive database overwrites and redundant embedding recalculations, repeatable ingestion pipelines compute SHA-256 canonical content hashes ($\text{Hash}_{\text{canonical}}$) over normalized record fields:
$$\text{Hash}_{\text{canonical}} = \text{SHA256}(\text{Name} \,\|\, \text{Address} \,\|\, \text{Rating} \,\|\, \text{AspectScores})$$
Field-level diff engines compare incoming canonical hashes against active database records, identifying explicit change sets (`INSERT`, `UPDATE`, `NO_CHANGE`).

#### 2.8.2 Dry-Run Safety and Selective Vector Synchronization
To guarantee data safety, ingestion pipelines enforce a strict multi-stage lifecycle:
$$\text{RAW} \rightarrow \text{NORM} \rightarrow \text{VAL} \rightarrow \text{DEDUP} \rightarrow \text{CANON} \rightarrow \text{DIFF} \rightarrow \text{DRY-RUN} \rightarrow \text{APPROVAL} \rightarrow \text{APPLY}$$
During `DRY-RUN`, diff reports (`dry_run.json`) are generated under unique run identifiers (`RUN_ID`) with zero database mutation. Executing an `APPLY` step requires explicit human approval specifying the valid `RUN_ID`. Following database update, selective vector synchronization recalculates embeddings *only* for records with modified content hashes, preserving vector database stability.

### 2.9 Research and Engineering Gap Summary
Prior literature and existing commercial platforms address recommendation algorithms, explainability models, RAG retrieval, and vector storage in isolation. However, a significant engineering gap remains in synthesizing these components into a unified, auditable platform. Specifically:
- Conventional recommenders lack real-time aspect explainability and review evidence grounding.
- Naive LLM-based RAG interfaces suffer from ungrounded hallucinations and lack citation provenance.
- File-based vector databases suffer from data drift and uncoordinated ingestion updates.

TrustLayer-AI addresses this research and engineering gap by integrating preference-aware Reciprocal Rank Fusion recommendation, real-time analytical aspect explainability, hybrid review evidence retrieval, automated post-generation grounding validation, unified PostgreSQL 17.6 + `pgvector` ACID storage, and a single-command CLI orchestrator with dry-run safety and live progress tracking into a single production platform.

---

## Chapter 3: Methodology and System Architecture

### 3.1 Overall System Methodology
TrustLayer-AI was engineered through an iterative 29-stage evolution to solve core challenges in recommendation quality, aspect explainability, conversational hallucination, vector store data drift, and data pipeline repeatability. Rather than assuming a static architecture from inception, the platform's methodology reflects empirical research discoveries and system engineering transitions.

The system spans five primary subsystems:
1. **Data Engineering Pipeline**: Upstream raw acquisition via external APIs, data cleaning, DistilBERT sentiment extraction, Aspect-Based Sentiment Analysis (ABSA), and canonical feature engineering.
2. **Hybrid Recommendation & Explainability Subsystem**: Collaborative filtering (SVD), content-based feature matching, Reciprocal Rank Fusion (RRF), and real-time analytical aspect alignment scoring.
3. **Conversational RAG & Grounding Subsystem**: Review evidence chunking, dense vector similarity retrieval, token-budget context compression, prompt orchestration, local LLM generation, citation injection, and post-generation grounding validation.
4. **Enterprise Database Infrastructure**: Clean Architecture repository abstraction layers managing unified relational and vector ACID transactions inside a PostgreSQL 17.6 database engine equipped with `pgvector`.
5. **Ingestion Engine & Master Orchestrator**: A 9-stage repeatable data ingestion engine featuring SHA-256 field-level diffing, dry-run safety, human approval boundaries, selective vector synchronization, and a single-command CLI master orchestrator with live terminal progress tracking and signal safety.

### 3.2 Data Acquisition
The data acquisition methodology focused on obtaining representative accommodation metadata and authentic guest reviews for the Delhi National Capital Region (NCR).

#### 3.2.1 Google Places API Data Collection
Primary hotel metadata and review text were collected using custom integration scripts (`fetch_google_places.py` and `fetch_google_reviews.py`). A geographic grid sampling approach across 15 major NCR area clusters (including central New Delhi, the Indira Gandhi International Airport corridor in Mahipalpur, Gurugram, Dwarka, Rohini, Paharganj, and Karol Bagh) yielded raw records for 1,661 distinct hotel properties.

For each property, the Places Details API retrieved place identifiers, property names, physical addresses, geographic coordinates (latitude and longitude), user rating averages, total rating counts, and text reviews. Due to API detail response limits, text review acquisition was capped at 5 reviews per hotel, yielding approximately 8,305 raw review entries. All raw payloads were preserved in `delhi_hotels_raw.csv` and `reviews_raw.csv` to establish an immutable acquisition baseline. Auditing raw data fields revealed that the Google Places API returned the `price_level` attribute as 100% missing (NaN) across all 1,661 hotels in India. Consequently, a proxy variable methodology was introduced during feature engineering to infer property budget tiers.

#### 3.2.2 Synthetic User Profile and Interaction Generation
To model user interactions in the absence of private commercial booking logs, a synthetic user generation engine (`generate_users.py`) created 500 demographic user profiles. Each profile incorporated explicit travel attributes, including budget category preferences, preferred area clusters, primary travel purpose (business, family, solo, leisure), and aspect priority weights.

Initial interaction generation (`generate_interactions.py`) simulated 5,000 user-item events (views, clicks, bookings). However, forensic evaluation in Stage A revealed that uniform random interaction assignment resulted in an extreme **99.27% matrix sparsity**, introducing unweighted random noise that severely degraded collaborative filtering performance. This prompted a major engineering remediation in Stage A.1 (`generate_interactions_v2.py`), which injected realistic preference matching (66% budget overlap, 51% area cluster overlap) and a power-law distribution of user interaction frequencies to accurately model real-world user activity.

### 3.3 Data Cleaning and Preparation
Raw collected data underwent rigorous sanitization via `clean_hotel_metadata.py` and `clean_reviews.py` to eliminate noise, standardize types, and enforce geographic constraints.

#### 3.3.1 Geographic Bounding Box and Deduplication
Hotels were deduplicated by canonical Google `place_id` keys and normalized property names. Geographic validity was enforced by passing coordinates through a spatial bounding-box filter defining the latitude/longitude limits of Delhi NCR ($28.40^\circ\text{N} \le \text{Lat} \le 28.88^\circ\text{N}$, $76.84^\circ\text{E} \le \text{Lng} \le 77.35^\circ\text{E}$). Out-of-bounds spatial outliers were pruned.

#### 3.3.2 Review Text Sanitization and Zero-Review Handling
Review text was sanitized using regular expressions to strip non-ASCII artifacts, HTML tags, and trailing whitespace. Text review auditing identified that 1,618 out of 1,661 hotels possessed non-empty text reviews, while 43 hotels had 0 reviews. To prevent entity dropouts, all 1,661 canonical hotels were preserved in the primary entity table, while the 43 zero-review properties were flagged for aspect score median imputation during feature engineering. Cleaned metadata and reviews were consolidated into `delhi_hotels_cleaned.csv` and `reviews_cleaned.csv`.

### 3.4 Sentiment Analysis and Aspect-Based Sentiment Analysis (ABSA)
To transform qualitative text reviews into structured quantitative signals, a two-stage NLP pipeline was implemented.

#### 3.4.1 Sentence-Level Sentiment Extraction
Review text sentiment polarity was computed using a pre-trained DistilBERT model (`distilbert-base-uncased-finetuned-sst-2-english`) in `analyze_sentiment.py`. For each review sentence, DistilBERT output a positive sentiment probability ($P_{\text{pos}} \in [0, 1]$). Evaluating sentiment probabilities against user star ratings demonstrated a high Pearson correlation ($r \approx 0.84$), confirming NLP extraction fidelity.

#### 3.4.2 Aspect-Based Sentiment Analysis (ABSA)
To extract granular sentiment across specific hospitality dimensions, `extract_absa_features.py` implemented an Aspect-Based Sentiment Analysis engine. Review text was parsed using keyword dictionary masking across five core aspects:
1. **Cleanliness**: Hygiene, room tidiness, and bathroom sanitation.
2. **Service**: Front-desk responsiveness, check-in efficiency, and room service.
3. **Location**: Accessibility to transit, airport corridors, and central attractions.
4. **Value for Money**: Perceived price-to-quality ratio.
5. **Staff Behavior**: Staff courtesy, helpfulness, and hospitality.

Aspect scores ($S_{\text{aspect}} \in [0, 100]$) were calculated by combining aspect-keyword frequency masking with DistilBERT sentence sentiment probabilities. Review-level aspect scores were aggregated to the hotel level using weighted mean pooling. Explanatory analysis across the dataset confirmed that **Cleanliness** exhibited the highest score variance among properties, establishing it as the primary differentiator for hotel quality in Delhi NCR.

### 3.5 Feature Engineering and Trust Scoring
Feature engineering (`engineer_features.py`) transformed cleaned metadata and aggregated NLP sentiment metrics into scaled numerical features.

#### 3.5.1 Feature Normalization and Budget Proxying
All numeric variables were scaled using `scikit-learn` `MinMaxScaler` ($X_{\text{scaled}} \in [0, 1]$). To address the 100% missing `price_level` attribute, a `budget_category` proxy feature (categorized as Budget, Mid-Range, or Luxury) was engineered by clustering property star ratings, review volumes, and geographic area tariffs. For the 43 zero-review hotels lacking ABSA sentiment scores, missing aspect values were imputed using the median aspect scores of their respective area clusters.

#### 3.5.2 Trust Score and Popularity Score Formulation
Two primary composite quality scores were engineered:
1. **Popularity Score ($P_{\text{score}}$)**: Derived from log-transformed total review counts:
   $$P_{\text{score}} = \frac{\log(1 + N_{\text{reviews}})}{\max(\log(1 + N_{\text{reviews}}))}$$
2. **Trust Score ($T_{\text{score}}$)**: A robust overall score combining normalized star rating ($R_{\text{norm}}$), DistilBERT positive sentiment probability ($S_{\text{sentiment}}$), and review density support ($V_{\text{support}}$):
   $$T_{\text{score}} = 0.50 \cdot R_{\text{norm}} + 0.35 \cdot S_{\text{sentiment}} + 0.15 \cdot V_{\text{support}}$$
   Rescaled to $[0, 100]$, $T_{\text{score}}$ exhibited a Gaussian distribution centered at $68.0$, whereas $P_{\text{score}}$ followed a steep power-law distribution. The near-zero correlation between Trust and Popularity ($r \approx 0.05$) confirmed that they capture orthogonal evaluation signals.

All features were merged into the canonical handoff dataset `final_hotel_dataset.csv` (1,661 hotels, 26 features, SHA-256: `eca959c788...`).

### 3.6 Recommendation Methodology and Engineering Pivots
Developing the recommendation system involved empirical evaluation and critical architectural remediations.

#### 3.6.1 Initial Model Development and Diagnostic Failure (Stage A)
Four candidate models were initially implemented in `scripts/recommender/`:
1. **Popularity Baseline**: Ranked hotels strictly by review volume and average rating.
2. **Content-Based (CB)**: Cosine similarity between user preference vectors and hotel feature vectors.
3. **Collaborative Filtering (CF)**: Matrix Factorization via SVD (`Surprise` library) over the user-item interaction matrix.
4. **Linear Hybrid Model**: Score-based linear blending: $S_{\text{hybrid}} = \alpha \cdot S_{\text{CF}} + (1-\alpha) \cdot S_{\text{CB}}$.

Diagnostic evaluation (`recommender_diagnostics.md`) revealed catastrophic model failure:
- Offline evaluation yielded abysmal metrics: $\text{Precision}@10 = 0.002$, $\text{Recall}@10 = 0.010$, $\text{NDCG}@10 = 0.006$.
- Grid-search optimization over the linear hybrid model selected $\alpha = 1.0$, completely disabling the content-based component.
- Matrix factorization (SVD) underfit heavily due to 99.27% interaction matrix sparsity (~3.6 interactions/hotel).
- Score calibration mismatch: Content-based cosine similarities clustered between $0.8$ and $0.9$, while SVD predicted ratings spread from $1.0$ to $5.0$. Linear blending over uncalibrated scales forced optimization to default to 100% CF dominance.

#### 3.6.2 Recommender Remediation and Reciprocal Rank Fusion (Stage A.1)
To resolve these failures, two major remediations were executed in `generate_interactions_v2.py` and `hybrid.py`:
1. **Synthetic Interaction Overhaul**: Regenerated interactions with structured preference overlap (66% budget match, 51% area match) and power-law interaction frequency.
2. **Reciprocal Rank Fusion (RRF)**: Replaced score-based linear blending with Reciprocal Rank Fusion ($k=60$):
   $$RRF\_Score(d) = \frac{1}{60 + r_{\text{CF}}(d)} + \frac{1}{60 + r_{\text{CB}}(d)}$$
   RRF fuses ordinal item ranks rather than raw uncalibrated scores, completely bypassing score calibration mismatches.

Re-evaluation demonstrated dramatic improvement, elevating $\text{NDCG}@10$ from $0.006$ to $> 0.12$ and passing recommendation quality gates.

### 3.7 Explainability Methodology
To provide transparent justifications for recommendations, explainability mechanisms were developed in `scripts/explainability/`.

#### 3.7.1 Abandonment of SHAP Approximations
Initial designs explored SHAP (SHapley Additive exPlanations) to interpret tree-based and collaborative models. However, empirical benchmarking forced the abandonment of SHAP due to two factors:
1. **Computational Latency**: SHAP value calculations required $> 1.5$ seconds per recommendation query, violating real-time API latency requirements ($< 500$ ms).
2. **Dense Non-Deterministic Attribution**: SHAP attributions generated over RRF rank-fused outputs produced complex, non-intuitive importance scores that failed human readability audits.

#### 3.7.2 Analytical Feature-Matching Explainer
SHAP was replaced by a real-time, deterministic **Analytical Feature-Matching Explainer** (`explainer.py`). For a target user preference vector and recommended hotel, the explainer calculates direct aspect alignment percentages across Cleanliness, Service, Location, Value, and Staff Behavior:
$$\text{Alignment}_{\text{aspect}} = 100 \cdot \left(1 - |W_{\text{user, aspect}} - S_{\text{hotel, aspect}}|\right)$$
The explainer outputs structured aspect alignment breakdown bars and qualitative explanation badges (e.g., *"Top Cleanliness Match in Mahipalpur"*), delivering deterministic, human-readable explanations in $< 5$ ms.

### 3.8 Retrieval-Augmented Generation (RAG) Methodology
To enable natural language conversational search, a grounded Hybrid RAG architecture was constructed (`app/services/`).

#### 3.8.1 Review Document Chunking and Segmentation
The 1,661 canonical hotels were segmented into **7,910 review evidence text chunks** (`data/rag/ChIJ*.json`). Each chunk captured specific document types: Chunk A (Property Profile), Chunk B (Aspect Summaries), Chunk C (Positive Review Evidence), Chunk D (Negative Review Evidence), and Chunk E (Recommender Ranking Signals). Chunks were embedded into 384-dimensional vector representations using SentenceTransformers (`all-MiniLM-L6-v2`).

#### 3.8.2 End-to-End RAG Execution Flow
Conversational queries execute through an 8-stage pipeline:
1. **Query Parsing (`query_parser.py`)**: Extracts natural language intent, budget limits, preferred area clusters, and requested amenities.
2. **Hybrid Retrieval (`retriever.py`)**: Combines vector cosine similarity search over review chunks, hard SQL metadata filtering (area, budget), and recommender trust score reranking.
3. **Context Compression (`context_compressor.py`)**: Deduplicates overlapping chunks and enforces a strict 1,500-token budget, formatting chunks with explicit `[Chunk ID: XYZ]` markers.
4. **Prompt Orchestration (`prompt_orchestrator.py`)**: Wraps compressed context in task-specific system prompts containing mandatory grounding instructions.
5. **LLM Generation (`llm_service.py`)**: Executes local Ollama inference (`mistral`/`llama3`) supporting synchronous responses and HTTP chunked streaming (`async stream_generate`).
6. **Citation Injection (`citation_injector.py`)**: Parses inline chunk citations from raw LLM text into structured `ProvenanceChunk` JSON models.
7. **Grounding Validation (`grounding_validator.py`)**: Cross-references LLM claims against retrieved evidence, actively stripping unverified amenity assertions.
8. **Frontend Delivery**: Delivers structured responses to the UI, enabling lazy-loading of provenance drawers.

Grounding evaluation over 150 benchmark queries achieved a **96.7% grounded response rate** and a **1.3% hallucination rate**, with 3 active interceptions stripping fabricated amenity claims.

### 3.9 Vector Retrieval Evolution and PostgreSQL Migration
Managing vector embeddings evolved from decoupled file stores to unified relational storage.

#### 3.9.1 Initial ChromaDB Architecture and Data Drift
In Stage C, vector embeddings were stored in a file-based ChromaDB database (`data/vector_store/`). While functional for initial retrieval testing, operating ChromaDB alongside raw CSV files introduced structural data drift, non-atomic schema updates, and a lack of ACID transaction guarantees.

#### 3.9.2 PostgreSQL 17.6 + pgvector Cutover (Stage 24.2)
To unify relational metadata and vector embeddings under a single ACID-compliant database, the system migrated to PostgreSQL 17.6 with the `pgvector` extension in Stage 24.2. All 7,910 embedding chunks were backfilled into the `embedding_documents` SQL table (`backfill_pgvector.py`).

Empirical parity verification demonstrated:
- **Embedding Vector Parity**: **1.0000 average cosine similarity** between ChromaDB and `pgvector` embeddings across 100 sampled vectors ($0.0000$ max absolute difference).
- **RAG Query Parity**: **20 / 20 (100.0%) Top-1 hotel match** across 20 benchmark recommendation queries comparing legacy file stores against PostgreSQL.

PostgreSQL 17.6 was established as the sole runtime source of truth.

### 3.10 PostgreSQL Data Architecture
The production PostgreSQL database (`trustlayer_db`) enforces a normalized relational schema comprising nine tables:
- `hotels`: Master entity table (1,661 rows; primary key `id`, property metadata, content hash, active flag).
- `hotel_locations`: Geographic coordinates and area cluster assignments (1,661 rows).
- `hotel_scores`: Engineered Trust Score, Popularity Score, and 5 ABSA aspect scores (1,661 rows).
- `hotel_sources`: External Google Place references and data URLs (1,661 rows).
- `hotel_amenities`: Boolean amenity indicators (wifi, parking, pool, restaurant, ac, bar, gym, spa; 1,661 rows).
- `embedding_documents`: Vector storage (7,910 rows; chunk ID, hotel FK, content text, `vector(384)`, metadata JSONB, content hash).
- `domain_events`: Transactional outbox pattern table recording domain state changes (`HOTEL_CREATED`, `HOTEL_UPDATED`; 1,661 rows).
- `ingestion_runs` & `ingestion_records`: Auditable ingestion run logs and record-level action histories.

SQL foreign key constraints enforce zero orphan child records across the database.

### 3.11 Repository Abstraction and Backend Architecture
To prevent coupling API routes directly to SQL queries, Stage 23 refactored the backend using the Clean Architecture Repository Pattern (`app/repositories/`). Abstract base contracts (`BaseHotelRepository`, `BaseEmbeddingRepository`, `BaseTraceRepository`) define data access methods. Concrete SQLAlchemy repository adapters (`PostgresHotelRepository`, `PgVectorEmbeddingRepository`, `PostgresTraceRepository`) handle database execution. Centralized configuration in `app/config/config.py` dynamically resolves active repositories based on environment flags (`DATA_BACKEND=postgres`, `VECTOR_BACKEND=pgvector`). FastAPI service layers (`HotelService`, `RecommendationService`) consume abstract repository interfaces, ensuring clean separation of concerns.

### 3.12 Repeatable Data Ingestion Methodology (Stage 26)
Stage 26 built an auditable, repeatable data ingestion engine to eliminate manual SQL updates and redundant embedding recalculations. The engine executes a 9-stage lifecycle:
1. `RAW`: Ingest source CSV files into staging memory.
2. `NORMALIZED`: Standardize types, strings, and coordinates.
3. `VALIDATED`: Enforce `schema_contract.py` bounds (ratings $[0..5]$, trust scores $[0..100]$, valid lat/long).
4. `DEDUPLICATED`: Prune duplicate entity keys.
5. `CANONICAL`: Update master dataset (`final_hotel_dataset.csv`).
6. `DIFF`: Execute `diff_engine.py` using canonical content hashing (`calculate_canonical_content_hash`).
7. `DRY-RUN`: Produce `dry_run.json` diff artifact detailing `INSERT`, `UPDATE`, and `NO_CHANGE` counts with **ZERO** PostgreSQL mutation.
8. `APPROVAL`: Require explicit human approval specifying the generated `RUN_ID`.
9. `TRANSACTIONAL APPLY`: Open a SQL transaction, apply database updates, log outbox events, and invoke `selective_vector_sync.py` to recompute embeddings *only* for modified content hashes.

### 3.13 Master Pipeline Orchestration and Progress Tracking (Stages 28 & 29)
Stages 28 and 29 unified all data pipeline processes into a single production CLI orchestrator.

#### 3.13.1 One-Command CLI Orchestrator (Stage 28)
Stage 27 identified that upstream data processing (collection, cleaning, NLP, ABSA, feature engineering, merging) was fragmented across standalone scripts. Stage 28 resolved this by building `scripts/orchestrator.py`:
- `python -m scripts.orchestrator full`: Sequentially triggers all 6 upstream pipeline stages, generates `final_hotel_dataset.csv`, and executes Stage 26 dry-run diffing under `data/runs/<RUN_ID>/` while maintaining strict database read-only safety.
- `python -m scripts.orchestrator apply --run-id <RUN_ID>`: Enforces human approval before executing SQL transactions.

#### 3.13.2 Live Progress Tracking and Signal Safety (Stage 29)
Stage 29 integrated `ProgressTracker` (`scripts/orchestration/progress.py`), adding an interactive ASCII terminal progress dashboard rendering active stage names, script entrypoints, record percentage bars, elapsed time, and ETA calculations, alongside file logging (`pipeline.log`). A custom `SIGINT` (Ctrl+C) signal handler safely terminates active sub-processes, marks `pipeline_manifest.json` as `INTERRUPTED`, and guarantees zero database corruption.

### 3.14 Experimental Methodology
The project employed distinct experimental and verification suites:
- **Offline Recommender Benchmarking**: Evaluated SVD, Content-Based, and RRF Hybrid models across Precision@10, Recall@10, and NDCG@10 using 70/30 chronological train/test splits.
- **Retrieval Ablation & Evaluation**: Evaluated hybrid vector search over 150 benchmark queries across Precision@5, Recall@5, MRR, and NDCG@5.
- **Grounding & Hallucination Auditing**: Audited LLM response generation over 150 benchmark queries, quantifying interception rates via `GroundingValidator`.
- **Database & Vector Parity Verification**: Validated cosine similarity parity ($1.0000$) and SQL relational integrity via direct SQLAlchemy queries.
- **Master Provenance Verification**: Executed master Pytest verification suites (`test_stage24_5_complete_backend.py`, `test_pipeline_stage26.py`, `test_stage28_orchestrator.py`, `test_stage29_progress.py`), achieving a 100% pass rate across all 50 backend tests.

### 3.15 End-to-End Operational Lifecycle
In summary, raw external data acquired from Google Places APIs is sanitized, enriched with DistilBERT sentiment and ABSA aspect scores, and merged into a canonical handoff dataset. A single-command orchestrator computes SHA-256 diffs against PostgreSQL 17.6, allowing approved transactional updates and selective vector synchronization. When users submit natural language queries, the FastAPI backend resolves abstract repository interfaces against PostgreSQL/pgvector storage, executes RRF hybrid ranking, generates aspect-alignment explanations in real time, and passes retrieved review evidence chunks through a grounded RAG generation loop. The resulting response is validated against hallucinations and rendered dynamically in the React frontend.

---

## Chapter 4: Experimental Evaluation and Results

### 4.1 Experimental Evaluation Overview
The evaluation of TrustLayer-AI was conducted across distinct empirical phases spanning model diagnostics, information retrieval ablation, natural language grounding validation, database storage parity checks, data pipeline integrity verification, and master backend provenance testing. 

Rather than assuming ideal system execution from inception, the project followed an iterative, evidence-driven evaluation paradigm. Empirical findings from early stages directly triggered major architectural remediations, including overhauling interaction modeling, switching to Reciprocal Rank Fusion (RRF), abandoning high-latency SHAP explainers in favor of analytical feature matching, and migrating file-based stores to an enterprise PostgreSQL 17.6 + `pgvector` database.

### 4.2 Dataset and Data Processing Results
Data acquisition and cleaning yielded verified statistical metrics across Delhi NCR properties:
- **Raw Property Acquisition**: 1,661 distinct hotel entities collected via the Google Places Details API across 15 major area clusters.
- **Raw Text Reviews**: 8,305 raw text review records acquired, reflecting the Google Places Detail API request limit of 5 reviews per property.
- **Cleaned Metadata and Reviews**: 1,661 hotels preserved after geographic bounding-box filtering ($28.40^\circ\text{N} \le \text{Lat} \le 28.88^\circ\text{N}$, $76.84^\circ\text{E} \le \text{Lng} \le 77.35^\circ\text{E}$). 1,618 hotels contained non-empty text reviews, while 43 hotels had 0 reviews.
- **Canonical Handoff Dataset**: `final_hotel_dataset.csv` established with 1,661 hotels and 26 engineered feature columns (SHA-256: `eca959c788d9535feea5ed1b11efb249988c60b6bfb7b4bb41ef33e50bad1e2e`).
- **Synthetic User Profiles**: 500 demographic user preference profiles generated with budget, area, travel purpose, and aspect priority attributes.
- **Review Evidence Segmentation**: 7,910 text chunks generated across Chunk Types A (Profile), B (Aspects), C (Positive Evidence), D (Negative Evidence), and E (Recommender Signals).

Geographic clustering confirmed that hotels are heavily concentrated in central New Delhi (Paharganj and Karol Bagh, 216 properties), the Indira Gandhi International Airport corridor (Mahipalpur, 56 properties), and Gurugram (39 properties). The 100% missing `price_level` attribute returned by the Places API was successfully mitigated by engineering a `budget_category` proxy feature based on area cluster tariffs and rating tiers.

### 4.3 Sentiment Analysis and ABSA Results
NLP evaluation validated sentence-level sentiment extraction and multi-dimensional aspect scoring:
- **DistilBERT Sentiment Polarity**: Sentence-level positive sentiment probabilities ($P_{\text{pos}}$) extracted via DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`) demonstrated a high Pearson correlation coefficient of **$r \approx 0.84$** against user star ratings, validating NLP sentiment extraction quality.
- **Aspect-Based Sentiment Distributions**: ABSA scores ($S_{\text{aspect}} \in [0, 100]$) evaluated across Cleanliness, Service, Location, Value for Money, and Staff Behavior revealed that **Cleanliness** exhibited the highest score variance across Delhi NCR properties, establishing it as the key aspect differentiator for hotel selection.

### 4.4 Trust and Feature Engineering Results
Feature engineering produced two orthogonal quality indicators:
1. **Trust Score ($T_{\text{score}}$)**: Combining normalized star rating, DistilBERT sentiment probability, and review volume support produced a Gaussian distribution centered at $68.0$ (range $0$ to $100$).
2. **Popularity Score ($P_{\text{score}}$)**: Log-transformed review volume yielded a steep power-law distribution.

Evaluating the correlation between Trust Score and Popularity Score yielded **$r \approx 0.05$**, proving that Trust and Popularity represent independent evaluation signals. A hotel with modest review volume can achieve a high Trust Score if its guest reviews exhibit consistently high sentiment and aspect ratings.

### 4.5 Initial Recommendation System Diagnostic Failure (Stage A)
Offline evaluation of the initial recommender algorithms in Stage A (`recommender_diagnostics.md`) uncovered severe performance degradation:
- **Precision@10**: $0.002$
- **Recall@10**: $0.010$
- **NDCG@10**: $0.006$

These values were barely above random chance, triggering a formal **NO-GO** decision for downstream deployment. Diagnostic investigation identified three root causes:
1. **Extreme Matrix Sparsity**: The initial user-item interaction matrix (500 users, 1,379 hotels, 5,000 interactions) exhibited a **99.27% matrix sparsity** (~3.6 interactions/hotel). Collaborative filtering via SVD underfit heavily, failing to learn latent factors and reverting to predicting global item biases.
2. **Score Calibration Mismatch**: Content-based cosine similarities clustered densely between $0.8$ and $0.9$, while SVD predicted ratings spread from $1.0$ to $5.0$. Grid-search optimization over the linear hybrid model ($\alpha \cdot S_{\text{CF}} + (1-\alpha) \cdot S_{\text{CB}}$) selected $\alpha = 1.0$, completely disabling the content-based component.
3. **Evaluation Script Reporting Flaw**: Auditing `evaluate_recommenders.py` revealed that narrative text claiming Content-Based filtering outperformed Collaborative Filtering on cold-start users was statically hardcoded. User-level 70/30 chronological splitting over fixed 10-interaction profiles left exactly **0 cold-start users** in the test set.

### 4.6 Recommendation System Remediation and RRF Results (Stage A.1)
To resolve these failures, two major remediations were executed in Stage A.1 (`recommender_remediation_report.md`):
1. **V2 Synthetic Interaction Generation**: Regenerated user interactions (`generate_interactions_v2.py`) with realistic preference overlap (66% budget match, 51% area match) and power-law interaction frequencies.
2. **Reciprocal Rank Fusion (RRF)**: Replaced linear score blending with Reciprocal Rank Fusion ($k=60$). RRF combines ordinal item ranks rather than raw prediction scores, eliminating score calibration mismatches.

Re-evaluation demonstrated dramatic ranking quality recovery, elevating **$\text{NDCG}@10$ from $0.006$ to $> 0.12$**, balancing catalog coverage, and securing a formal **GO** decision.

### 4.7 Explainability Evaluation
Evaluating explainability mechanisms highlighted significant performance trade-offs:
- **SHAP Evaluation**: Initial SHAP value calculations incurred severe computational latency ($> 1.5$ seconds per query) and produced dense, non-deterministic feature importance scores over RRF rank-fused outputs that failed human readability audits.
- **Analytical Feature-Matching Explainer**: Replacing SHAP with an analytical explainer (`explainer.py`) enabled direct computation of aspect alignment scores across Cleanliness, Service, Location, Value, and Staff Behavior in **$< 5$ ms**. Auditing over 100 sample user profiles passed 100% of logic and readability checks.

### 4.8 RAG Retrieval Evaluation and Ablation
Hybrid retrieval evaluation over 150 benchmark queries (`retrieval_evaluation.md`) validated dense vector retrieval, metadata filtering, and recommender reranking against success gates.

**Table 4.1: RAG Retrieval Ablation Study across 150 Benchmark Queries**

| Retrieval Configuration | Precision@5 | Recall@5 | MRR | NDCG@5 |
| :--- | :---: | :---: | :---: | :---: |
| Semantic Vector Only | 0.68 | 0.65 | 0.70 | 0.71 |
| + Metadata Filtering | 0.75 | 0.73 | 0.78 | 0.79 |
| + Recommendation Reranking | 0.73 | 0.70 | 0.75 | 0.76 |
| **Full Hybrid Retrieval** | **0.81** | **0.79** | **0.83** | **0.85** |
| **Target Threshold** | $\ge 0.70$ | $\ge 0.70$ | $\ge 0.75$ | $\ge 0.75$ |
| **Status** | **PASS** | **PASS** | **PASS** | **PASS** |

Ablation analysis proved that adding hard metadata filtering contributed $+0.07$ to Precision@5, while recommender reranking contributed an additional $+0.05$, achieving a final Precision@5 of **0.81**. The total retrieval latency breakdown was measured as: Embedding Generation (12.4 ms), ChromaDB Search (145.2 ms), Metadata Filtering (2.1 ms), Reranking (4.3 ms), and Context Assembly (1.8 ms), totaling **165.8 ms**.

### 4.9 Grounding and Hallucination Evaluation
Evaluating the RAG answer generation pipeline and `GroundingValidator` across 150 benchmark queries (`stage_d_evaluation.md`) yielded verified reliability metrics:
- **Grounded Response Rate**: **96.7%** (Target $\ge 95\%$) — PASS
- **Hallucination Rate**: **1.3%** (Target $\le 2\%$) — PASS
- **Explanation Consistency**: **96.0%** (Target $\ge 95\%$) — PASS
- **Provenance Coverage**: **98.7%** (Target $\ge 95\%$) — PASS
- **Active Interceptions**: `GroundingValidator` actively intercepted **3 responses** containing fabricated amenity assertions (e.g., claiming a budget hotel featured a luxury spa), stripping ungrounded text and triggering context re-prompting.
- **Cache Performance**: Cache Miss Latency = $210.0$ ms | Cache Hit Latency = $12.0$ ms.

### 4.10 ChromaDB -> PostgreSQL/pgvector Migration Results (Stage 24.2)
Stage 24.2 backfilled all 7,910 review chunks into PostgreSQL 17.6 `pgvector` storage (`STAGE24.2_PGVECTOR_BACKFILL_REPORT.md`). Controlled dual-backend verification demonstrated:
- **Embedding Cosine Similarity Parity**: Sampling 100 random vectors across ChromaDB and `pgvector` yielded an **average cosine similarity of 1.0000** ($0.0000$ max absolute difference across 384 dimensions).
- **20-Query RAG Parity**: Evaluating 20 recommendation queries comparing legacy file stores against PostgreSQL achieved **20 / 20 (100.0%) Top-1 hotel match** and **100% Top-5 candidate overlap**.

### 4.11 PostgreSQL Relational Integrity Results (Stage 24.5)
Master provenance auditing (`STAGE24.5_COMPLETE_BACKEND_FORENSIC_VERIFICATION_REPORT.md`) verified direct SQL query counts in the production PostgreSQL database (`trustlayer_db`):
- `hotels`: **1,661 rows**
- `hotel_locations`: **1,661 rows**
- `hotel_scores`: **1,661 rows**
- `hotel_sources`: **1,661 rows**
- `hotel_amenities`: **1,661 rows**
- `embedding_documents`: **7,910 rows**
- `domain_events`: **1,661 rows** (Transactional outbox events)
- `ingestion_records`: **1,661 rows**
- `ingestion_runs`: **1 row**

Relational checks confirmed **0 orphan records** across child tables and **0 duplicate primary keys**, validating complete legacy file detachment.

### 4.12 Stage 26 Ingestion Results
Evaluating the repeatable ingestion pipeline (`STAGE26_REPEATABLE_DATA_PIPELINE_REPORT.md`) resulted in an **8 / 8 PASS** result in Pytest (`test_pipeline_stage26.py`). Key verification evidence:
- **Schema Contract Enforcement**: Validated numeric rating bounds $[0..5]$ and trust score bounds $[0..100]$.
- **Dry-Run Safety**: `pipeline.py dry-run` generated `dry_run.json` diff reports with **ZERO** PostgreSQL mutation.
- **Approval Protection**: Apply execution strictly rejected stale or invalid `RUN_ID` parameters.
- **Selective Vector Synchronization**: Recalculate embeddings *only* for modified content hashes, skipping redundant vector operations.

### 4.13 Stage 28 Master Orchestration Results
Evaluating the single-command CLI orchestrator (`STAGE28_FINAL_REPORT.md`) passed **6 / 6 tests** (`test_stage28_orchestrator.py`). Executing `python -m scripts.orchestrator full` sequentially triggered all 6 upstream stages, generated `final_hotel_dataset.csv` (1,661 rows, 26 features), and created `dry_run.json` under `data/runs/<RUN_ID>/` while maintaining PostgreSQL read-only safety. Executing `apply --run-id <RUN_ID>` verified dataset SHA-256 hashes before opening SQL transactions.

### 4.14 Stage 29 Live Progress Results
Stage 29 verification (`STAGE29_LIVE_PROGRESS_REPORT.md`) passed **4 / 4 tests** (`test_stage29_progress.py`). The `ProgressTracker` engine successfully rendered an interactive ASCII terminal progress dashboard showing active stage names, record percentage bars, elapsed execution time, and ETA calculations, outputting structured logs to `pipeline.log`. Emitting a `SIGINT` (Ctrl+C) signal cleanly terminated active sub-processes, marked `pipeline_manifest.json` as `INTERRUPTED`, and guaranteed zero database corruption.

### 4.15 Master Backend Automated Testing Results
The entire backend test suite achieved a **50 / 50 PASSED (100%)** result across all Pytest suites under tested conditions:
- **Stage 29 Progress Suite**: **4 / 4 PASSED** (`test_stage29_progress.py`)
- **Stage 28 Orchestration Suite**: **6 / 6 PASSED** (`test_stage28_orchestrator.py`)
- **Stage 26 Ingestion Suite**: **8 / 8 PASSED** (`test_pipeline_stage26.py`)
- **Stage 24.5 Provenance Suite**: **18 / 18 PASSED** (`test_stage24_5_complete_backend.py`)
- **API, Context & Grounding Suite**: **14 / 14 PASSED** (`test_api_endpoints.py`, etc.)

### 4.16 Jupyter Research Notebook Experimental Findings & Built-in Visualizations
The 10 Jupyter research notebooks (`research/notebooks/`) provided essential analytical evidence throughout system development. Key figures extracted from `research/reports/figures/` and `research/reports/images/` capture the empirical behavior of each stage:

#### 4.16.1 Notebook 01: Hotel Metadata Analysis
- **Geographic Spatial Density**: Mapped 1,661 hotels across Delhi NCR. High property density is concentrated in Central Delhi (Paharganj & Karol Bagh: 216 hotels), airport transit hubs (Mahipalpur: 56 hotels), and commercial centers (Gurugram: 39 hotels).
- **Missing Value Discovery**: Audit confirmed `price_level` was 100% missing (NaN) across all Google Places API payloads in India, motivating the proxy budget classification model.

![Figure 4.1: Geographic Hotel Map across Delhi NCR Cluster Regions](../../research/reports/figures/01_hotel_map.png)

![Figure 4.2: Audit of Missing Attribute Values in Raw Google Places Payloads](../../research/reports/figures/01_missing_values.png)

![Figure 4.3: Distribution of Hotel Ratings and Review Counts](../../research/reports/figures/01_ratings_reviews.png)

![Figure 4.4: Top Geographic Area Clusters by Property Volume](../../research/reports/figures/01_top_areas.png)

#### 4.16.2 Notebook 02: Review Analysis
- **Positivity Skew**: Guest ratings exhibited a strong positive skew (median rating 4.10).
- **API Response Truncation**: Google Places Details API capped text review retrieval at 5 reviews per property (8,305 total reviews).

![Figure 4.5: Review Text Sentence Length Distribution](../../research/reports/figures/02_review_length.png)

![Figure 4.6: Distribution of Ratings Across Collected Reviews](../../research/reports/figures/02_review_ratings.png)

![Figure 4.7: Review Count Per Hotel Property (Capped at 5)](../../research/reports/figures/02_reviews_per_hotel.png)

![Figure 4.8: Temporal Distribution of Guest Reviews Across Years](../../research/reports/figures/02_temporal_years.png)

#### 4.16.3 Notebook 03: Sentiment Analysis
- **DistilBERT Extraction**: Sentence sentiment probabilities ($P_{\text{pos}}$) extracted via DistilBERT correlated strongly ($r \approx 0.84$) with star ratings.

![Figure 4.9: DistilBERT Positive Sentiment Probability Distribution](../../research/reports/figures/03_positive_prob_dist.png)

![Figure 4.10: Categorical Sentiment Label Counts](../../research/reports/figures/03_sentiment_labels.png)

![Figure 4.11: Correlation Scatter Plot of Sentiment Probability vs. Star Rating](../../research/reports/figures/03_sentiment_vs_rating.png)

#### 4.16.4 Notebook 04: Aspect-Based Sentiment Analysis (ABSA)
- **Aspect Score Variance**: Cleanliness exhibited the highest inter-property score variance, making it the dominant factor in personalized ranking differentiation.

![Figure 4.12: Aspect Score Distributions across Cleanliness, Service, Location, Value, and Staff](../../research/reports/figures/04_aspect_boxplots.png)

![Figure 4.13: Inter-Aspect Score Correlation Matrix Heatmap](../../research/reports/figures/04_aspect_correlation.png)

#### 4.16.5 Notebook 05: Feature Engineering & Trust Scoring
- **Trust vs. Popularity**: $T_{\text{score}}$ (Gaussian, mean 68.0) and $P_{\text{score}}$ (power-law) exhibited zero correlation ($r \approx 0.05$), proving they provide independent quality signals.

![Figure 4.14: Correlation Matrix of Engineered Feature Variables](../../research/reports/figures/05_engineered_correlations.png)

![Figure 4.15: Trust Score Gaussian vs. Popularity Score Power-Law Distributions](../../research/reports/figures/05_engineered_scores.png)

![Figure 4.16: Trust Score Distribution Segmented by Property Budget Category](../../research/reports/figures/05_trust_by_budget.png)

#### 4.16.6 Notebook 06: Synthetic User Dataset Analysis
- **User Preference Auditing**: Demographic analysis over 500 synthetic user profiles verified target distributions for budget preferences, travel purpose, and preferred amenity filters.

![Figure 4.17: Synthetic User Preferred Amenity Distribution](../../research/reports/figures/06_user_amenities.png)

![Figure 4.18: Demographic Distribution across 500 Synthetic User Profiles](../../research/reports/figures/06_user_demographics.png)

#### 4.16.7 Notebook 07 & 10: Interaction Matrix & Remediation Analysis
- **Sparsity & Remediation Audit**: Exposed 99.27% matrix sparsity in V1 interactions. Audited V2 interactions, confirming preference overlap injection (66% budget, 51% area match) that restored SVD and RRF hybrid recommender performance.

![Figure 4.19: Interaction Types Distribution (Views, Clicks, Bookings)](../../research/reports/figures/07_interaction_types.png)

![Figure 4.20: Interaction Density per User and Hotel (Matrix Sparsity Audit)](../../research/reports/figures/07_interactions_per_user_hotel.png)

![Figure 4.21: User Activity Level Distribution Histogram](../../research/reports/images/activity_hist.png)

![Figure 4.22: User-Hotel Preference Alignment Score Distribution](../../research/reports/images/alignment.png)

![Figure 4.23: Hotel Interaction Popularity Distribution](../../research/reports/images/hotel_pop.png)

#### 4.16.8 Notebook 08: Master Final Dataset Overview
- **Dataset Handoff Verification**: Confirmed master canonical dataset integrity (1,661 hotels, 26 feature columns, zero missing values post-imputation).

![Figure 4.24: Global Feature Correlation Heatmap for Canonical Handoff Dataset](../../research/reports/figures/08_global_correlation.png)

![Figure 4.25: Missing Value Audit Heatmap Post-Imputation](../../research/reports/figures/08_missing_heatmap.png)

### 4.17 End-to-End System Results
In the final production backend, executing user requests through FastAPI REST endpoints (`/api/v1/recommend`, `/api/v1/chat`, `/api/v1/hotel/{id}/explanation`) resolved queries against PostgreSQL 17.6 + `pgvector` in **210.0 ms cache miss latency** and **12.0 ms cache hit latency**.

### 4.18 Limitations and Experimental Caveats
The system's empirical findings operate under the following documented constraints:
- **Google Places API Review Cap**: External API detail requests cap reviews at 5 per property, limiting long-tail review volume analysis.
- **Missing Price Attribute**: Google Places API returned 100% missing `price_level` data, requiring engineered `budget_category` proxies.
- **Synthetic Interaction Modeling**: User interaction matrices were synthetically generated (V2 preference overlap model) rather than captured from live commercial transaction logs.
- **Local Execution Scope**: Local LLM inference (`mistral`/`llama3`) and PostgreSQL database deployments were evaluated on single-host developer infrastructure.

### 4.19 Final Evaluation Summary

**Table 4.2: Final Verification Summary across TrustLayer-AI System Components**

| Component | Evaluation Method | Verified Empirical Result | Status |
| :--- | :--- | :--- | :---: |
| Data Pipeline | Dataset Integrity Audit | 1,661 Hotels, 7,910 Chunks, SHA-256 Verified | PASS |
| Sentiment / ABSA | DistilBERT | $r \approx 0.84$ Rating Correlation; Cleanliness Differentiator | PASS |
| Initial Recommender | Offline Benchmark (Stage A) | $\text{NDCG}@10 = 0.006$; SVD Underfitting ($\alpha=1.0$) | FAIL |
| Remediated Recommender | RRF Rank Fusion (Stage A.1) | $\text{NDCG}@10 > 0.12$; Calibration Mismatch Resolved | PASS |
| Explainability | Analytical Explainer | $< 5$ ms Latency; 100% Readability Audit Pass | PASS |
| RAG Retrieval | 150-Query Benchmark | Precision@5 = 0.81, Recall@5 = 0.79, MRR = 0.83 | PASS |
| Grounding Validator | 150-Query Audit | 96.7% Grounded Rate, 1.3% Hallucination Rate | PASS |
| PostgreSQL / pgvector | Dual-Backend Parity | 1.0000 Cosine Sim Parity, 100% Top-1 RAG Match | PASS |
| Repeatable Ingestion | Stage 26 Pytest Suite | 8 / 8 PASSED; Dry-Run Safety Verified | PASS |
| Master Orchestrator | Stage 28 Pytest Suite | 6 / 6 PASSED; One-Command CLI Verified | PASS |
| Progress | Stage 29 Pytest Suite | 4 / 4 PASSED; Live ASCII & Ctrl+C Safety Verified | PASS |
| Master Backend Suite | Complete Pytest Suite | 50 / 50 PASSED (100% Suite Verification) | PASS |

---

## Chapter 5: Conclusion and Future Work

### 5.1 Project Summary
This Independent Project presented **TrustLayer-AI**, a preference-aware, explainable hybrid hotel recommendation and grounded Retrieval-Augmented Generation (RAG) platform. Developed through an iterative 29-stage evolution, the project addressed critical usability, explainability, hallucination, vector store data drift, and pipeline repeatability challenges inherent in modern automated travel systems.

The engineering trajectory evolved through distinct system phases:
1. **Data Ingestion & NLP Pipeline (Stages 1--4)**: Raw property metadata and traveler text reviews for 1,661 hotels across 15 Delhi NCR area clusters were acquired via Google Places APIs. Text reviews were parsed using pre-trained DistilBERT models to extract sentence-level sentiment probabilities ($r \approx 0.84$ with ratings) and compute 5-dimensional Aspect-Based Sentiment Analysis (ABSA) scores across Cleanliness, Service, Location, Value, and Staff Behavior. Features were scaled alongside an engineered Gaussian Trust Score (mean $68.0$) into a canonical handoff dataset (`final_hotel_dataset.csv`).
2. **Recommendation & Remediation (Stages 5--6.1)**: Initial collaborative filtering (SVD) experiments suffered a diagnostic failure ($\text{NDCG}@10 = 0.006$) due to 99.27% matrix sparsity and unweighted synthetic interaction noise. Furthermore, linear score blending collapsed to single-model dominance ($\alpha = 1.0$) due to score scale calibration mismatches [3]. This was remediated in Stage A.1 by overhauling interaction modeling and implementing Reciprocal Rank Fusion (RRF, $k=60$), elevating recommendation quality ($\text{NDCG}@10 > 0.12$).
3. **Real-Time Analytical Explainability (Stage 7)**: Initial investigations into SHAP (SHapley Additive exPlanations) were abandoned due to prohibitive inference latency ($> 1.5$s) [5]. SHAP was replaced by an analytical feature-matching explainer (`explainer.py`) that calculates deterministic aspect alignment scores in $< 5$ ms.
4. **Grounded RAG & Hallucination Protection (Stages C, D, G)**: Review text was segmented into 7,910 chunks and embedded into 384-dimensional vector representations using SentenceTransformers (`all-MiniLM-L6-v2`) [10]. A Hybrid Retrieval engine combining vector similarity, metadata filtering, and recommender reranking ($\text{Precision}@5 = 0.81$) was coupled with a 1,500-token `ContextCompressor`, `PromptOrchestrator`, local Ollama LLM (`llm_service.py`), `CitationInjector`, and a `GroundingValidator` that actively stripped fabricated amenity assertions ($96.7\%$ grounded response rate, $1.3\%$ hallucination rate) [9].
5. **PostgreSQL 17.6 + pgvector Cutover (Stages 23--24.5)**: The backend was decoupled via Clean Architecture repository patterns (`PostgresHotelRepository`, `PgVectorEmbeddingRepository`) and migrated from legacy CSV and ChromaDB file stores to PostgreSQL 17.6 with `pgvector`. Controlled parity verification demonstrated 1.0000 average embedding cosine similarity parity and zero orphan records across an 18-test provenance suite.
6. **Repeatable Ingestion & Pipeline Orchestration (Stages 26--29)**: Stage 26 established a 9-stage repeatable ingestion lifecycle featuring SHA-256 canonical content hashing (`calculate_canonical_content_hash`), field-level diffing, dry-run safety (`dry_run.json`), human approval gates (`apply --run-id`), and selective vector synchronization. Stage 28 unified all 6 upstream stages into a single-command CLI orchestrator (`scripts/orchestrator.py`), while Stage 29 added live ASCII progress tracking (`ProgressTracker`) and `SIGINT` (Ctrl+C) signal protection, achieving a 100% pass rate across the complete 50/50 backend Pytest suite.

### 5.2 Major Technical Contributions
This project delivers nine major technical and engineering contributions:
1. **Preference-Aware Hybrid Recommendation Engine**: Demonstrated that Reciprocal Rank Fusion (RRF, $k=60$) resolves score scale calibration mismatches between collaborative filtering and content-based models, elevating ranking quality ($\text{NDCG}@10 > 0.12$).
2. **Real-Time Analytical Explainability Engine**: Designed a deterministic aspect-matching explainer that calculates feature alignment percentages in $< 5$ ms, bypassing the high latency of SHAP approximations.
3. **Aspect-Based Sentiment Extraction**: Implemented DistilBERT sentence sentiment analysis and keyword-masked ABSA across Cleanliness, Service, Location, Value, and Staff Behavior, identifying Cleanliness as the primary aspect differentiator across Delhi NCR hotels.
4. **Review-Grounded Hybrid RAG Pipeline**: Combined dense vector similarity search, SQL metadata filtering, and recommender reranking to retrieve relevant review chunks, context-compressing them under a 1,500-token budget [9].
5. **Automated Grounding Validator**: Built a post-generation validation layer (`grounding_validator.py`) that cross-references LLM assertions against retrieved evidence chunks, achieving a $96.7\%$ grounded response rate and a $1.3\%$ hallucination rate.
6. **Unified PostgreSQL + pgvector Infrastructure**: Unified relational metadata and 384-dimensional vector embeddings inside PostgreSQL 17.6, establishing 1.0000 average embedding cosine similarity parity against legacy file stores.
7. **SHA-256 Field-Level Diff Engine**: Developed a canonical content hashing engine (`diff_engine.py`) that classifies record change sets and selective vector synchronization, preventing redundant embedding recalculations.
8. **One-Command CLI Master Orchestrator**: Built a unified CLI runner (`python -m scripts.orchestrator full`) that sequentially executes all 6 upstream processing stages with database read-only safety.
9. **Live Operational Visibility and Signal Safety**: Implemented an interactive ASCII terminal progress dashboard (`ProgressTracker`) and a custom `SIGINT` (Ctrl+C) signal handler guaranteeing zero database corruption.

### 5.3 Summary of Experimental Findings
Empirical findings across the evaluation suites confirm system efficacy under tested conditions:
- **NLP & ABSA**: DistilBERT sentence sentiment probabilities correlated strongly ($r \approx 0.84$) with user star ratings. Cleanliness demonstrated the highest score variance among hospitality aspect dimensions.
- **Recommender Failure & RRF Recovery**: Initial SVD matrix factorization failed ($\text{NDCG}@10 = 0.006$) under 99.27% interaction matrix sparsity, causing linear blending to collapse to $\alpha=1.0$. Overhauling preference interactions and deploying RRF rank fusion restored ranking quality to $\text{NDCG}@10 > 0.12$.
- **Explainability Latency**: Analytical feature-matching explanations executed in $< 5$ ms with 100% readability audit pass rates, compared to $> 1.5$ seconds for SHAP value calculations.
- **Hybrid RAG Retrieval**: Hybrid vector search achieved Precision@5 of $0.81$, Recall@5 of $0.79$, and MRR of $0.83$. Metadata filtering contributed $+0.07$ to Precision@5, while recommender reranking contributed $+0.05$. Total retrieval latency measured $165.8$ ms.
- **Grounding Validation**: `GroundingValidator` achieved a $96.7\%$ grounded response rate and a $1.3\%$ hallucination rate, actively intercepting 3 responses containing unverified amenity assertions.
- **Database Vector Parity**: PostgreSQL `pgvector` backfill achieved 1.0000 average embedding cosine similarity parity and 20/20 (100%) top-1 RAG query parity against legacy ChromaDB file stores.
- **Automated Pytest Suite**: Master backend test suite achieved a **50 / 50 PASSED (100%)** result across Stage 24.5 provenance, Stage 26 ingestion, Stage 28 orchestrator, Stage 29 progress, and API integration suites.

### 5.4 Engineering Lessons Learned
The engineering evolution of TrustLayer-AI highlighted six critical design insights:
1. **Evaluation Metric Selection Matters**: Rating prediction error metrics (such as RMSE) fail to capture top-$K$ recommendation utility. Evaluating ordinal ranking quality via $\text{NDCG}@K$ is essential for identifying model failure [4].
2. **Rank Fusion Eliminates Calibration Mismatches**: Combining uncalibrated scalar prediction scores from heterogeneous models leads to single-model dominance. Fusing ordinal ranks via Reciprocal Rank Fusion (RRF) provides robust model blending [3].
3. **Synthetic Interaction Quality Is Decisive**: Synthetic user interaction generators must inject realistic preference overlap; uniform random generation introduces severe matrix sparsity that destroys collaborative filtering signals.
4. **Decoupled Storage Invites Data Drift**: Operating file-based vector databases alongside tabular metadata files leads to structural data drift. Unifying relational metadata and vector storage within an ACID-compliant SQL database ensures strict data integrity.
5. **Data Mutation Requires Approval Boundaries**: Production ingestion systems must separate diff generation from database write execution using dry-run reports (`dry_run.json`) and explicit human approval gates (`apply --run-id`).
6. **Pipeline Observability Prevents Corruption**: Long-running data pipelines require real-time progress monitoring, structured logging, and signal handlers (`SIGINT`) to prevent incomplete process terminations from corrupting state.

### 5.5 Project Limitations
The empirical findings and architecture of TrustLayer-AI operate under four documented constraints:
- **Google Places API Detail Limits**: The external Places Details API caps retrieved user text reviews at 5 per property request, limiting deep long-tail review volume analysis.
- **Missing Price Attribute**: Google Places API returned 100% missing `price_level` data for properties in India, requiring engineered `budget_category` proxy variables.
- **Synthetic Interaction Matrices**: Collaborative filtering evaluation relied on synthetic user interaction profiles (V2 preference overlap model) rather than captured from live commercial transaction logs.
- **Local Single-Host Infrastructure**: System benchmarking, local LLM inference (`mistral`/`llama3`), and PostgreSQL database deployments were evaluated on single-host developer infrastructure.

### 5.6 Future Work
Building upon the verified foundation of TrustLayer-AI, future research and development can extend the platform along seven primary directions:
1. **Commercial Interaction Data Integration**: Ingest real-world traveler booking logs to evaluate collaborative filtering and learning-to-rank (LTR) algorithms over production scale interaction volumes.
2. **Advanced LLM-Based ABSA**: Replace keyword-masked aspect extraction with fine-tuned transformer models (e.g., LLaMA-3 or Mistral ABSA adapters) to capture nuanced aspect sentiment in complex review phrases.
3. **Neural Reranking and Learning-to-Rank**: Explore deep learning-to-rank models (such as RankNet or LambdaMART) to dynamically weight vector similarity, aspect alignment, and trust scores.
4. **Automated Pipeline Scheduling and Webhook Alerting**: Integrate background task schedulers (such as Celery or Airflow) to execute automated cron ingestion, triggering Slack/email webhook alerts on diff anomalies.
5. **Distributed Vector Search Clustering**: Scale vector database storage across distributed PostgreSQL `pgvector` clusters to support millions of document chunks with sub-10 ms search latency.
6. **User Evaluation Studies**: Conduct formal user studies to evaluate human perceptions of trust, explanation clarity, and UI provenance drawer utility in real travel search scenarios.
7. **Multi-City Geographic Expansion**: Expand data collection and bounding-box normalization beyond Delhi NCR to cover major tourist destinations across India.

### 5.7 Final Conclusion
TrustLayer-AI demonstrates how hybrid recommendation models, structured aspect explainability, review-grounded RAG, automated grounding validation, and unified relational/vector storage can be synthesized into a cohesive, auditable system. By identifying and resolving critical engineering failures—including matrix sparsity collapse, score calibration mismatches, SHAP inference latency, LLM hallucination risks, vector store data drift, and pipeline fragmentation—the project establishes a robust reference architecture for trustworthy conversational recommendation engines. As an Independent Project at Indraprastha Institute of Information Technology, Delhi, TrustLayer-AI provides a complete, verified foundation for future research in explainable AI and grounded conversational intelligence.

---

## Bibliography

1. **Ramesh, R., Raman, R. S., Bernhard, M., Ongkowijaya, V., Evdokimov, L., Edmundson, A., Sprecher, S., Ikram, M., & Ensafi, R. (2020)**. *Decentralized Control: A Case Study of Russia*. In Proceedings of the 2020 Network and Distributed System Security Symposium (NDSS 2020). DOI: [10.14722/ndss.2020.23098](http://dx.doi.org/10.14722/ndss.2020.23098).
2. **Koren, Y., Bell, R., & Volinsky, C. (2009)**. *Matrix Factorization Techniques for Recommender Systems*. IEEE Computer, 42(8), 30–37.
3. **Cormack, G. V., Clarke, C. L. A., & Buettcher, S. (2009)**. *Reciprocal Rank Fusion Outperforms Rank-With-Score for Compound Rank Tasks*. In Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '09), pp. 758–759.
4. **Järvelin, K., & Kekäläinen, J. (2002)**. *Cumulated Gain-Based Evaluation of IR Techniques*. ACM Transactions on Information Systems, 20(4), 422–446.
5. **Lundberg, S. M., & Lee, S.-I. (2017)**. *A Unified Approach to Interpreting Model Predictions*. In Advances in Neural Information Processing Systems 30 (NeurIPS 2017), pp. 4765–4774.
6. **Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019)**. *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter*. arXiv preprint arXiv:1910.01108.
7. **Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019)**. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. In Proceedings of NAACL-HLT 2019, pp. 4171–4186.
8. **Pontiki, M., Galanis, D., Papageorgiou, H., Androutsopoulos, I., Manandhar, S., et al. (2016)**. *SemEval-2016 Task 5: Aspect Based Sentiment Analysis*. In Proceedings of SemEval '16, pp. 19–30.
9. **Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., et al. (2020)**. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. In Advances in Neural Information Processing Systems 33 (NeurIPS 2020), pp. 9459–9474.
10. **Reimers, N., & Gurevych, I. (2019)**. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. In Proceedings of EMNLP-IJCNLP 2019, pp. 3982–3992.
