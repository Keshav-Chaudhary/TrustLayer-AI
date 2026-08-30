# 🏗️ System Architecture & Data Flow

This document details the internal architecture, semantic decomposition, and end-to-end query execution lifecycle of **TrustLayer-AI**.

---

## 🧭 Architectural Overview

TrustLayer-AI bridges statistical aspect analysis with generative LLMs using strict provenance constraints:

```
                               ┌────────────────────────┐
                               │   User Natural Query   │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Intent & Constraint    │
                               │ Parser (Regex + NLP)   │
                               └───────────┬────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
       ┌────────────────────────┐                    ┌────────────────────────┐
       │   Strict Filter Match  │                    │ Fallback Cascading     │
       │ (Area, Price, Persona) │                    │ Constraint Relaxer     │
       └────────────┬───────────┘                    └────────────┬───────────┘
                    │                                             │
                    └──────────────────────┬──────────────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ ChromaDB Vector Search │
                               │ 5-Chunk Semantic Match │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Context Compressor &   │
                               │ Prompt Synthesizer     │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Local Ollama LLM       │
                               │ (Qwen2.5-7B-Instruct)  │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Grounding Validator &  │
                               │ Citation Verifier      │
                               └───────────┬────────────┘
                                           │
                                           ▼
                               ┌────────────────────────┐
                               │ Structured JSON Output │
                               │ with Evidence Badges   │
                               └────────────────────────┘
```

---

## 🧩 5-Chunk Semantic Decomposition

To avoid loss of detail during embedding and retrieval, each hotel entity is broken down into **5 distinct semantic chunks** encoded with `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional embeddings):

| Chunk Identifier | Category | Purpose | Included Metadata |
| :--- | :--- | :--- | :--- |
| **Chunk A** | Profile & Basic Specs | Hotel identity, locality, price per night, and official rating tier. | `hotel_id`, `name`, `locality`, `city`, `price_level` |
| **Chunk B** | Quantitative Aspect Scores | 5-dimensional ABSA metric ratings (*Cleanliness, Service, Location, Value, Staff*). | `cleanliness_score`, `service_score`, `location_score`, `value_score`, `staff_score` |
| **Chunk C** | Positive Provenance Evidence | Verbatim verified quotes and positive highlight themes extracted from real guest reviews. | `positive_tags`, `review_snippets_positive` |
| **Chunk D** | Negative / Cautionary Evidence | Critical feedback points, known pain points, and cautionary review excerpts. | `negative_tags`, `review_snippets_negative` |
| **Chunk E** | Global Recommendation Signals | Composite Trust Score (0-100), composite sentiment index, popularity ranking. | `trust_score`, `sentiment_rating`, `review_count` |

---

## 🛡️ Anti-Hallucination Grounding Validator

The Grounding Validator acts as an interception layer between LLM generation and client responses:
1. **Provenance Checking**: Verifies every claimed amenity, distance, and feature against the retrieved hotel chunks.
2. **Citation Injection**: Cites exact review fragments to back subjective statements (e.g., *"Quiet rooms with soundproof glazing"*).
3. **Threshold Gate**: Enforces a minimum trust score threshold (default: `70.0`). Below this, a transparent caution tag is attached.

---

## 🔄 Smart Constraint Relaxation Strategy

When strict queries return zero matches (e.g., *Luxury 5-star near Connaught Place under 1,500 INR*), the engine executes an intelligent 3-stage fallback:
1. **Persona Relaxation**: Relaxes travel persona constraints while keeping geographic & price boundaries intact.
2. **Budget Range Expansion**: Widens budget ceiling by +15% to 25% while maintaining strict locality.
3. **Adjacent Area Proximity**: Broadens area search to adjacent localities with clear transit notes.
