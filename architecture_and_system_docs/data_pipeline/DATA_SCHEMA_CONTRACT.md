# DATA SCHEMA CONTRACT

## Required & Optional Fields
- `hotel_id` (string, Required): Unique canonical identifier.
- `name` / `hotel_name` (string, Required): Official hotel name.
- `rating` (float, Optional): Bound `[0.0, 5.0]`. Default: `4.0`.
- `review_count` (integer, Optional): Bound `>= 0`. Default: `0`.
- `trust_score` (float, Optional): Bound `[0.0, 100.0]`. Default: `85.0`.
- `latitude` (float, Optional): Bound `[-90.0, 90.0]`.
- `longitude` (float, Optional): Bound `[-180.0, 180.0]`.
- `amenities` (list/string, Optional): Normalized list of amenity names.
