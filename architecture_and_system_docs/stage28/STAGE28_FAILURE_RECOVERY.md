# STAGE 28 — FAILURE RECOVERY & STALE RUN PROTECTION

- **Dry-Run Safety**: Dry-run operations perform zero database mutations. If an upstream stage fails, the pipeline halts immediately with status `FAILED` and PostgreSQL remains 100% untouched.
- **Stale RUN_ID Protection**: `scripts/orchestrator.py apply` checks SHA-256 manifest hashes, un-applied status, and record count invariants before executing transactional apply.
