# STAGE 27 — ONE-COMMAND PIPELINE ORCHESTRATION DESIGN

## Proposed Master Orchestrator Architecture (`scripts/orchestrator.py`)

The proposed master orchestrator will provide a single unified CLI interface:

```bash
# Execute Stage-by-Stage Or Full Upstream -> Downstream Pipeline
python -m scripts.orchestrator full

# Execute Stage-Level Subcommands
python -m scripts.orchestrator fetch
python -m scripts.orchestrator clean
python -m scripts.orchestrator nlp
python -m scripts.orchestrator features
python -m scripts.orchestrator merge
python -m scripts.orchestrator dry-run
python -m scripts.orchestrator apply --run-id <RUN_ID>
python -m scripts.orchestrator verify
```

## Production Safety & Approval Boundary
- `python -m scripts.orchestrator full` will run Stages 1 through 6, generate `final_hotel_dataset.csv`, run Stage 26 validation & diff against PostgreSQL, print the dry-run diff summary, save `dry_run.json` with a unique `RUN_ID`, and **STOP BEFORE MODIFYING POSTGRESQL**.
- The database update requires explicit approval:
  ```bash
  python -m scripts.orchestrator apply --run-id <RUN_ID>
  ```
