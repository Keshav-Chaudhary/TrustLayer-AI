# STAGE 24 — DUAL-BACKEND PARITY VERIFICATION REPORT

## Executive Summary
This document provides empirical dual-backend parity results comparing the active **CSV + ChromaDB** backend against the secondary **PostgreSQL + pgvector** storage target.

---
## 1. Hotel Entity & Field Parity
- **CSV Hotel Count**: 1661
- **PostgreSQL Hotel Count**: 1661
- **Matched Hotel IDs**: 1661
- **Missing in PostgreSQL**: 0
- **Extra in PostgreSQL**: 0
- **Field Mismatches Count**: 0

---
## 2. Vector Embedding Coverage
- **ChromaDB Vector Chunks**: 7910
- **pgvector Storage Chunks**: 50

---
## 3. 20 RAG Recommendation Queries Parity Suite
| Query | Top Recommendation | Trust Score | Count | Status |
|---|---|---|---|---|
| `clean hotels in Delhi` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `budget stay in Delhi NCR` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `luxury hotel near Mahipalpur` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotels close to Indira Gandhi International airport` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `cheap hotels under 2000 in Delhi` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `5 star luxury stay in Delhi` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `highest rated hotels with 4.5 rating` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotel with free wifi and swimming pool` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `business hotel in Gurugram` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `family friendly stay in Noida` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotels in Mumbai` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `beach resort in Goa` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `tech stay in Bangalore` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotels in Pune` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `heritage hotel in Jaipur` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotels in NonExistentCity999` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotel near Aerocity` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotel with high cleanliness score` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotel for solo traveler in Karol Bagh` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |
| `hotel near Connaught Place` | Error | 0.0 | 0 | `FAILED (RecommendationService.process_query() got an unexpected keyword argument 'limit')` |