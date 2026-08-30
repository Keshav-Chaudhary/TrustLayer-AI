# Step 1: Retriever Validation

## Performance
- **Average Retrieval Latency**: 2146.54 ms
- **Candidates before filtering**: 50 (fetch_k = 10 * 5)
- **Candidates after filtering**: Varies based on hard constraints (returns up to 10 after ranking)

## Score Distributions
- **Semantic Score**: min=0.41, max=1.00, avg=0.76
- **Metadata Score**: min=0.00, max=0.30, avg=0.08
- **Recommendation Score**: min=0.23, max=0.97, avg=0.71
- **Final Score**: min=0.46, max=0.81, avg=0.61

## Edge Cases Handled
- **Empty Constraints**: Gracefully handles missing hard/soft constraints (defaults to empty dicts).
- **No Semantic Spread**: The `1e-9` in `max_dist - min_dist + 1e-9` prevents division by zero when all semantic distances are identical.
- **Normalization Boundaries**: Min-max normalization strictly forces the highest ranked semantic chunk to 1.0 and lowest to 0.0 per query batch.

## Top-10 Example: Score Decomposition
**Query**: `luxury family hotels in Delhi`
**Hard Constraints**: `{}`
**Soft Constraints**: `{'travel_purpose': 'family', 'budget_category': 'luxury'}`

| Rank | Hotel/Chunk ID | Semantic (0.6) | Metadata (0.2) | Rec Score (0.2) | Final Score |
|---|---|---|---|---|---|
| 1 | ChIJZVHCl2ocDTkR4FUy2t2OM2c_chunkC | 0.962 | 0.217 | 0.942 | **0.809** |
| 2 | ChIJmyas5kQfDTkRq1YVNY1ULj8_chunkA | 1.000 | 0.000 | 0.840 | **0.768** |
| 3 | ChIJzUZZUdzjDDkRJKDEesqf9fQ_chunkC | 0.901 | 0.100 | 0.847 | **0.730** |
| 4 | ChIJY6Gyi5UCDTkRmjXmCUzwY6w_chunkA | 0.794 | 0.300 | 0.821 | **0.700** |
| 5 | ChIJ0bhXzyPnDDkRtIidxqRxIhM_chunkA | 0.816 | 0.150 | 0.869 | **0.693** |
| 6 | ChIJEefgc975DDkRMtvbFpfSpBo_chunkA | 0.780 | 0.150 | 0.952 | **0.689** |
| 7 | ChIJUQAAACQCDTkROgV0toDmdlM_chunkA | 0.912 | 0.000 | 0.656 | **0.679** |
| 8 | ChIJW9lffGEPDTkRKS5A-LwG5AU_chunkA | 0.622 | 0.150 | 0.966 | **0.596** |
| 9 | ChIJn4gzI1ziDDkR9O77oIjkc7E_chunkC | 0.634 | 0.150 | 0.815 | **0.574** |
| 10 | ChIJG7ishgb9DDkRnIrNWT8PfPM_chunkC | 0.583 | 0.250 | 0.780 | **0.556** |
