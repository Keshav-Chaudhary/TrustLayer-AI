# Stage B.1: Explainability Validation Audit Report

## 1. Fidelity Breakdown
| Factor | Frequency | Drop Frequency | Drop % | Mean Rank Change | Median Rank Change | Score Change | Top-10 Eviction % |
|---|---|---|---|---|---|---|---|
| area_match | 178 | 166 | 93.26% | 51.98 | 17.0 | -0.0106 | 62.36% |
| budget_match | 284 | 182 | 64.08% | 7.74 | 1.0 | -0.0030 | 18.31% |
| service_sentiment | 36 | 20 | 55.56% | 4.36 | 1.0 | -0.0024 | 13.89% |
| high_trust_score | 214 | 66 | 30.84% | 0.79 | 0.0 | -0.0009 | 2.34% |
| staff_behavior_sentiment | 64 | 34 | 53.12% | 1.47 | 1.0 | -0.0011 | 1.56% |
| location_sentiment | 120 | 72 | 60.00% | 8.58 | 1.0 | -0.0033 | 18.33% |
| cleanliness_sentiment | 47 | 23 | 48.94% | 3.04 | 0.0 | -0.0023 | 10.64% |
| value_for_money_sentiment | 24 | 19 | 79.17% | 5.79 | 3.0 | -0.0045 | 25.00% |

## 2. Expanded RRF Validation
- Explanations Evaluated: 1000
- Classification Accuracy: 100.00%

## 3. Explanation-Type Distribution
| Type | Count | Percentage |
|---|---|---|
| cb_dominant | 437 | 43.70% |
| balanced_hybrid | 378 | 37.80% |
| cf_dominant | 149 | 14.90% |
| fallback | 36 | 3.60% |

## 4. Confidence Calibration
| Confidence | Count | Avg Training Interactions | Avg Final Rank |
|---|---|---|---|
| High | 110 | 35.79 | 6.06 |
| Medium | 780 | 19.48 | 5.42 |
| Low | 110 | 4.09 | 5.50 |

## 5. Explanation Diversity Audit
- **Unique Explanation Templates (NLG Strings)**: 304
- **Unique Top-Factors Combinations**: 57
- **Average Explanation Diversity per User (1 - Jaccard)**: 0.4936

## 6. Consistency Evaluation
- **Intra-User Consistency (Mean Jaccard)**: 0.5064
