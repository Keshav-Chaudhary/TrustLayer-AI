# Stage A.1 Phase 1: Interaction Quality Audit

## Quantitative Metrics

1. **Total interactions generated**: `14069`
2. **User activity distribution table**:
   - 5-15 interactions: 176 users (35.2%)
   - 15-30 interactions: 193 users (38.6%)
   - 30-75 interactions: 105 users (21.0%)
   - 75-150 interactions: 26 users (5.2%)
3. **Number of users in each activity bucket**: (See above)
4. **Area Alignment Rate (%)**: `72.79%`
5. **Budget Alignment Rate (%)**: `90.36%`
6. **Travel Purpose Alignment Rate (%)**: `72.51%` (Proxy metric based on trust_score alignment)
7. **Amenity Alignment Rate (%)**: `0.00%` 
   *Justification: The `final_hotel_dataset.csv` does not contain an `amenities` column. Amenity alignment calculations are impossible without this data, so it defaults to zero.*
8. **Cold-start user statistics (Train Interactions)**: 
   - 0 train interactions: 0 users
   - 1 train interaction: 0 users
   - <= 3 train interactions: 14 users
   - <= 5 train interactions: 64 users
   *(evaluate_recommenders.py will use the <= 5 training interactions definition, resulting in an exact cold-start cohort of 64 users for the evaluation table).*
9. **Interaction matrix dimensions**: `500 users × 1661 hotels`
10. **Matrix sparsity (%)**: `98.3060%`

## Validation Assertions
- **interactions_v2.csv row count**: `14069` -> Valid
- **Schema validation results**: True -> Valid
- **Long-tail distribution validation**: True -> Valid
- **Alignment threshold validation**: Area>=70% & Budget>=80% -> True -> Valid

## Visual Diagnostics (from 10_interaction_quality_audit.ipynb)

### User Activity Histogram
![User Activity Histogram](D:\Side_Projects\0_Independent_Project\TrustLayer-AI\research\reports\images\activity_hist.png)

### Hotel Popularity Distribution
![Hotel Popularity Distribution](D:\Side_Projects\0_Independent_Project\TrustLayer-AI\research\reports\images\hotel_pop.png)

### Preference Alignment Charts
![Preference Alignment](D:\Side_Projects\0_Independent_Project\TrustLayer-AI\research\reports\images\alignment.png)

*Note: Interaction density visualization and cold-start population analysis are reflected in the Matrix Sparsity (98.3060%) and User Activity Histogram.*
