# Aspect Distribution Audit

## 1. Aspect Scores Analysis

| Feature | Mean | Std Dev | Min | Max | P5 | P50 (Median) | P95 | Status |
|---|---|---|---|---|---|---|---|---|
| cleanliness_score | 0.5416 | 0.3809 | 0.0002 | 0.9999 | 0.0003 | 0.5000 | 0.9999 | Pass (>= 0.05) |
| service_score | 0.5553 | 0.3743 | 0.0002 | 0.9999 | 0.0003 | 0.5000 | 0.9999 | Pass (>= 0.05) |
| location_score | 0.6124 | 0.3360 | 0.0002 | 0.9999 | 0.0005 | 0.5000 | 0.9999 | Pass (>= 0.05) |
| value_for_money_score | 0.4687 | 0.3543 | 0.0002 | 0.9999 | 0.0003 | 0.5000 | 0.9998 | Pass (>= 0.05) |
| staff_behavior_score | 0.6201 | 0.3642 | 0.0002 | 0.9999 | 0.0004 | 0.6667 | 0.9999 | Pass (>= 0.05) |

## 2. Recommendation Signals Analysis

| Feature | Mean | Std Dev | Min | Max | P5 | P50 (Median) | P95 |
|---|---|---|---|---|---|---|---|
| trust_score | 0.6809 | 0.1703 | 0.0000 | 1.0000 | 0.3699 | 0.7033 | 0.9084 |
| rating_score | 4.0740 | 0.5963 | 1.0000 | 5.0000 | 3.0000 | 4.1000 | 4.9000 |
| sentiment_score | 0.5794 | 0.3230 | 0.0002 | 0.9999 | 0.0009 | 0.6001 | 0.9998 |

## 3. Final Recommendation

- **cleanliness_score**: Std=0.3809 -> Recommendation: **Retrieval + Explanation**
- **service_score**: Std=0.3743 -> Recommendation: **Retrieval + Explanation**
- **location_score**: Std=0.3360 -> Recommendation: **Retrieval + Explanation**
- **value_for_money_score**: Std=0.3543 -> Recommendation: **Retrieval + Explanation**
- **staff_behavior_score**: Std=0.3642 -> Recommendation: **Retrieval + Explanation**
