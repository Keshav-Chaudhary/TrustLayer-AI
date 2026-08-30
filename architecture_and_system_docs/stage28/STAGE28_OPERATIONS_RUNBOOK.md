# STAGE 28 — OPERATIONS RUNBOOK

## Step-by-Step Operator Instructions

### Step 1: Run Full End-to-End Pipeline Dry-Run
```bash
python -m scripts.orchestrator full
```

### Step 2: Inspect Run Manifest & Diff Artifact
Check the generated manifest:
```text
data/runs/<RUN_ID>/pipeline_manifest.json
data/diffs/<RUN_ID>/dry_run.json
```

### Step 3: Explicitly Apply Approved Ingestion Run
```bash
python -m scripts.orchestrator apply --run-id <RUN_ID>
```

### Step 4: Run Comprehensive Verification
```bash
python -m scripts.orchestrator verify
```
