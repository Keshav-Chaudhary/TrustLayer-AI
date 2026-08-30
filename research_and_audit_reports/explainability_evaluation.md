# Stage B: Explainability Evaluation Report

## 1. Metrics
- **Coverage**: 96.40%
- **Fidelity**: 45.00% (Percentage of ablated features causing rank drops)

## 2. Sample Structured Explanations (JSON)
```json
{
  "hotel_id": "ChIJBS-HCGL9DDkRnvfrMTf9pDM",
  "user_id": "f6bca5e6-d93f-4742-9d35-8b9c2d6ae349",
  "cb_rank": 28,
  "cf_rank": 5,
  "rrf_score": 0.011363636363636364,
  "explanation_type": "cb_dominant",
  "top_factors": [
    "budget_match",
    "service_sentiment",
    "high_trust_score"
  ],
  "confidence": "Low",
  "nlg_text": "Recommended because it falls within your budget category (Luxury), has excellent service sentiment, and has a strong verified trust score. Confidence: Low"
}
```
```json
{
  "hotel_id": "ChIJO_r_o_cADTkRGwll3ggET_I",
  "user_id": "f6bca5e6-d93f-4742-9d35-8b9c2d6ae349",
  "cb_rank": 13,
  "cf_rank": 19,
  "rrf_score": 0.0136986301369863,
  "explanation_type": "cb_dominant",
  "top_factors": [
    "budget_match",
    "service_sentiment",
    "high_trust_score"
  ],
  "confidence": "Low",
  "nlg_text": "Recommended because it falls within your budget category (Luxury), has excellent service sentiment, and has a strong verified trust score. Confidence: Low"
}
```
```json
{
  "hotel_id": "ChIJ9W1BH1UHDTkR-atCKhI6R6Y",
  "user_id": "f6bca5e6-d93f-4742-9d35-8b9c2d6ae349",
  "cb_rank": 1,
  "cf_rank": 56,
  "rrf_score": 0.01639344262295082,
  "explanation_type": "cb_dominant",
  "top_factors": [
    "area_match",
    "budget_match",
    "service_sentiment"
  ],
  "confidence": "Low",
  "nlg_text": "Recommended because it matches your preferred area (Delhi), falls within your budget category (Luxury), and has excellent service sentiment. Confidence: Low"
}
```
