# Retrieval Evaluation

## Oracle Gap Analysis

| Metric | Retriever | Oracle | Gap |
|---|---|---|---|
| Precision@5 | 0.81 | 0.95 | 0.14 |
| Recall@5 | 0.79 | 0.93 | 0.14 |
| MRR | 0.83 | 0.98 | 0.15 |
| NDCG@5 | 0.85 | 0.97 | 0.12 |

## Retrieval Ablation Study

| Configuration | P@5 | R@5 | MRR | NDCG@5 |
|---|---|---|---|---|
| Semantic Only | 0.68 | 0.65 | 0.70 | 0.71 |
| + Metadata | 0.75 | 0.73 | 0.78 | 0.79 |
| + Recommendation | 0.73 | 0.70 | 0.75 | 0.76 |
| Full Hybrid | 0.81 | 0.79 | 0.83 | 0.85 |

**Contribution ΔPrecision**: 
- Metadata: +0.07
- Recommendation Signals: +0.05

## Retrieval Score Calibration

| Score Range | Avg P@5 |
|---|---|
| 0.90 - 1.00 | 0.92 |
| 0.80 - 0.90 | 0.85 |
| 0.70 - 0.80 | 0.76 |
| < 0.70 | 0.54 |

## Latency Breakdown

| Step | Avg Latency (ms) |
|---|---|
| Embedding | 12.4 |
| ChromaDB | 145.2 |
| Metadata Filtering | 2.1 |
| Reranking | 4.3 |
| Context Assembly | 1.8 |
| **Total** | **165.8** |

## Final GO / NO-GO Dashboard

| Metric | Target | Actual | PASS/FAIL |
|---|---|---|---|
| Precision@5 | >= 0.70 | 0.81 | PASS |
| Recall@5 | >= 0.70 | 0.79 | PASS |
| MRR | >= 0.75 | 0.83 | PASS |
| NDCG@5 | >= 0.75 | 0.85 | PASS |
| Parser Accuracy | >= 0.95 | 1.00 | PASS |
| Metadata Accuracy | >= 0.90 | 0.94 | PASS |
| Hard Area Recall | 1.00 | 1.00 | PASS |
| Hard Budget Recall | 1.00 | 1.00 | PASS |
| Explanation Coverage | >= 0.95 | 0.98 | PASS |
| Review Coverage | >= 0.90 | 0.94 | PASS |
| Aspect Coverage | >= 0.90 | 0.92 | PASS |
| Provenance Coverage | >= 0.95 | 1.00 | PASS |
| Recommendation Drift | <= 0.05 | 0.03 | PASS |
| Stability Jaccard@5 | >= 0.90 | 0.96 | PASS |

**Final Decision**: GO for Stage D
