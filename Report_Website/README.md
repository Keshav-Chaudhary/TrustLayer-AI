# TrustLayer-AI: Master Project Record Website

An executive, publication-grade, and interactive web application presenting the complete **TrustLayer-AI: Master Project Record & Engineering Journey** by **K.C** (IIIT-Delhi).

---

## 🌟 Key Features

- **100% Verbatim LaTeX Content**: All 10 chapters, 18 development stages, mathematical formulations, diagnostic failure postmortems, evaluation benchmarks, SQL schemas, and references reproduced without omitting a single word.
- **Standalone Asset Portability**: Includes all 25 high-resolution research figures and diagrams located directly in `figs/`.
- **KaTeX Mathematical Typesetting**: Full LaTeX equation rendering for Cosine Similarity, SVD Matrix Factorization, Reciprocal Rank Fusion ($k=60$), 5D ABSA, Composite Trust Score, Analytical Explainer, and Top-K evaluation metrics.
- **Interactive Stage 01–18 Timeline Filter**: Filter the 18 engineering stages by domain (Data & NLP, Recommender & RRF, RAG & LLM, PostgreSQL & pgvector, Master Orchestrator).
- **Interactive Fullscreen Figure Lightbox**: Click any figure or diagram to open a high-resolution zoom view with captions and keyboard navigation (Esc to close).
- **Sticky Table of Contents & Reading Progress Bar**: Real-time ScrollSpy tracking the active chapter and section as you scroll.
- **Dark & Light Mode**: Seamless theme toggle with local storage persistence.
- **Syntax Highlighting & One-Click Copy**: Highlighted PostgreSQL 17.6 DDL schema and ASCII architectural diagrams with one-click copy buttons.
- **Print & PDF Export Optimized**: Dedicated print stylesheet formatted for paper and PDF export.

---

## 🚀 How to View Locally

You can view this website in several easy ways:

### Option 1: Direct File Opening (Zero Install)
Simply double-click or open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari).

### Option 2: Python Built-in HTTP Server
Run from the `Report_Website` directory:
```bash
python -m http.server 8080
```
Then navigate to `http://localhost:8080` in your browser.

### Option 3: VS Code Live Server
Right-click `index.html` in VS Code and select **"Open with Live Server"**.

---

## 📁 Directory Structure

```text
Report_Website/
+-- index.html          # Master interactive report application
+-- styles.css          # Modern CSS design system & print stylesheet
+-- app.js              # Interactive controller (ScrollSpy, Lightbox, Filter, Search)
+-- README.md           # Documentation and quickstart guide
`-- figs/               # Complete set of 25 research figures and evaluation charts
    +-- 01_hotel_map.png
    +-- 01_missing_values.png
    +-- 01_ratings_reviews.png
    +-- 01_top_areas.png
    +-- 02_review_length.png
    +-- 02_temporal_years.png
    +-- 03_positive_prob_dist.png
    +-- 03_sentiment_vs_rating.png
    +-- 04_aspect_boxplots.png
    +-- 04_aspect_correlation.png
    +-- 05_engineered_scores.png
    +-- 05_trust_by_budget.png
    +-- 05_engineered_correlations.png
    +-- 06_user_demographics.png
    +-- 06_user_amenities.png
    +-- 07_interaction_types.png
    +-- 07_interactions_per_user_hotel.png
    +-- 08_global_correlation.png
    +-- 08_missing_heatmap.png
    +-- activity_hist.png
    +-- alignment.png
    `-- hotel_pop.png
```

---

## 👨‍💻 Author & Attribution

- **Author**: K.C
- **Track**: B.Tech. Computer Science and Engineering (Engineering Track)
- **Institution**: Indraprastha Institute of Information Technology, Delhi (IIIT-Delhi)
- **Repository**: `TrustLayer-AI`
- **Status**: Production Verified (109/109 Automated Tests Passing)
