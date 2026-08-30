# DATA INGESTION RUNBOOK

## Step-by-Step Operator Guide for New Data Ingestion

### Step 1: Place Raw Files
Place incoming raw CSV dataset files into `data/sources/raw/`:
```bash
cp new_hotels_2026.csv data/sources/raw/
```

### Step 2: Execute Pipeline Dry-Run
Run the dry-run command to validate, deduplicate, and compute diffs against PostgreSQL:
```bash
python -m scripts.ingestion.pipeline dry-run
```
Output:
```text
=== PIPELINE DRY RUN SUCCESSFUL ===
Run ID      : a1b2c3d4
New Hotels  : 15
Updated     : 42
Unchanged   : 1,604
Artifact    : data/diffs/a1b2c3d4/dry_run.json
```

### Step 3: Review Diff Artifact
Inspect `data/diffs/a1b2c3d4/dry_run.json` to verify changes.

### Step 4: Apply Approved Ingestion Run
Execute the apply command specifying the approved `RUN_ID`:
```bash
python -m scripts.ingestion.pipeline apply --run-id a1b2c3d4
```

### Step 5: Verify Ingestion & Provenance
Run the verification check:
```bash
python -m scripts.ingestion.pipeline verify
```
