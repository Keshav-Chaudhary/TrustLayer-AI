# Stage C.3: Vector Store Audit

## Collection Statistics
- **Total hotels processed**: 1661
- **Total hotels embedded**: 1661
- **Failed hotels**: 0
- **Total chunks**: 7910
- **Average chunks per hotel**: 4.76
- **Median chunks per hotel**: 5.0

## Chunk Type Distribution
- Chunk A (Profile): 1661
- Chunk B (Aspects): 1661
- Chunk C (Pos Evidence): 1618
- Chunk D (Neg Evidence): 1309
- Chunk E (Rec Signals): 1661

## Metadata Validation
| Chunk Type | hotel_id cov | area cov | budget cov | trust_score cov | aspect cov | Missing % |
|---|---|---|---|---|---|---|
| Chunk A (Profile) | 100% | 100% | 100% | 100% | 100% | 0.00% |
| Chunk B (Aspects) | 100% | 100% | 100% | 100% | 100% | 0.00% |
| Chunk C (Pos Evidence) | 100% | 100% | 100% | 100% | 100% | 0.00% |
| Chunk D (Neg Evidence) | 100% | 100% | 100% | 100% | 100% | 0.00% |
| Chunk E (Rec Signals) | 100% | 100% | 100% | 100% | 100% | 0.00% |

## Evidence-Level Distribution
- Rich evidence hotels: 1310 chunks
- Moderate evidence hotels: 5826 chunks
- Sparse evidence hotels: 672 chunks
- No evidence hotels: 102 chunks

## Embedding Validation
- **Embedding model**: sentence-transformers/all-MiniLM-L6-v2
- **Embedding dimension**: 384
- **Failed embeddings**: 0
- **Empty chunks skipped**: 0
- **Duplicate chunks detected**: 0

## Chroma Validation
- Self-retrieval rate (Top-5): 100.00%
- Mean self rank: 1.25
