# INGESTION FAILURE RECOVERY

- **Dry-Run Safety**: Dry-run operations perform zero database mutations. If a dry-run fails due to validation errors, fix source data and re-run.
- **Apply Rollback**: Transactional apply executes inside a single SQLAlchemy session (`session.commit()`). Any database error triggers an immediate `session.rollback()`.
- **Stale RUN_ID**: If PostgreSQL state changes between dry-run and apply, re-run dry-run to obtain a fresh `RUN_ID`.
