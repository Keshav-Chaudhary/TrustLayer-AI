# TrustLayer-AI Raw Production Audit

Audit Executed At: 2026-07-16 18:52:57

## Pre-flight Checks
### GET /health
```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```
Status: 200
Latency: 8.2ms
Output:
```json
{"status":"ok","message":"TrustLayer-AI API is healthy"}
```

### GET /metrics
```powershell
Invoke-RestMethod http://127.0.0.1:8000/metrics
```
Status: 200
Latency: 5.4ms
Output:
```json
{"total_hotels":3450,"total_chunks":7910,"cache_hit_rate":0.0,"avg_latency_ms":185.0}
```

## AI Query Audit (100 Queries)
### Query 1: family hotels in Delhi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotels in Delhi"}'
```
Status: 200
Latency: 42.7ms
Response excerpt:
```json
{"trace_id":"req-f528cafe","query":"family hotels in Delhi","recommendations":[{"hotel_id":"ChIJQTyWH_v9DDkRWIAPGAhMUz0","name":"Homestay Near Isbt Kashmiri Gate & Metro | Private Rooms & Dorms","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":2.5,"location":3.3,"value":5.0},"trust_score":90.7,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to conf
...[truncated]...
```

### Query 2: family hotels with good cleanliness
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotels with good cleanliness"}'
```
Status: 200
Latency: 71.0ms
Response excerpt:
```json
{"trace_id":"req-ff25773d","query":"family hotels with good cleanliness","recommendations":[{"hotel_id":"ChIJa8DmBlkZDTkRmCx2X4Z5BuU","name":"Kohsa7","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":79.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignmen
...[truncated]...
```

### Query 3: business hotels in Aerocity
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotels in Aerocity"}'
```
Status: 200
Latency: 68.1ms
Response excerpt:
```json
{"trace_id":"req-f5392665","query":"business hotels in Aerocity","recommendations":[{"hotel_id":"ChIJ7bfQAnIcDTkR6QuFSvjr3e4","name":"Lemon Tree Hotel, Delhi Airport","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.3,"service":4.5,"location":2.5,"value":3.9},"trust_score":82.6,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterio
...[truncated]...
```

### Query 4: quiet hotels near airport
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "quiet hotels near airport"}'
```
Status: 200
Latency: 59.6ms
Response excerpt:
```json
{"trace_id":"req-8127ceff","query":"quiet hotels near airport","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","que
...[truncated]...
```

### Query 5: luxury stays in Gurugram
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury stays in Gurugram"}'
```
Status: 200
Latency: 60.8ms
Response excerpt:
```json
{"trace_id":"req-2cab4ba3","query":"luxury stays in Gurugram","recommendations":[{"hotel_id":"ChIJ2Q_vUgAhDTkRG9JSfed_m9U","name":"Grand Mantram Resort","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":83.9,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_ali
...[truncated]...
```

### Query 6: budget hotels in Paharganj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotels in Paharganj"}'
```
Status: 200
Latency: 71.1ms
Response excerpt:
```json
{"trace_id":"req-ffefb0b2","query":"budget hotels in Paharganj","recommendations":[{"hotel_id":"ChIJAZTkm0D9DDkRMDezVFMRIKM","name":"The Gold Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":74.3,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignment_s
...[truncated]...
```

### Query 7: hotels with breakfast in Karol Bagh
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotels with breakfast in Karol Bagh"}'
```
Status: 200
Latency: 68.7ms
Response excerpt:
```json
{"trace_id":"req-503d60bb","query":"hotels with breakfast in Karol Bagh","recommendations":[{"hotel_id":"ChIJ3S7zfJ8CDTkRI1ahIlccS5o","name":"Fabhotel Marble Arch - Hotel In Karol Bagh, New Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":0.0},"trust_score":42.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to conf
...[truncated]...
```

### Query 8: couple friendly hotels in New Delhi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "couple friendly hotels in New Delhi"}'
```
Status: 200
Latency: 55.2ms
Response excerpt:
```json
{"trace_id":"req-8a7c5820","query":"couple friendly hotels in New Delhi","recommendations":[{"hotel_id":"ChIJBb6nI8D9DDkRwrBTMaXlXG4","name":"Hotel Vcr Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":3.0,"location":2.5,"value":2.5},"trust_score":78.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_a
...[truncated]...
```

### Query 9: hotels with pool in Gurugram
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotels with pool in Gurugram"}'
```
Status: 200
Latency: 42.8ms
Response excerpt:
```json
{"trace_id":"req-d86881d7","query":"hotels with pool in Gurugram","recommendations":[{"hotel_id":"ChIJf4aZlKIZDTkRZvUGFuf-IV4","name":"The Trot Hotel & Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":3.7,"location":3.3,"value":3.3},"trust_score":76.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","quer
...[truncated]...
```

### Query 10: hotels with wifi in Mahipalpur
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotels with wifi in Mahipalpur"}'
```
Status: 200
Latency: 57.2ms
Response excerpt:
```json
{"trace_id":"req-75b9b066","query":"hotels with wifi in Mahipalpur","recommendations":[{"hotel_id":"ChIJC4a0GTAdDTkR08VLCKrqsfs","name":"Hotel Iconic","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":1.7,"location":5.0,"value":5.0},"trust_score":76.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignme
...[truncated]...
```

### Query 11: clean hotels near Paharganj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean hotels near Paharganj"}'
```
Status: 200
Latency: 191.5ms
Response excerpt:
```json
{"trace_id":"req-bf741187","query":"clean hotels near Paharganj","recommendations":[{"hotel_id":"ChIJ0yLaR0H9DDkR4ItbT8FxMO8","name":"Hotel Shelton","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":5.0,"value":0.0},"trust_score":78.4,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignment
...[truncated]...
```

### Query 12: affordable family hotel in Rohini
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "affordable family hotel in Rohini"}'
```
Status: 200
Latency: 77.9ms
Response excerpt:
```json
{"trace_id":"req-d64fde54","query":"affordable family hotel in Rohini","recommendations":[{"hotel_id":"ChIJQ5QKh-cBDTkRdH8g2foHdjc","name":"Gallivanto Inn - Rohini","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":4.0,"location":5.0,"value":3.3},"trust_score":81.9,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.
...[truncated]...
```

### Query 13: premium business stay in Sector 43
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "premium business stay in Sector 43"}'
```
Status: 200
Latency: 62.2ms
Response excerpt:
```json
{"trace_id":"req-feb3f4d0","query":"premium business stay in Sector 43","recommendations":[{"hotel_id":"ChIJ23KVO4gZDTkR8kPIdIcogHg","name":"Hotel Golf View Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":90.1,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.
...[truncated]...
```

### Query 14: airport hotel with shuttle
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "airport hotel with shuttle"}'
```
Status: 200
Latency: 47.9ms
Response excerpt:
```json
{"trace_id":"req-9c0e1bde","query":"airport hotel with shuttle","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","qu
...[truncated]...
```

### Query 15: hotels with parking in Dwarka
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotels with parking in Dwarka"}'
```
Status: 200
Latency: 49.7ms
Response excerpt:
```json
{"trace_id":"req-207eec44","query":"hotels with parking in Dwarka","recommendations":[{"hotel_id":"ChIJFT23yP8bDTkRm65IVfSQIsk","name":"Hideaway Bed And Breakfast","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":86.8,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion."
...[truncated]...
```

### Query 16: safe hotel for solo traveler
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "safe hotel for solo traveler"}'
```
Status: 200
Latency: 38.8ms
Response excerpt:
```json
{"trace_id":"req-20309109","query":"safe hotel for solo traveler","recommendations":[{"hotel_id":"ChIJ5V5eFuAHDTkR47MCn7ul_ww","name":"Fabexpress The Maharaja Grand","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":63.2,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.0,"review_evidence":[],"provenance":[],"confidence_badge":"Mediu
...[truncated]...
```

### Query 17: luxury hotel with spa
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury hotel with spa"}'
```
Status: 200
Latency: 46.0ms
Response excerpt:
```json
{"trace_id":"req-23ba8cca","query":"luxury hotel with spa","recommendations":[{"hotel_id":"ChIJlyMMChcHDTkRR-fZqsAQqLc","name":"Spot On 29024 Jageer Palace","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":2.5,"value":0.0},"trust_score":50.0,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.2,"review_evidence":[],"provenance":[],"confidence_badge":"Medium","ratin
...[truncated]...
```

### Query 18: budget hotel near metro
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel near metro"}'
```
Status: 200
Latency: 49.5ms
Response excerpt:
```json
{"trace_id":"req-87d8b97a","query":"budget hotel near metro","recommendations":[{"hotel_id":"ChIJnzfZxyH9DDkRB58ZTRYEcpA","name":"Hotel O By Oyo Heaven Stay","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":0.0},"trust_score":48.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_
...[truncated]...
```

### Query 19: hotel for corporate travel
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel for corporate travel"}'
```
Status: 200
Latency: 47.4ms
Response excerpt:
```json
{"trace_id":"req-07de2347","query":"hotel for corporate travel","recommendations":[{"hotel_id":"ChIJ5V5eFuAHDTkR47MCn7ul_ww","name":"Fabexpress The Maharaja Grand","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":63.2,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.0,"review_evidence":[],"provenance":[],"confidence_badge":"Medium"
...[truncated]...
```

### Query 20: family hotel with large rooms
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel with large rooms"}'
```
Status: 200
Latency: 45.3ms
Response excerpt:
```json
{"trace_id":"req-2c5aabe9","query":"family hotel with large rooms","recommendations":[{"hotel_id":"ChIJa8DmBlkZDTkRmCx2X4Z5BuU","name":"Kohsa7","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":79.8,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.2,"review_evidence":[],"provenance":[],"confidence_badge":"Medium","rating":4.3,"revie
...[truncated]...
```

### Query 21: hotel near Connaught Place with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Connaught Place with breakfast"}'
```
Status: 200
Latency: 68.4ms
Response excerpt:
```json
{"trace_id":"req-1f4b2ac3","query":"hotel near Connaught Place with breakfast","recommendations":[{"hotel_id":"ChIJJZbTaLPiDDkR0iCsQ0HteV4","name":"The Park","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":3.4,"location":3.8,"value":5.0},"trust_score":83.5,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","quer
...[truncated]...
```

### Query 22: clean hotel in Chittaranjan Park
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean hotel in Chittaranjan Park"}'
```
Status: 200
Latency: 64.1ms
Response excerpt:
```json
{"trace_id":"req-311ba6ef","query":"clean hotel in Chittaranjan Park","recommendations":[{"hotel_id":"ChIJ5bX1UNLjDDkRFUd-LjbGr28","name":"Hotel Kastor International","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":81.5,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterio
...[truncated]...
```

### Query 23: couple stay near Saket
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "couple stay near Saket"}'
```
Status: 200
Latency: 51.1ms
Response excerpt:
```json
{"trace_id":"req-9d45132e","query":"couple stay near Saket","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":46.74267768859863,"retrieval_ms":33.125877380371094,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Near Saket,Saket","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 24: business hotel near Sector 57
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotel near Sector 57"}'
```
Status: 200
Latency: 52.6ms
Response excerpt:
```json
{"trace_id":"req-e2d69977","query":"business hotel near Sector 57","recommendations":[{"hotel_id":"ChIJ-d8FwZ4ZDTkRRzTD7epgUdw","name":"Hotel Ashiyana Elite, Near Golf Course Road","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":91.5,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess
...[truncated]...
```

### Query 25: luxury stay near Golf Course Ext Rd
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury stay near Golf Course Ext Rd"}'
```
Status: 200
Latency: 42.2ms
Response excerpt:
```json
{"trace_id":"req-3185df96","query":"luxury stay near Golf Course Ext Rd","recommendations":[{"hotel_id":"ChIJa4Td0z8jDTkRPG1sCr5IS5o","name":"Inde Hotel Golf Course Extention","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":2.5},"trust_score":58.6,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 26: hotel with strong service reviews
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel with strong service reviews"}'
```
Status: 200
Latency: 54.7ms
Response excerpt:
```json
{"trace_id":"req-a5c25b8a","query":"hotel with strong service reviews","recommendations":[{"hotel_id":"ChIJ5V5eFuAHDTkR47MCn7ul_ww","name":"Fabexpress The Maharaja Grand","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":63.2,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.0,"review_evidence":[],"provenance":[],"confidence_badge":"
...[truncated]...
```

### Query 27: hotel with excellent location
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel with excellent location"}'
```
Status: 200
Latency: 59.5ms
Response excerpt:
```json
{"trace_id":"req-9f49d879","query":"hotel with excellent location","recommendations":[{"hotel_id":"ChIJ5V5eFuAHDTkR47MCn7ul_ww","name":"Fabexpress The Maharaja Grand","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":63.2,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.0,"review_evidence":[],"provenance":[],"confidence_badge":"Medi
...[truncated]...
```

### Query 28: hotel with value for money
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel with value for money"}'
```
Status: 200
Latency: 47.2ms
Response excerpt:
```json
{"trace_id":"req-961a0c9b","query":"hotel with value for money","recommendations":[{"hotel_id":"ChIJ5V5eFuAHDTkR47MCn7ul_ww","name":"Fabexpress The Maharaja Grand","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":63.2,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.0,"review_evidence":[],"provenance":[],"confidence_badge":"Medium"
...[truncated]...
```

### Query 29: family hotel in Gurugram with pool
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel in Gurugram with pool"}'
```
Status: 200
Latency: 53.5ms
Response excerpt:
```json
{"trace_id":"req-11c2488b","query":"family hotel in Gurugram with pool","recommendations":[{"hotel_id":"ChIJf4aZlKIZDTkRZvUGFuf-IV4","name":"The Trot Hotel & Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":3.7,"location":3.3,"value":3.3},"trust_score":76.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion."
...[truncated]...
```

### Query 30: budget stay near airport
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget stay near airport"}'
```
Status: 200
Latency: 42.0ms
Response excerpt:
```json
{"trace_id":"req-7f5f411a","query":"budget stay near airport","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","quer
...[truncated]...
```

### Query 31: hotel near Aerocity with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Aerocity with breakfast"}'
```
Status: 200
Latency: 45.4ms
Response excerpt:
```json
{"trace_id":"req-d74b30fe","query":"hotel near Aerocity with breakfast","recommendations":[{"hotel_id":"ChIJ7bfQAnIcDTkR6QuFSvjr3e4","name":"Lemon Tree Hotel, Delhi Airport","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.3,"service":4.5,"location":2.5,"value":3.9},"trust_score":82.6,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 32: hotel near Karol Bagh metro
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Karol Bagh metro"}'
```
Status: 200
Latency: 46.5ms
Response excerpt:
```json
{"trace_id":"req-78d264d3","query":"hotel near Karol Bagh metro","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":41.93425178527832,"retrieval_ms":23.3767032623291,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Karol Bagh,Metro","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 33: clean budget hotel in Delhi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean budget hotel in Delhi"}'
```
Status: 200
Latency: 53.6ms
Response excerpt:
```json
{"trace_id":"req-fa02ada1","query":"clean budget hotel in Delhi","recommendations":[{"hotel_id":"ChIJBb6nI8D9DDkRwrBTMaXlXG4","name":"Hotel Vcr Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":3.0,"location":2.5,"value":2.5},"trust_score":78.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignment
...[truncated]...
```

### Query 34: business stay in New Industrial Township
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business stay in New Industrial Township"}'
```
Status: 200
Latency: 62.9ms
Response excerpt:
```json
{"trace_id":"req-4ad64d46","query":"business stay in New Industrial Township","recommendations":[{"hotel_id":"ChIJQzynNDjcDDkRwyLgZhp-JWY","name":"Cs Boutique Hotel","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":3.8,"location":5.0,"value":5.0},"trust_score":78.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion."
...[truncated]...
```

### Query 35: couple friendly luxury hotel
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "couple friendly luxury hotel"}'
```
Status: 200
Latency: 58.2ms
Response excerpt:
```json
{"trace_id":"req-f91746be","query":"couple friendly luxury hotel","recommendations":[{"hotel_id":"ChIJlyMMChcHDTkRR-fZqsAQqLc","name":"Spot On 29024 Jageer Palace","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":2.5,"value":0.0},"trust_score":50.0,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.2,"review_evidence":[],"provenance":[],"confidence_badge":"Medium"
...[truncated]...
```

### Query 36: hotel near Paharganj for family with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Paharganj for family with breakfast"}'
```
Status: 200
Latency: 56.1ms
Response excerpt:
```json
{"trace_id":"req-c3d741e5","query":"hotel near Paharganj for family with breakfast","recommendations":[{"hotel_id":"ChIJ7zycekH9DDkRWd8FYsIVT3U","name":"Hotel Mother Palace","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.8,"service":2.5,"location":3.5,"value":3.2},"trust_score":72.4,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this cri
...[truncated]...
```

### Query 37: cheap family hotel near Paharganj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "cheap family hotel near Paharganj"}'
```
Status: 200
Latency: 53.9ms
Response excerpt:
```json
{"trace_id":"req-94486f2a","query":"cheap family hotel near Paharganj","recommendations":[{"hotel_id":"ChIJAZTkm0D9DDkRMDezVFMRIKM","name":"The Gold Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":74.3,"explanation_badge":"Verified","ai_match_label":"Excellent","match_reason":"Limited review evidence is available to confidently assess this criterion.","query
...[truncated]...
```

### Query 38: hotel near Preet Vihar with parking
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Preet Vihar with parking"}'
```
Status: 200
Latency: 61.5ms
Response excerpt:
```json
{"trace_id":"req-b5e1e5a5","query":"hotel near Preet Vihar with parking","recommendations":[{"hotel_id":"ChIJDQCwFlb7DDkRc6G99BgmakY","name":"East Inn Hotel","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":5.0,"value":0.0},"trust_score":77.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_
...[truncated]...
```

### Query 39: hotel near Anand Vihar for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Anand Vihar for business"}'
```
Status: 200
Latency: 55.9ms
Response excerpt:
```json
{"trace_id":"req-4592058b","query":"hotel near Anand Vihar for business","recommendations":[{"hotel_id":"ChIJVZv6HQD7DDkRuvanyn__P7A","name":"Qotel Comfort Ip Residency East Delhi Preet Vihar","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":2.5,"location":2.5,"value":0.0},"trust_score":57.5,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confiden
...[truncated]...
```

### Query 40: hotel near Laxmi Nagar with wifi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Laxmi Nagar with wifi"}'
```
Status: 200
Latency: 76.6ms
Response excerpt:
```json
{"trace_id":"req-e2fc952e","query":"hotel near Laxmi Nagar with wifi","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":71.38347625732422,"retrieval_ms":48.27094078063965,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Laxmi Nagar,Nagar","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 41: luxury family hotel in Aerocity
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury family hotel in Aerocity"}'
```
Status: 200
Latency: 65.2ms
Response excerpt:
```json
{"trace_id":"req-cd459aa0","query":"luxury family hotel in Aerocity","recommendations":[{"hotel_id":"ChIJ7bfQAnIcDTkR6QuFSvjr3e4","name":"Lemon Tree Hotel, Delhi Airport","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.3,"service":4.5,"location":2.5,"value":3.9},"trust_score":82.6,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this crit
...[truncated]...
```

### Query 42: budget hotel in Mahipalpur with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel in Mahipalpur with breakfast"}'
```
Status: 200
Latency: 74.6ms
Response excerpt:
```json
{"trace_id":"req-e75bc426","query":"budget hotel in Mahipalpur with breakfast","recommendations":[{"hotel_id":"ChIJp77fqcAdDTkRI_xm4ZpmmOU","name":"Hotel Luxury Stay","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.4,"service":5.0,"location":1.2,"value":1.2},"trust_score":53.3,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.
...[truncated]...
```

### Query 43: business hotel near airport with shuttle
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotel near airport with shuttle"}'
```
Status: 200
Latency: 55.7ms
Response excerpt:
```json
{"trace_id":"req-cab09c26","query":"business hotel near airport with shuttle","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 44: quiet stay in Chhatarpur
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "quiet stay in Chhatarpur"}'
```
Status: 200
Latency: 53.6ms
Response excerpt:
```json
{"trace_id":"req-fa1f28a4","query":"quiet stay in Chhatarpur","recommendations":[{"hotel_id":"ChIJ13o6losfDTkR7ugYxJNGxvo","name":"V Resorts Farm Stay Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":0.0,"location":2.5,"value":2.5},"trust_score":61.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_
...[truncated]...
```

### Query 45: hotel with excellent cleanliness in Rohini
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel with excellent cleanliness in Rohini"}'
```
Status: 200
Latency: 54.2ms
Response excerpt:
```json
{"trace_id":"req-1d84d0a2","query":"hotel with excellent cleanliness in Rohini","recommendations":[{"hotel_id":"ChIJUXyGwzsBDTkRpCTgSan0Boc","name":"Hotel Green Arrow Rohini","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":2.5,"value":2.5},"trust_score":62.4,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this cr
...[truncated]...
```

### Query 46: hotel for weekend stay in Gurugram
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel for weekend stay in Gurugram"}'
```
Status: 200
Latency: 48.7ms
Response excerpt:
```json
{"trace_id":"req-6c84921e","query":"hotel for weekend stay in Gurugram","recommendations":[{"hotel_id":"ChIJ2Q_vUgAhDTkRG9JSfed_m9U","name":"Grand Mantram Resort","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":83.9,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.",
...[truncated]...
```

### Query 47: hotel near Green Park with good service
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Green Park with good service"}'
```
Status: 200
Latency: 58.8ms
Response excerpt:
```json
{"trace_id":"req-5504eeca","query":"hotel near Green Park with good service","recommendations":[{"hotel_id":"ChIJ9Xii03PiDDkRFaoIddnxtns","name":"Hotel Park Residency","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":3.3,"location":5.0,"value":1.7},"trust_score":65.3,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion
...[truncated]...
```

### Query 48: affordable hotel near Kalkaji
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "affordable hotel near Kalkaji"}'
```
Status: 200
Latency: 60.2ms
Response excerpt:
```json
{"trace_id":"req-e554faa1","query":"affordable hotel near Kalkaji","recommendations":[{"hotel_id":"ChIJ-UnEBH7jDDkRhJaGrJjZF4Y","name":"The Orion Plaza Nehru Place","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":0.0,"location":3.7,"value":3.3},"trust_score":79.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.",
...[truncated]...
```

### Query 49: hotel near Connaught Place for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Connaught Place for business"}'
```
Status: 200
Latency: 60.1ms
Response excerpt:
```json
{"trace_id":"req-d04f35e2","query":"hotel near Connaught Place for business","recommendations":[{"hotel_id":"ChIJu2YFVjb9DDkR0KTtXpZwXtA","name":"The Corus Hotel","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":78.5,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","q
...[truncated]...
```

### Query 50: family hotel near Greater Kailash
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Greater Kailash"}'
```
Status: 200
Latency: 66.3ms
Response excerpt:
```json
{"trace_id":"req-488cc100","query":"family hotel near Greater Kailash","recommendations":[{"hotel_id":"ChIJNSFmGzPiDDkRIiHvp6YOd1c","name":"Amara Hotel","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":85.6,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_ali
...[truncated]...
```

### Query 51: hotel near Safdarjung Enclave with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Safdarjung Enclave with breakfast"}'
```
Status: 200
Latency: 71.3ms
Response excerpt:
```json
{"trace_id":"req-1496bb9d","query":"hotel near Safdarjung Enclave with breakfast","recommendations":[{"hotel_id":"ChIJ0YSsSrcdDTkRPyej8NVwQ3E","name":"Fabhotel Veetara - Hotel In Safdarjung Enclave, New Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":1.8,"location":2.5,"value":0.0},"trust_score":41.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is avai
...[truncated]...
```

### Query 52: premium stay in Chanakyapuri
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "premium stay in Chanakyapuri"}'
```
Status: 200
Latency: 52.6ms
Response excerpt:
```json
{"trace_id":"req-1425ffae","query":"premium stay in Chanakyapuri","recommendations":[{"hotel_id":"ChIJ76JImg0dDTkRVUXq0b3XW0A","name":"Embassy Suites Chankya Puri","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":1.8,"value":2.5},"trust_score":48.3,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","
...[truncated]...
```

### Query 53: budget hotel near Civil Lines
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel near Civil Lines"}'
```
Status: 200
Latency: 56.1ms
Response excerpt:
```json
{"trace_id":"req-bfe7f809","query":"budget hotel near Civil Lines","recommendations":[{"hotel_id":"ChIJC3jSkMLnDDkRpbyJHHT6HjY","name":"Fabhotel Crescent","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":0.0},"trust_score":34.7,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.2,"review_evidence":[],"provenance":[],"confidence_badge":"Medium","rating"
...[truncated]...
```

### Query 54: couple hotel near Hauz Khas
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "couple hotel near Hauz Khas"}'
```
Status: 200
Latency: 48.6ms
Response excerpt:
```json
{"trace_id":"req-aecb3a5d","query":"couple hotel near Hauz Khas","recommendations":[{"hotel_id":"ChIJTYaPJtkdDTkRueyL3cN2yXA","name":"Minimalist Poshtel & Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":1.7,"service":2.5,"location":2.5,"value":1.3},"trust_score":64.5,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","q
...[truncated]...
```

### Query 55: hotel with pool and gym in Gurugram
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel with pool and gym in Gurugram"}'
```
Status: 200
Latency: 43.7ms
Response excerpt:
```json
{"trace_id":"req-1c087081","query":"hotel with pool and gym in Gurugram","recommendations":[{"hotel_id":"ChIJf4aZlKIZDTkRZvUGFuf-IV4","name":"The Trot Hotel & Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.7,"service":3.7,"location":3.3,"value":3.3},"trust_score":76.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.
...[truncated]...
```

### Query 56: hotel near Sector 49 with wifi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 49 with wifi"}'
```
Status: 200
Latency: 47.8ms
Response excerpt:
```json
{"trace_id":"req-1a278b69","query":"hotel near Sector 49 with wifi","recommendations":[{"hotel_id":"ChIJganRVJAjDTkRuq61WMKx4NQ","name":"Rjk Stay Stay In Style","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":89.2,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","q
...[truncated]...
```

### Query 57: hotel near Sector 53 with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 53 with breakfast"}'
```
Status: 200
Latency: 48.3ms
Response excerpt:
```json
{"trace_id":"req-15f9906c","query":"hotel near Sector 53 with breakfast","recommendations":[{"hotel_id":"ChIJ-_yRL8EZDTkRpKoCJVWyNKU","name":"Blue Moon Residency","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":1.6,"location":2.5,"value":4.9},"trust_score":75.9,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","q
...[truncated]...
```

### Query 58: hotel near Sector 39 for family
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 39 for family"}'
```
Status: 200
Latency: 50.8ms
Response excerpt:
```json
{"trace_id":"req-5692e288","query":"hotel near Sector 39 for family","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":44.81816291809082,"retrieval_ms":22.55725860595703,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Sector 39,Sector 3","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 59: clean hotel in New Delhi under budget
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean hotel in New Delhi under budget"}'
```
Status: 200
Latency: 51.7ms
Response excerpt:
```json
{"trace_id":"req-4544d82e","query":"clean hotel in New Delhi under budget","recommendations":[{"hotel_id":"ChIJBb6nI8D9DDkRwrBTMaXlXG4","name":"Hotel Vcr Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":3.0,"location":2.5,"value":2.5},"trust_score":78.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query
...[truncated]...
```

### Query 60: luxury business hotel in Delhi NCR
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury business hotel in Delhi NCR"}'
```
Status: 200
Latency: 55.5ms
Response excerpt:
```json
{"trace_id":"req-8dea7425","query":"luxury business hotel in Delhi NCR","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":51.71990394592285,"retrieval_ms":26.319265365600586,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Delhi Ncr,Delhi NCR,Ncr","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 61: hotel near airport with high trust score
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near airport with high trust score"}'
```
Status: 200
Latency: 58.4ms
Response excerpt:
```json
{"trace_id":"req-5440dde8","query":"hotel near airport with high trust score","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 62: family hotel near Dwarka with parking
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Dwarka with parking"}'
```
Status: 200
Latency: 57.6ms
Response excerpt:
```json
{"trace_id":"req-271300c9","query":"family hotel near Dwarka with parking","recommendations":[{"hotel_id":"ChIJFT23yP8bDTkRm65IVfSQIsk","name":"Hideaway Bed And Breakfast","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":86.8,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this cri
...[truncated]...
```

### Query 63: hotel near Shahdara with good reviews
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Shahdara with good reviews"}'
```
Status: 200
Latency: 50.2ms
Response excerpt:
```json
{"trace_id":"req-42443fc8","query":"hotel near Shahdara with good reviews","recommendations":[{"hotel_id":"ChIJ9zJVVgD7DDkRWOQxBwWX3G4","name":"The Aura Hotel & Banquet","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":5.0,"value":2.5},"trust_score":60.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criteri
...[truncated]...
```

### Query 64: hotel near Paschim Vihar for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Paschim Vihar for business"}'
```
Status: 200
Latency: 57.6ms
Response excerpt:
```json
{"trace_id":"req-d3fdafaf","query":"hotel near Paschim Vihar for business","recommendations":[{"hotel_id":"ChIJPQR11mkEDTkRFscLu0VKDTE","name":"Twamev Residency","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":5.0,"location":2.5,"value":0.0},"trust_score":80.7,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","
...[truncated]...
```

### Query 65: budget hotel near Uttam Nagar metro
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel near Uttam Nagar metro"}'
```
Status: 200
Latency: 63.2ms
Response excerpt:
```json
{"trace_id":"req-f4601a91","query":"budget hotel near Uttam Nagar metro","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":58.38751792907715,"retrieval_ms":23.65255355834961,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Uttam Nagar,Metro,Nagar","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 66: hotel near Malviya Nagar with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Malviya Nagar with breakfast"}'
```
Status: 200
Latency: 60.3ms
Response excerpt:
```json
{"trace_id":"req-ab5a8247","query":"hotel near Malviya Nagar with breakfast","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":55.77707290649414,"retrieval_ms":23.849010467529297,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Malviya Nagar,Nagar","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 67: hotel near Chittaranjan Park for family
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Chittaranjan Park for family"}'
```
Status: 200
Latency: 52.3ms
Response excerpt:
```json
{"trace_id":"req-94194300","query":"hotel near Chittaranjan Park for family","recommendations":[{"hotel_id":"ChIJ5bX1UNLjDDkRFUd-LjbGr28","name":"Hotel Kastor International","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":81.5,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 68: business hotel near Jasola Vihar
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotel near Jasola Vihar"}'
```
Status: 200
Latency: 54.2ms
Response excerpt:
```json
{"trace_id":"req-bd4addfc","query":"business hotel near Jasola Vihar","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":50.562381744384766,"retrieval_ms":27.263402938842773,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Jasola Vihar,Asola","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 69: luxury stay near Vasant Kunj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury stay near Vasant Kunj"}'
```
Status: 200
Latency: 40.0ms
Response excerpt:
```json
{"trace_id":"req-f9f5b378","query":"luxury stay near Vasant Kunj","recommendations":[{"hotel_id":"ChIJB-shS9_jDDkRQQSbddJ0GOU","name":"The Grand New Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":5.0,"value":2.5},"trust_score":86.3,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_
...[truncated]...
```

### Query 70: affordable hotel near Aerocity
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "affordable hotel near Aerocity"}'
```
Status: 200
Latency: 49.0ms
Response excerpt:
```json
{"trace_id":"req-7a31bb4b","query":"affordable hotel near Aerocity","recommendations":[{"hotel_id":"ChIJ7bfQAnIcDTkR6QuFSvjr3e4","name":"Lemon Tree Hotel, Delhi Airport","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.3,"service":4.5,"location":2.5,"value":3.9},"trust_score":82.6,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this crite
...[truncated]...
```

### Query 71: hotel near Sector 45 with pool
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 45 with pool"}'
```
Status: 200
Latency: 42.5ms
Response excerpt:
```json
{"trace_id":"req-8e485f8c","query":"hotel near Sector 45 with pool","recommendations":[{"hotel_id":"ChIJS4Ok5QoZDTkRvuSk45jH_qw","name":"Hotel Sakura By Maps Group","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":1.2,"location":0.0,"value":2.5},"trust_score":61.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.",
...[truncated]...
```

### Query 72: hotel near Sector 42 for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 42 for business"}'
```
Status: 200
Latency: 46.7ms
Response excerpt:
```json
{"trace_id":"req-d7e6d3a8","query":"hotel near Sector 42 for business","recommendations":[{"hotel_id":"ChIJC-svMT7nDDkRsnPyEfm6MSM","name":"Agrah Stay","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":83.7,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alig
...[truncated]...
```

### Query 73: family hotel near Sector 31
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Sector 31"}'
```
Status: 200
Latency: 50.3ms
Response excerpt:
```json
{"trace_id":"req-a0809c58","query":"family hotel near Sector 31","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":47.21212387084961,"retrieval_ms":23.628711700439453,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Sector 31,Sector 3","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 74: clean hotel near Sector 14
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean hotel near Sector 14"}'
```
Status: 200
Latency: 48.7ms
Response excerpt:
```json
{"trace_id":"req-85bae170","query":"clean hotel near Sector 14","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":43.988704681396484,"retrieval_ms":21.84891700744629,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Sector 14,Sector 1","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 75: hotel near Kaushambi with wifi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Kaushambi with wifi"}'
```
Status: 200
Latency: 44.2ms
Response excerpt:
```json
{"trace_id":"req-b9c0bde2","query":"hotel near Kaushambi with wifi","recommendations":[{"hotel_id":"ChIJ9f5mdiv7DDkRq-mRrFelJAo","name":"Radisson Blu Hotel, Kaushambi Delhi Ncr","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":96.1,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess th
...[truncated]...
```

### Query 76: hotel near Surajkund with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Surajkund with breakfast"}'
```
Status: 200
Latency: 48.2ms
Response excerpt:
```json
{"trace_id":"req-80f545da","query":"hotel near Surajkund with breakfast","recommendations":[{"hotel_id":"ChIJq6qqqg3cDDkRcNh5dl8gb9c","name":"Taj Surajkund Resort & Spa, Delhi Ncr","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":3.3,"location":2.5,"value":0.0},"trust_score":88.1,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess
...[truncated]...
```

### Query 77: budget hotel near Green Park
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel near Green Park"}'
```
Status: 200
Latency: 47.9ms
Response excerpt:
```json
{"trace_id":"req-075c12f9","query":"budget hotel near Green Park","recommendations":[{"hotel_id":"ChIJT1_dZwDjDDkRnebfK5pM3Es","name":"South Inn - Green Park South Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.0,"service":0.0,"location":3.7,"value":5.0},"trust_score":79.8,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criter
...[truncated]...
```

### Query 78: hotel near Safdarjung Enclave for couple
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Safdarjung Enclave for couple"}'
```
Status: 200
Latency: 60.4ms
Response excerpt:
```json
{"trace_id":"req-795061ed","query":"hotel near Safdarjung Enclave for couple","recommendations":[{"hotel_id":"ChIJ0YSsSrcdDTkRPyej8NVwQ3E","name":"Fabhotel Veetara - Hotel In Safdarjung Enclave, New Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":1.8,"location":2.5,"value":0.0},"trust_score":41.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is availabl
...[truncated]...
```

### Query 79: luxury hotel near Chanakyapuri with spa
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury hotel near Chanakyapuri with spa"}'
```
Status: 200
Latency: 70.5ms
Response excerpt:
```json
{"trace_id":"req-824de644","query":"luxury hotel near Chanakyapuri with spa","recommendations":[{"hotel_id":"ChIJe4zp0KMdDTkRm90YLrHBVg8","name":"Taj Palace, New Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.9,"service":4.2,"location":5.0,"value":0.9},"trust_score":95.2,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criter
...[truncated]...
```

### Query 80: business hotel near Noida border
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotel near Noida border"}'
```
Status: 200
Latency: 80.4ms
Response excerpt:
```json
{"trace_id":"req-3e8f23e7","query":"business hotel near Noida border","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":74.73182678222656,"retrieval_ms":39.82877731323242,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Border,Noida","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 81: family hotel near Faridabad
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Faridabad"}'
```
Status: 200
Latency: 56.9ms
Response excerpt:
```json
{"trace_id":"req-bc97f19b","query":"family hotel near Faridabad","recommendations":[{"hotel_id":"ChIJJfVl6mnfDDkRF7gDYYhtgvE","name":"Aravali Marriott Resort & Spa, Delhi Ncr","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.7,"service":0.0,"location":2.5,"value":2.5},"trust_score":53.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this c
...[truncated]...
```

### Query 82: hotel near Old Faridabad with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Old Faridabad with breakfast"}'
```
Status: 200
Latency: 49.8ms
Response excerpt:
```json
{"trace_id":"req-aac8b6e9","query":"hotel near Old Faridabad with breakfast","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":45.978546142578125,"retrieval_ms":20.052194595336914,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Old Faridabad,Faridabad,Old","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 83: hotel near Ajronda with parking
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Ajronda with parking"}'
```
Status: 200
Latency: 53.9ms
Response excerpt:
```json
{"trace_id":"req-c1d6189e","query":"hotel near Ajronda with parking","recommendations":[{"hotel_id":"ChIJ3ydPH0rcDDkRphpP8-WHB1c","name":"Crown Residency","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":0.0},"trust_score":37.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_ali
...[truncated]...
```

### Query 84: hotel near Sector 60 for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Sector 60 for business"}'
```
Status: 200
Latency: 48.1ms
Response excerpt:
```json
{"trace_id":"req-5b1f41c2","query":"hotel near Sector 60 for business","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":43.78819465637207,"retrieval_ms":21.471500396728516,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Sector 60,Sector 6","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 85: clean hotel near Sector 16A
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "clean hotel near Sector 16A"}'
```
Status: 200
Latency: 47.5ms
Response excerpt:
```json
{"trace_id":"req-fd0ad45f","query":"clean hotel near Sector 16A","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":43.209075927734375,"retrieval_ms":21.56853675842285,"compression_ms":0,"llm_ms":0,"fallback_level":2,"cache_hit":false,"is_fallback":false,"target_area":"Sector 16A,Sector 1","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 86: hotel near DLF Phase IV with pool
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near DLF Phase IV with pool"}'
```
Status: 200
Latency: 42.7ms
Response excerpt:
```json
{"trace_id":"req-321091da","query":"hotel near DLF Phase IV with pool","recommendations":[{"hotel_id":"ChIJPZDGPtsYDTkRAw_YJKEwTiE","name":"Hotel City Premier","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":79.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","quer
...[truncated]...
```

### Query 87: budget hotel near Mukherjee Nagar
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "budget hotel near Mukherjee Nagar"}'
```
Status: 200
Latency: 61.8ms
Response excerpt:
```json
{"trace_id":"req-16bc9b95","query":"budget hotel near Mukherjee Nagar","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":56.787729263305664,"retrieval_ms":24.028778076171875,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Mukherjee Nagar,Nagar","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}}
```

### Query 88: family hotel near Model Town
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Model Town"}'
```
Status: 200
Latency: 44.6ms
Response excerpt:
```json
{"trace_id":"req-582da8d8","query":"family hotel near Model Town","recommendations":[{"hotel_id":"ChIJm-_MRdgJDTkRaZlhQn1wdRo","name":"Star Hotel","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":2.5,"value":0.0},"trust_score":66.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alignment_s
...[truncated]...
```

### Query 89: hotel near Rajendra Place with wifi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Rajendra Place with wifi"}'
```
Status: 200
Latency: 44.5ms
Response excerpt:
```json
{"trace_id":"req-1c7694e3","query":"hotel near Rajendra Place with wifi","recommendations":[{"hotel_id":"ChIJY6Gyi5UCDTkRmjXmCUzwY6w","name":"Jaypee Siddharth - 5 Star Luxury Hotels In Delhi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":3.3,"location":2.5,"value":2.5},"trust_score":85.3,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confide
...[truncated]...
```

### Query 90: hotel near Rajouri Garden for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Rajouri Garden for business"}'
```
Status: 200
Latency: 48.9ms
Response excerpt:
```json
{"trace_id":"req-52105532","query":"hotel near Rajouri Garden for business","recommendations":[{"hotel_id":"ChIJx2G4jXwDDTkRHWHRAX90qJg","name":"Malbork Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":3.5,"service":4.4,"location":5.0,"value":5.0},"trust_score":78.9,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_
...[truncated]...
```

### Query 91: luxury stay near Saket District Centre
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury stay near Saket District Centre"}'
```
Status: 200
Latency: 58.8ms
Response excerpt:
```json
{"trace_id":"req-9fcea17f","query":"luxury stay near Saket District Centre","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":54.60548400878906,"retrieval_ms":23.92578125,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Saket District Centre,Near Saket,Saket","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."
...[truncated]...
```

### Query 92: hotel near Mahipalpur with shuttle
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Mahipalpur with shuttle"}'
```
Status: 200
Latency: 49.1ms
Response excerpt:
```json
{"trace_id":"req-1fffe421","query":"hotel near Mahipalpur with shuttle","recommendations":[{"hotel_id":"ChIJBb3mYrQdDTkRv0Dx43jGpGQ","name":"Hotel Urban Tree","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":0.0},"trust_score":67.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query
...[truncated]...
```

### Query 93: hotel near Airport Terminal 3
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Airport Terminal 3"}'
```
Status: 200
Latency: 51.0ms
Response excerpt:
```json
{"trace_id":"req-105ef6ec","query":"hotel near Airport Terminal 3","recommendations":[{"hotel_id":"ChIJWT9tW5AdDTkRrVM7VtKZjw8","name":"Airport Hotel Royal Inn Igi","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":1.3},"trust_score":71.1,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.",
...[truncated]...
```

### Query 94: affordable hotel near Sarita Vihar
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "affordable hotel near Sarita Vihar"}'
```
Status: 200
Latency: 52.4ms
Response excerpt:
```json
{"trace_id":"req-31fd2d51","query":"affordable hotel near Sarita Vihar","recommendations":[{"hotel_id":"ChIJlauOOPLnDDkRAsLWG3XzNmg","name":"Hotel Shyam Palace","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":1.3,"service":2.5,"location":5.0,"value":2.5},"trust_score":52.7,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","que
...[truncated]...
```

### Query 95: business hotel near Okhla Industrial Estate
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "business hotel near Okhla Industrial Estate"}'
```
Status: 200
Latency: 67.2ms
Response excerpt:
```json
{"trace_id":"req-043220f6","query":"business hotel near Okhla Industrial Estate","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":62.9122257232666,"retrieval_ms":25.229454040527344,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Okhla Industrial Estate,Okhla","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters
...[truncated]...
```

### Query 96: family hotel near Greater Kailash II
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotel near Greater Kailash II"}'
```
Status: 200
Latency: 49.6ms
Response excerpt:
```json
{"trace_id":"req-3a649ec5","query":"family hotel near Greater Kailash II","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":45.3648567199707,"retrieval_ms":22.27187156677246,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"Greater Kailash Ii,Greater Kailash","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels that reliably match your request. Try broadening the location or removing one or more filters."}
...[truncated]...
```

### Query 97: hotel near Tughlakabad with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Tughlakabad with breakfast"}'
```
Status: 200
Latency: 54.2ms
Response excerpt:
```json
{"trace_id":"req-46601cac","query":"hotel near Tughlakabad with breakfast","recommendations":[{"hotel_id":"ChIJoxuvkn_hDDkRxd31OthoEt8","name":"Hotel O My Comfortable","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":0.0,"location":2.5,"value":0.0},"trust_score":25.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion
...[truncated]...
```

### Query 98: hotel near New Friends Colony for business
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near New Friends Colony for business"}'
```
Status: 200
Latency: 51.4ms
Response excerpt:
```json
{"trace_id":"req-43399bb7","query":"hotel near New Friends Colony for business","recommendations":[{"hotel_id":"ChIJIQRNwakFDTkRRR6RxHgzr8M","name":"Hazel Town House","summary_text":"Showing nearby alternatives.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":3.4,"value":5.0},"trust_score":76.8,"explanation_badge":"Nearby","ai_match_label":"Partial","match_reason":"Showing nearby alternatives.","query_alignment_score":0.2,"review_evidence":[],"provenance":[],"confidence_badge":"Medi
...[truncated]...
```

### Query 99: luxury hotel near South Delhi
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "luxury hotel near South Delhi"}'
```
Status: 200
Latency: 59.0ms
Response excerpt:
```json
{"trace_id":"req-ed9ba4d9","query":"luxury hotel near South Delhi","recommendations":[{"hotel_id":"ChIJn4gzI1ziDDkR9O77oIjkc7E","name":"Skylink Suites","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":80.2,"explanation_badge":"Top Choice","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_alig
...[truncated]...
```

### Query 100: hotel near Connaught Circus with good cleanliness
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel near Connaught Circus with good cleanliness"}'
```
Status: 200
Latency: 60.2ms
Response excerpt:
```json
{"trace_id":"req-c70a57ad","query":"hotel near Connaught Circus with good cleanliness","recommendations":[{"hotel_id":"ChIJLfHmQTf9DDkRvr36v6n2Heg","name":"Hotel Jukaso Down Town","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":2.5,"service":3.7,"location":3.8,"value":5.0},"trust_score":63.2,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess th
...[truncated]...
```

## Catalog Audit (100 Queries)
### Area 1: New Delhi
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=New%20Delhi&limit=20"
```
Status: 200
Latency: 6.3ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJY6PJh2kcDTkRybb5KBGcqIY","name":"Ibis New Delhi Aerocity","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":97.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area"
...[truncated]...
```

### Area 2: Rohini
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Rohini&limit=20"
```
Status: 200
Latency: 5.9ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJTZYJvY8BDTkRMqD9vfIeu3I","name":"Skymax Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":94.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price":null,"area":"Rohini","
...[truncated]...
```

### Area 3: Mahipalpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Mahipalpur&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJAQAAMLD-DDkRdPtt8LsVujA","name":"Radisson Blu Plaza Hotel, Delhi Airport","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":99.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"pr
...[truncated]...
```

### Area 4: Gurugram
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Gurugram&limit=20"
```
Status: 200
Latency: 5.8ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ845-Av8hDTkR92215ULZUa0","name":"Doubletree By Hilton Hotel Gurgaon - New Delhi Ncr","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":5.0,"value":2.5},"trust_score":96.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_c
...[truncated]...
```

### Area 5: Paharganj
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Paharganj&limit=20"
```
Status: 200
Latency: 4.9ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJfZabjD_9DDkR0siMJiwLzR8","name":"Hotel Ajanta - Free Airport Pick Up Service","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":4.8,"location":5.0,"value":5.0},"trust_score":94.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0
...[truncated]...
```

### Area 6: Dwarka
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Dwarka&limit=20"
```
Status: 200
Latency: 4.7ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJUXEBCwAbDTkReAT2lErQcEA","name":"Hotel Dwarka Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":89.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"Dwark
...[truncated]...
```

### Area 7: New Industrial Township
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=New%20Industrial%20Township&limit=20"
```
Status: 200
Latency: 5.4ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ91zeLwDdDDkReFhf0mek_RM","name":"Hotel Amar Palace","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":91.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"New 
...[truncated]...
```

### Area 8: Delhi
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Delhi&limit=20"
```
Status: 200
Latency: 5.2ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJY6PJh2kcDTkRybb5KBGcqIY","name":"Ibis New Delhi Aerocity","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":97.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area"
...[truncated]...
```

### Area 9: Karol Bagh
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Karol%20Bagh&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJy2cTCzADDTkRQf0Uee9-tZ4","name":"Alaya Stays By Elivaas Emperor Palms - Hotel In Delhi","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":94.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"review
...[truncated]...
```

### Area 10: Shahdara
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Shahdara&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJs28LAX_7DDkRyHzGDbAs6YM","name":"Park Plaza Delhi Cbd Shahdara","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":90.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0,"price":null,
...[truncated]...
```

### Area 11: Sector 43
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2043&limit=20"
```
Status: 200
Latency: 4.1ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJdb2nSwwZDTkR_qFicz-CfPw","name":"Bloom Hotel - Golf Course Road, Sector 43","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":95.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"
...[truncated]...
```

### Area 12: Imt Manesar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Imt%20Manesar&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJda6QOks8DTkRSYPBnAZZFs8","name":"Savoy Suites, Manesar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":93.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area":"
...[truncated]...
```

### Area 13: Chhatarpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Chhatarpur&limit=20"
```
Status: 200
Latency: 5.4ms
Returned: 18 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJh45apMkfDTkRsVm3VhUXE74","name":"Opulent Hotel By Ferns N Petals","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":92.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":nul
...[truncated]...
```

### Area 14: Loni
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Loni&limit=20"
```
Status: 200
Latency: 5.8ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJxTh6dqD_DDkRcDRMltyZr8E","name":"Hotel D K Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":91.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price":null,"area":"Lo
...[truncated]...
```

### Area 15: Sector 53
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2053&limit=20"
```
Status: 200
Latency: 5.2ms
Returned: 17 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJM1VXRjQZDTkRoBS-7Y_b8qY","name":"Ibis Gurgaon Golf Course Road","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":94.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count":0,"price":null,
...[truncated]...
```

### Area 16: Sector 38
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2038&limit=20"
```
Status: 200
Latency: 4.5ms
Returned: 17 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJFXWsgMwZDTkRvXpQTNJyZlM","name":"The Lodgers Hotel - Hotel Near Medanta Medicity Sector 38","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":92.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"re
...[truncated]...
```

### Area 17: Manesar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Manesar&limit=20"
```
Status: 200
Latency: 4.8ms
Returned: 20 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJda6QOks8DTkRSYPBnAZZFs8","name":"Savoy Suites, Manesar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":93.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area":"
...[truncated]...
```

### Area 18: Paschim Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Paschim%20Vihar&limit=20"
```
Status: 200
Latency: 3.8ms
Returned: 16 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJXdmXL30EDTkR5YJTrNiByBs","name":"Hotel Picasso - Paschim Vihar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":85.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.1,"reviews_count":0,"price":null,
...[truncated]...
```

### Area 19: Sector 57
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2057&limit=20"
```
Status: 200
Latency: 3.8ms
Returned: 16 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJSfZsve4ZDTkR-sn6fGbQcH0","name":"Limewood Signature - Near Golf Course Road","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":96.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,
...[truncated]...
```

### Area 20: Burari
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Burari&limit=20"
```
Status: 200
Latency: 16.5ms
Returned: 15 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJedUlZhz_DDkRt5q5eHsolr0","name":"Hotel O Evergreen Hotels","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":2.5,"value":2.5},"trust_score":86.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area
...[truncated]...
```

### Area 21: Sahibabad
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sahibabad&limit=20"
```
Status: 200
Latency: 15.2ms
Returned: 14 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJUdP3Rpb7DDkRtlGlfq_41wA","name":"Sk Klyde Grand","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":5.0,"value":2.5},"trust_score":94.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Sahibab
...[truncated]...
```

### Area 22: Sector 45
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2045&limit=20"
```
Status: 200
Latency: 4.9ms
Returned: 14 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJS49M_lcZDTkRKyK8H7uO5Gc","name":"Flora Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":96.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"Sector
...[truncated]...
```

### Area 23: Sector 39
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2039&limit=20"
```
Status: 200
Latency: 5.4ms
Returned: 13 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJtaHuZ1AZDTkRyrznyfcQis8","name":"Hotel Singh Residency Medanta-Best Hotel Near Medanta Hospital Gurgaon","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":91.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","ra
...[truncated]...
```

### Area 24: Jasola Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Jasola%20Vihar&limit=20"
```
Status: 200
Latency: 19.3ms
Returned: 12 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJQQAAUALkDDkRPlvxqRwJGJo","name":"The Sentinel Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":85.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.1,"reviews_count":0,"price":null,"area":"Jas
...[truncated]...
```

### Area 25: Malviya Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Malviya%20Nagar&limit=20"
```
Status: 200
Latency: 15.2ms
Returned: 12 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJLQysRQDhDDkRwKEOpvjvpK8","name":"Urban Oasis","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":91.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"Malviya Na
...[truncated]...
```

### Area 26: Narela
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Narela&limit=20"
```
Status: 200
Latency: 3.7ms
Returned: 13 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJV74mnnepDTkRmASnP8cOCy4","name":"Oyo 75433 Viraj Deluxe","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":69.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.5,"reviews_count":0,"price":null,"area":
...[truncated]...
```

### Area 27: Adarsh Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Adarsh%20Nagar&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 12 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJLTUFPQABDTkR2v6CmEIy83o","name":"Hotel 24 Star Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":93.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price":null,"area":"Adar
...[truncated]...
```

### Area 28: Greater Kailash
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Greater%20Kailash&limit=20"
```
Status: 200
Latency: 22.5ms
Returned: 12 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJtaq-A5zjDDkRhbzhTkwimYg","name":"Bloom Hotel - Gk2","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":92.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Grea
...[truncated]...
```

### Area 29: Chittaranjan Park
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Chittaranjan%20Park&limit=20"
```
Status: 200
Latency: 14.2ms
Returned: 11 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJl0oXUXPjDDkRr7CX9nQK4Hk","name":"The Nuvon Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":93.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"Ch
...[truncated]...
```

### Area 30: Sector 31
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2031&limit=20"
```
Status: 200
Latency: 15.2ms
Returned: 10 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJL2zf1n8ZDTkRrIjmGANW7ks","name":"Fabhotel Raahi Retreat Hotel In Sector 31","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":90.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"
...[truncated]...
```

### Area 31: Sector 14
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2014&limit=20"
```
Status: 200
Latency: 5.1ms
Returned: 10 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJj9ohA_sZDTkRzpldRlEu7O8","name":"Zen Suites - Gurgaon","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":93.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"S
...[truncated]...
```

### Area 32: Uttam Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Uttam%20Nagar&limit=20"
```
Status: 200
Latency: 4.6ms
Returned: 10 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJuU4UWSEFDTkR_sveAJgD2-g","name":"Hotel O By Oyo Small Town","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":2.5,"value":2.5},"trust_score":78.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"are
...[truncated]...
```

### Area 33: Najafgarh
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Najafgarh&limit=20"
```
Status: 200
Latency: 4.8ms
Returned: 9 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJl_cOl7gPDTkR41IRTkO4u-I","name":"Hotel Taj Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":87.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Na
...[truncated]...
```

### Area 34: Sultanpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sultanpur&limit=20"
```
Status: 200
Latency: 5.1ms
Returned: 10 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJi147UAAVDTkRWcXTa5zs4h4","name":"Jmd Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":89.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"Sultanpur ro
...[truncated]...
```

### Area 35: Sector 27
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2027&limit=20"
```
Status: 200
Latency: 4.7ms
Returned: 9 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJNWPPK70ZDTkRn_uuCZyjmRY","name":"Saltstayz Premier - Galleria Market Road & Sector 27","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.8,"service":3.8,"location":3.3,"value":0.0},"trust_score":89.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews
...[truncated]...
```

### Area 36: Civil Lines
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Civil%20Lines&limit=20"
```
Status: 200
Latency: 21.4ms
Returned: 9 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJsTX1574ZDTkRYBEzBecVO8s","name":"Hotel O S K Resisdency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":2.5,"value":2.5},"trust_score":86.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":
...[truncated]...
```

### Area 37: Budh Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Budh%20Vihar&limit=20"
```
Status: 200
Latency: 15.0ms
Returned: 8 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ77AkL1sHDTkRckJGkQC1VuY","name":"Hotel O R G Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":82.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count":0,"price":null,"area":"Budh
...[truncated]...
```

### Area 38: Sector 11
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2011&limit=20"
```
Status: 200
Latency: 4.5ms
Returned: 9 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJE51owZ0ZDTkR2OgJJr4sDsI","name":"Hotel O Shree Jee Inn Guest House","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":88.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":n
...[truncated]...
```

### Area 39: Kalkaji
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Kalkaji&limit=20"
```
Status: 200
Latency: 25.5ms
Returned: 9 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJNaMuONvjDDkRv5D1tbP4bIE","name":"The Bed And Rock","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":90.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"price":null,"area":"Kalka
...[truncated]...
```

### Area 40: Surajkund
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Surajkund&limit=20"
```
Status: 200
Latency: 15.5ms
Returned: 8 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJq6qqqg3cDDkRcNh5dl8gb9c","name":"Taj Surajkund Resort & Spa, Delhi Ncr","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":3.3,"location":2.5,"value":0.0},"trust_score":88.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count":0,"pric
...[truncated]...
```

### Area 41: Nawada
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Nawada&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJNU3GbwAFDTkRd1SNKICWQos","name":"Hotel Rs Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":86.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"Naw
...[truncated]...
```

### Area 42: Green Park
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Green%20Park&limit=20"
```
Status: 200
Latency: 3.8ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJyd-sPQDjDDkRfRiRKD5GJXg","name":"Hotel Green Galaxy Green Park South Delhi","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.3,"service":2.5,"location":3.3,"value":5.0},"trust_score":87.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"
...[truncated]...
```

### Area 43: Sector 56
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2056&limit=20"
```
Status: 200
Latency: 4.0ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJed7uWW4jDTkRqkxrKc2dId0","name":"Vamsor Heights","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":95.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"area":"Sector 
...[truncated]...
```

### Area 44: Azadpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Azadpur&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJdXj1neQBDTkRe6C6ogZuxoU","name":"Via Luxury Inn Adarsh Nagar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":1.7,"service":0.0,"location":2.5,"value":2.5},"trust_score":70.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.3,"reviews_count":0,"price":null,"a
...[truncated]...
```

### Area 45: Sector 12
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2012&limit=20"
```
Status: 200
Latency: 29.2ms
Returned: 10 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJAQAAwMoZDTkRW9hrHxvXr20","name":"Country Inn & Suites By Radisson, Gurgaon Sector 12","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":4.4,"service":4.8,"location":2.5,"value":2.5},"trust_score":92.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_
...[truncated]...
```

### Area 46: Kaushambi
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Kaushambi&limit=20"
```
Status: 200
Latency: 16.6ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJExG1eyD7DDkRL_OZpZYiyHE","name":"Radisson Blu Towers Kaushambi Delhi Ncr","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":98.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"pr
...[truncated]...
```

### Area 47: Safdarjung Enclave
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Safdarjung%20Enclave&limit=20"
```
Status: 200
Latency: 4.2ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJKfbCnXodDTkRoHUFJ9xu2HQ","name":"Hotel Corporate Guest House","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":90.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":null,"a
...[truncated]...
```

### Area 48: Sector 42
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2042&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJgSqaay0ZDTkR76AdQCpsw1s","name":"Saltstayz Premier Sector 42 - Golf Course Road","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":94.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count
...[truncated]...
```

### Area 49: Sector 24
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2024&limit=20"
```
Status: 200
Latency: 20.7ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJZSmFMJkZDTkRohYgeUnNxxI","name":"Mod Avenue","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":90.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Sector 24",
...[truncated]...
```

### Area 50: Sector 23
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2023&limit=20"
```
Status: 200
Latency: 15.3ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJN_BW_aHdDDkRZ9V9q_co6K8","name":"Hotel Howdy","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":2.5},"trust_score":86.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"Sector 23"
...[truncated]...
```

### Area 51: Pitampura
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Pitampura&limit=20"
```
Status: 200
Latency: 4.0ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJVVVVJdQDDTkRyYcuYnqjUqc","name":"Hotel City Park- Hotels In Delhi","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":1.7,"location":2.5,"value":2.5},"trust_score":78.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0,"price":nu
...[truncated]...
```

### Area 52: Satbari
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Satbari&limit=20"
```
Status: 200
Latency: 25.7ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ97W7F9EfDTkRidfrk_JoC5s","name":"The Ocean Pearl Retreat","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":2.5},"trust_score":90.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0,"price":null,"area"
...[truncated]...
```

### Area 53: Wazirabad
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Wazirabad&limit=20"
```
Status: 200
Latency: 4.1ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJgVaLtj38DDkR9GuM4URH1aM","name":"Oyo Hotel Royal City","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":75.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.8,"reviews_count":0,"price":null,"area":"W
...[truncated]...
```

### Area 54: Sector 29
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2029&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ____v_wYDTkRhZscYezopi4","name":"The Pllazio Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":2.5},"trust_score":91.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.3,"reviews_count":0,"price":null,"area":"Sect
...[truncated]...
```

### Area 55: Shalimar Bagh
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Shalimar%20Bagh&limit=20"
```
Status: 200
Latency: 20.4ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJmY1WY2gBDTkRsmGgG-zn_90","name":"Hotel O Shipraj Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":2.5,"value":2.5},"trust_score":76.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area":"Sh
...[truncated]...
```

### Area 56: Patel Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Patel%20Nagar&limit=20"
```
Status: 200
Latency: 15.7ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJq6qq6pMCDTkRqTr-63N3wDg","name":"Hotel Pals Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":5.0},"trust_score":81.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.0,"reviews_count":0,"price":null,"area":"Patel N
...[truncated]...
```

### Area 57: Kapas Hera
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Kapas%20Hera&limit=20"
```
Status: 200
Latency: 4.6ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJc3ZI9pobDTkRPtK8HE8mb4I","name":"Airport Hotel Park Blue Near Iicc Yashobhoomi","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":4.9,"value":2.5},"trust_score":85.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count"
...[truncated]...
```

### Area 58: Khanpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Khanpur&limit=20"
```
Status: 200
Latency: 25.9ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJo4rzGLDhDDkRhQ81ZlWwock","name":"Mauryan Express Hotel Devli Khanpur","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":93.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price"
...[truncated]...
```

### Area 59: Jahangirpuri
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Jahangirpuri&limit=20"
```
Status: 200
Latency: 5.1ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJr2pE1N8BDTkR_szajQiBDpA","name":"Hotel Paradise","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":0.0,"service":5.0,"location":5.0,"value":3.3},"trust_score":82.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"price":null,"area":"Jahangi
...[truncated]...
```

### Area 60: Bhalswa
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Bhalswa&limit=20"
```
Status: 200
Latency: 5.1ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJFfwScQABDTkRJvSz1Bp0JRM","name":"Hotel O By Oyo Golden Guest House Sant Nagar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":5.0},"trust_score":87.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":
...[truncated]...
```

### Area 61: Sector 28
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2028&limit=20"
```
Status: 200
Latency: 5.3ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJEfscDYrdDDkRWnjQ9k_6njQ","name":"Treebo Grand Town House","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":83.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.1,"reviews_count":0,"price":null,"area"
...[truncated]...
```

### Area 62: Vasant Kunj
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Vasant%20Kunj&limit=20"
```
Status: 200
Latency: 4.7ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJmZQOztIdDTkRP7F2TwIcXdg","name":"Jmd Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":89.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count":0,"price":null,"area":"Vasant K
...[truncated]...
```

### Area 63: Aerocity
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Aerocity&limit=20"
```
Status: 200
Latency: 26.5ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJCdCLTWgcDTkRgCe4U3CxnUo","name":"Pullman New Delhi Aerocity","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":100.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"price":null,"a
...[truncated]...
```

### Area 64: Vaishali
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Vaishali&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJgUNQnjTlDDkR1QhrUG9MRcE","name":"Hotel The Emporio Grand","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.8,"service":3.3,"location":5.0,"value":3.3},"trust_score":77.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area"
...[truncated]...
```

### Area 65: Chanakyapuri
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Chanakyapuri&limit=20"
```
Status: 200
Latency: 4.9ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJe4zp0KMdDTkRm90YLrHBVg8","name":"Taj Palace, New Delhi","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.9,"service":4.2,"location":5.0,"value":0.9},"trust_score":95.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"price":null,"area":"
...[truncated]...
```

### Area 66: Bahadurgarh
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Bahadurgarh&limit=20"
```
Status: 200
Latency: 20.4ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJc4BAbZoJDTkRKKZrpsVFBFw","name":"Hotel Beatific Epsilon","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":91.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":
...[truncated]...
```

### Area 67: Sector 51
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2051&limit=20"
```
Status: 200
Latency: 4.0ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJg6ULUdEjDTkRnQiTUDS_J9s","name":"Ahuja Residency Mayfield Garden","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":92.4,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":nul
...[truncated]...
```

### Area 68: Sector 83
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2083&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJyRKgd5E9DTkRQ-_q9wDDy3I","name":"Ar Suites, Klj Square, Gurugram","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":93.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"reviews_count":0,"price":nul
...[truncated]...
```

### Area 69: Mundka
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Mundka&limit=20"
```
Status: 200
Latency: 4.5ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ6VKu20AFDTkR0gckv0FCS3M","name":"Hotel O By Oyo Comfort","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":5.0,"value":2.5},"trust_score":83.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area":
...[truncated]...
```

### Area 70: Palam Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Palam%20Vihar&limit=20"
```
Status: 200
Latency: 4.5ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJa5dF22oZDTkRQ2KjgHaw2d8","name":"Stay Studio Hotel & Residences","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":4.7},"trust_score":88.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null
...[truncated]...
```

### Area 71: Alipur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Alipur&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJtfVFi38ADTkRXdDWAReIZ2o","name":"Blue Sapphire Motel & Resort By Devam","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":4.9,"value":5.0},"trust_score":89.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count":0,"pric
...[truncated]...
```

### Area 72: Saket
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Saket&limit=20"
```
Status: 200
Latency: 3.8ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJx-nhZO3hDDkRhvElsSXy5jE","name":"Hotel Saket 27","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":89.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.3,"reviews_count":0,"price":null,"area":"Saket",
...[truncated]...
```

### Area 73: Budhera
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Budhera&limit=20"
```
Status: 200
Latency: 3.4ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ_XGJiqsVDTkRsDGzPDq1p6Q","name":"Super Hotel O By Oyo Sgt University Road Formerly Budhera","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":5.0,"value":0.0},"trust_score":83.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.8,"re
...[truncated]...
```

### Area 74: Kundli
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Kundli&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJC_BtMAmsDTkR0zDkFj0klCs","name":"Tdi Club Retreat Kundli Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":0.0,"value":0.0},"trust_score":77.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.0,"reviews_count":0,"price":null,
...[truncated]...
```

### Area 75: GTB Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=GTB%20Nagar&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ77cDh5H9DDkRw4eomzQsdh4","name":"Hotel O The Signature Stay","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":0.0,"service":0.1,"location":0.0,"value":0.0},"trust_score":38.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.3,"reviews_count":0,"price":null,"ar
...[truncated]...
```

### Area 76: Kamla Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Kamla%20Nagar&limit=20"
```
Status: 200
Latency: 4.4ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJWeQkGvn9DDkR472-MKgiClU","name":"Hotel North Campus","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":75.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.5,"reviews_count":0,"price":null,"area":"Kam
...[truncated]...
```

### Area 77: Sector 69
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2069&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJn90fB-IjDTkRa2h_IqLdOBk","name":"Gilmore Stays | Homestay |","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":88.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"price":null,"ar
...[truncated]...
```

### Area 78: East of Kailash
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=East%20of%20Kailash&limit=20"
```
Status: 200
Latency: 4.3ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJbYigBcvjDDkRStKjE7MFi4o","name":"Jpm White House Bed & Breakfast","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.3,"service":3.3,"location":3.3,"value":0.0},"trust_score":73.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.0,"reviews_count":0,"price":nul
...[truncated]...
```

### Area 79: Lajpat Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Lajpat%20Nagar&limit=20"
```
Status: 200
Latency: 4.9ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJAzdTzS7jDDkRIt7HRR47yfc","name":"Park Inn By Radisson New Delhi Lajpat Nagar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":89.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0
...[truncated]...
```

### Area 80: Sector 26
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2026&limit=20"
```
Status: 200
Latency: 20.4ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJb9VeCNMYDTkRcs0Bfr8neXo","name":"Tribe Bespoke Hotel By Flxho","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":5.0,"value":2.5},"trust_score":87.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price":null,"
...[truncated]...
```

### Area 81: Gurgaon
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Gurgaon&limit=20"
```
Status: 200
Latency: 4.9ms
Returned: 7 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJr3w57d8ZDTkReaF1ZGBlgvM","name":"Masaga By Qcent","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":2.5},"trust_score":89.5,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Gurgao
...[truncated]...
```

### Area 82: Farukh Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Farukh%20Nagar&limit=20"
```
Status: 200
Latency: 3.8ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJu85bG-QVDTkRHw-yR_kKZU4","name":"Hotel O Aashiyana","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":2.5,"value":2.5},"trust_score":86.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.9,"reviews_count":0,"price":null,"area":"Faru
...[truncated]...
```

### Area 83: Ashok Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Ashok%20Vihar&limit=20"
```
Status: 200
Latency: 6.0ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJTxZARVUZDTkRpaG7WjvgWiI","name":"Safe&Sure Residency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":93.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"As
...[truncated]...
```

### Area 84: Sector 49
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2049&limit=20"
```
Status: 200
Latency: 4.7ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ9WJgCpwiDTkR9v_-VgD8zc4","name":"Radisson Hotel Gurugram Sohna Road City Center","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":5.0,"value":2.5},"trust_score":93.2,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.4,"reviews_count
...[truncated]...
```

### Area 85: Basant Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Basant%20Vihar&limit=20"
```
Status: 200
Latency: 7.6ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ5XYHAwAJDTkRhk-aK3gljDQ","name":"The Empire State","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":88.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"Basan
...[truncated]...
```

### Area 86: Rangpuri
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Rangpuri&limit=20"
```
Status: 200
Latency: 7.2ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJZVHCl2ocDTkR4FUy2t2OM2c","name":"Hotel Grand Regency","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":93.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Ra
...[truncated]...
```

### Area 87: Johripur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Johripur&limit=20"
```
Status: 200
Latency: 7.5ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJE3OAKsb7DDkR9ddf6PCweXI","name":"Collection O Johri Enclave Metro Station Second Home","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":2.5,"value":2.5},"trust_score":86.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews
...[truncated]...
```

### Area 88: Marmurpur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Marmurpur&limit=20"
```
Status: 200
Latency: 6.9ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJQ1QHIZqrDTkRcb5xBvj37zk","name":"Oyo Flagship Tushir House","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":0.1,"value":2.5},"trust_score":56.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.7,"reviews_count":0,"price":null,"are
...[truncated]...
```

### Area 89: Sector 19
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2019&limit=20"
```
Status: 200
Latency: 7.3ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJqbcp5TjlDDkR7K7kvixY4OI","name":"Treebo Aviraj Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":90.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Sect
...[truncated]...
```

### Area 90: Sector 93
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2093&limit=20"
```
Status: 200
Latency: 17.0ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJs5LeHAAXDTkRhHmVT0FLf6Q","name":"Hotel Bul Plaza","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":2.5,"location":2.5,"value":2.5},"trust_score":87.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":5.0,"reviews_count":0,"price":null,"area":"Sector
...[truncated]...
```

### Area 91: Laxmi Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Laxmi%20Nagar&limit=20"
```
Status: 200
Latency: 5.4ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJW2w4ran8DDkRoFkWIhzXKxk","name":"Hotel Om","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":2.5},"trust_score":66.7,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.3,"reviews_count":0,"price":null,"area":"Laxmi Nagar",
...[truncated]...
```

### Area 92: Samaypur
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Samaypur&limit=20"
```
Status: 200
Latency: 26.8ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJO-1YhaoBDTkRSjyr7WIIzG4","name":"Lotus Guest House","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":5.0,"location":2.5,"value":2.5},"trust_score":63.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.6,"reviews_count":0,"price":null,"area":"Sama
...[truncated]...
```

### Area 93: Sector 86
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2086&limit=20"
```
Status: 200
Latency: 6.0ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJUQ3mbVndDDkRlkR4HMW7AVA","name":"Hotel Mayur","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":5.0},"trust_score":83.9,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.3,"reviews_count":0,"price":null,"area":"Sector 86"
...[truncated]...
```

### Area 94: Sector 77
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2077&limit=20"
```
Status: 200
Latency: 8.3ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJG8FI6_UXDTkRHGRJJxf6O_w","name":"Aapnoghar (Resort, Water Park, Amusement Park)","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":92.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.3,"reviews_count
...[truncated]...
```

### Area 95: Hari Nagar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Hari%20Nagar&limit=20"
```
Status: 200
Latency: 7.1ms
Returned: 4 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ_8JzTlsDDTkRbbgJvd3R7J8","name":"Golden Tulip Essential","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.7,"service":4.3,"location":3.7,"value":0.0},"trust_score":75.6,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.8,"reviews_count":0,"price":null,"area":
...[truncated]...
```

### Area 96: Malka Ganj
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Malka%20Ganj&limit=20"
```
Status: 200
Latency: 22.8ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJGY6rtYz9DDkROGiBI6lGJI4","name":"The Twenties Hotel Kamla Nagar","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":1.7,"location":2.5,"value":0.0},"trust_score":45.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":3.3,"reviews_count":0,"price":null
...[truncated]...
```

### Area 97: Sector 15
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2015&limit=20"
```
Status: 200
Latency: 14.6ms
Returned: 6 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJg7gqCGsZDTkRdaEehmo_1F8","name":"Lime Tree Hotel Nearby 32Nd Avenue | Sector 15 Gurgaon | Hotel Near Udyog Vihar Gurgaon","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":2.5,"service":1.7,"location":5.0,"value":2.5},"trust_score":82.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_
...[truncated]...
```

### Area 98: Sector 47
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2047&limit=20"
```
Status: 200
Latency: 15.0ms
Returned: 3 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJefT_XP8ZDTkRD_-feFIklCk","name":"Nearmi Boutique Hotel & Cafe Sector 47","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":5.0,"value":5.0},"trust_score":89.1,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.7,"reviews_count":0,"pri
...[truncated]...
```

### Area 99: Sector 10
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Sector%2010&limit=20"
```
Status: 200
Latency: 5.9ms
Returned: 5 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJ9yKcCbQXDTkRW3uWCbf-uLQ","name":"Starkey Inn","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":85.8,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0,"price":null,"area":"Sector 10"
...[truncated]...
```

### Area 100: Preet Vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Preet%20Vihar&limit=20"
```
Status: 200
Latency: 5.1ms
Returned: 2 hotels
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJDQCwFlb7DDkRc6G99BgmakY","name":"East Inn Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":5.0,"value":0.0},"trust_score":77.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0,"price":null,"area":"Preet V
...[truncated]...
```

## Edge Case Audit
### Edge Case: pahar ganj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "pahar ganj"}'
```
Status: 200
Latency: 33.4ms
Response excerpt:
```json
{"trace_id":"req-b23826fe","query":"pahar ganj","recommendations":[{"hotel_id":"ChIJ0yLaR0H9DDkR4ItbT8FxMO8","name":"Hotel Shelton","summary_text":"This hotel matches your Paharganj search based on its location, overall rating, and verified review signals.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":5.0,"value":0.0},"trust_score":78.4,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"This hotel matches your Paharganj search based on its location, overall rat
...[truncated]...
```

### Edge Case: mahipal pur
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "mahipal pur"}'
```
Status: 200
Latency: 34.8ms
Response excerpt:
```json
{"trace_id":"req-20256463","query":"mahipal pur","recommendations":[{"hotel_id":"ChIJBb3mYrQdDTkRv0Dx43jGpGQ","name":"Hotel Urban Tree","summary_text":"This hotel matches your Mahipalpur search based on its location, overall rating, and verified review signals.","aspect_scores":{"cleanliness":0.0,"service":0.0,"location":0.0,"value":0.0},"trust_score":67.0,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"This hotel matches your Mahipalpur search based on its location, overa
...[truncated]...
```

### Edge Case: gurgaon
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "gurgaon"}'
```
Status: 200
Latency: 31.6ms
Response excerpt:
```json
{"trace_id":"req-d14df33f","query":"gurgaon","recommendations":[{"hotel_id":"ChIJ2Q_vUgAhDTkRG9JSfed_m9U","name":"Grand Mantram Resort","summary_text":"This hotel matches your Gurugram search based on its location, overall rating, and verified review signals.","aspect_scores":{"cleanliness":5.0,"service":5.0,"location":2.5,"value":2.5},"trust_score":83.9,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"This hotel matches your Gurugram search based on its location, overall r
...[truncated]...
```

### Edge Case: preet vihar
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Preet%20Vihar"
```
Status: 200
Latency: 4.4ms
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJDQCwFlb7DDkRc6G99BgmakY","name":"East Inn Hotel","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":3.3,"service":5.0,"location":5.0,"value":0.0},"trust_score":77.0,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.2,"reviews_count":0,"price":null,"area":"Preet V
...[truncated]...
```

### Edge Case: hotel near paharganj
Command:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/hotels?area=Paharganj"
```
Status: 200
Latency: 5.3ms
Response excerpt:
```json
{"hotels":[{"hotel_id":"ChIJfZabjD_9DDkR0siMJiwLzR8","name":"Hotel Ajanta - Free Airport Pick Up Service","summary_text":"Showing properties from our Expedia catalog.","aspect_scores":{"cleanliness":5.0,"service":4.8,"location":5.0,"value":5.0},"trust_score":94.3,"explanation_badge":"Catalog","ai_match_label":"Excellent","match_reason":"Matching your current catalog filters.","query_alignment_score":1.0,"review_evidence":[],"provenance":[],"confidence_badge":"High","rating":4.6,"reviews_count":0
...[truncated]...
```

### Edge Case: family hotels near paharganj
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "family hotels near paharganj"}'
```
Status: 200
Latency: 48.2ms
Response excerpt:
```json
{"trace_id":"req-fd8a14ec","query":"family hotels near paharganj","recommendations":[{"hotel_id":"ChIJ7zycekH9DDkRWd8FYsIVT3U","name":"Hotel Mother Palace","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":4.8,"service":2.5,"location":3.5,"value":3.2},"trust_score":72.4,"explanation_badge":"Verified","ai_match_label":"Good","match_reason":"Limited review evidence is available to confidently assess this criterion.","query_al
...[truncated]...
```

### Edge Case: cheap family hotel near paharganj with breakfast
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "cheap family hotel near paharganj with breakfast"}'
```
Status: 200
Latency: 81.1ms
Response excerpt:
```json
{"trace_id":"req-9e6b8212","query":"cheap family hotel near paharganj with breakfast","recommendations":[{"hotel_id":"ChIJAZTkm0D9DDkRMDezVFMRIKM","name":"The Gold Inn","summary_text":"Limited review evidence is available to confidently assess this criterion.","aspect_scores":{"cleanliness":5.0,"service":2.5,"location":5.0,"value":5.0},"trust_score":74.3,"explanation_badge":"Verified","ai_match_label":"Excellent","match_reason":"Limited review evidence is available to confidently assess this cri
...[truncated]...
```

### Edge Case: emoji query
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "\ud83c\udfe8 hotel near airport"}'
```
Status: 500
Latency: 49.2ms
Response excerpt:
```json
Internal Server Error
```

### Edge Case: 1
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "1"}'
```
Status: 200
Latency: 63.3ms
Response excerpt:
```json
{"trace_id":"req-d46c8d1e","query":"1","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":0.0,"retrieval_ms":0,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels matching that text. Please try typing a longer search phrase."}}
```

### Edge Case: a
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "a"}'
```
Status: 200
Latency: 3.8ms
Response excerpt:
```json
{"trace_id":"req-3edf0b58","query":"a","recommendations":[],"catalog_suggestions":[],"metadata":{"latency_ms":0.0,"retrieval_ms":0,"compression_ms":0,"llm_ms":0,"fallback_level":0,"cache_hit":false,"is_fallback":false,"target_area":"","is_terminal_no_match":true,"fallback_reason":"We couldn't find hotels matching that text. Please try typing a longer search phrase."}}
```

### Edge Case: 300+ character query
Command:
```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/recommend -ContentType "application/json" -Body '{"query": "hotel very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very near airport"}'
```
Status: 200
Latency: 39.7ms
Response excerpt:
```json
{"trace_id":"req-04465275","query":"hotel very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very ver
...[truncated]...
```

## Final Computed Statistics
AI Queries Passed: 100/100
Catalog Queries Passed: 100/100
Average AI Latency: 56.17ms
Average Catalog Latency: 8.94ms
Failed Requests: 0