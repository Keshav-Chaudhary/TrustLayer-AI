# PROJECT DELETION IMPACT MATRIX

| Category | File Count | Deletion Impact Summary | Deletion Risk |
|---|---|---|---|
| **Production Source (`app/`)** | 25 | Deleting will break FastAPI application startup, dependency injection, and core business services. | 🔴 HIGH RISK |
| **Configuration (`.env`, `config.py`)** | 4 | Deleting breaks PostgreSQL database connections, backend routing flags, and API settings. | 🔴 HIGH RISK |
| **Test Suite (`tests/`)** | 12 | Application runs, but automated regression testing, CI/CD pipeline, and audit verification break. | 🟠 MEDIUM RISK |
| **Ingestion Scripts (`scripts/ingestion/`)** | 5 | Application runs, but ability to seed PostgreSQL or sync vectors from baseline datasets breaks. | 🟠 MEDIUM RISK |
| **Verification Scripts (`scripts/verification/`)** | 4 | Application runs, but automated database provenance auditing and forensic reporting break. | 🟡 LOW RISK |
| **Reference Datasets (`data/exports/`)** | 3 | Application runs on PostgreSQL, but reference source datasets required for bootstrapping are lost. | ⚪ KEEP — DATA |
| **Documentation (`architecture_and_system_docs/`)**| 18 | Genuinely no runtime code impact. Retained strictly as system documentation and audit history. | 🟢 SAFE / NO RUNTIME IMPACT |
