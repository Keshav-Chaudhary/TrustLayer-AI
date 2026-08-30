# STAGE 24 — OPERATIONAL RUNBOOK

## Operational CLI Commands

### 1. Ingestion Bootstrap Pipeline

```bash
# Validate CSV source records without database writes
python -m scripts.ingestion.bootstrap_postgres --mode validate-only

# Perform dry-run change detection calculation
python -m scripts.ingestion.bootstrap_postgres --mode dry-run

# Execute transactional apply to PostgreSQL target database
python -m scripts.ingestion.bootstrap_postgres --mode apply --db-url "postgresql://<user>:<password>@localhost:5432/trustlayer_db"
```

### 2. Domain Event Outbox Worker

```bash
# Process pending outbox events (single batch run)
python -m scripts.workers.outbox_worker --once --db-url "postgresql://<user>:<password>@localhost:5432/trustlayer_db"

# Start continuous polling worker loop (2.0s interval)
python -m scripts.workers.outbox_worker --db-url "postgresql://<user>:<password>@localhost:5432/trustlayer_db"
```

### 3. Dual-Backend Parity Verification

```bash
# Run dual-backend entity, field, and RAG recommendation parity suite
python -m scripts.verification.parity_verification
```

### 4. Automated Pytest Test Suite

```bash
# Execute complete Stage 23 & Stage 24 test suite (24 tests)
python -m pytest
```

---

## Controlled Backend Switching Strategy

To switch backend execution mode in development/staging:

Set environment variables in `.env`:
```env
DATA_BACKEND=postgres
VECTOR_BACKEND=pgvector
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/trustlayer_db
```

To rollback to read-only CSV bootstrap path:
```env
DATA_BACKEND=csv
VECTOR_BACKEND=chroma
```
