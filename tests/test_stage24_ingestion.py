import os
import pytest
from scripts.ingestion.bootstrap_postgres import run_bootstrap

@pytest.fixture
def temp_db_url(tmp_path):
    return f"sqlite:///{tmp_path}/test_bootstrap.db"

def test_bootstrap_dry_run(temp_db_url):
    res = run_bootstrap(mode="dry-run", db_url=temp_db_url)
    assert res["status"] == "SUCCESS"
    assert res["records_seen"] == 1661
    assert res["records_inserted"] == 1661
    assert res["records_rejected"] == 0

def test_bootstrap_validate_only():
    res = run_bootstrap(mode="validate-only")
    assert res["status"] == "VALIDATED"
    assert res["records_seen"] == 1661
    assert res["records_rejected"] == 0

def test_bootstrap_apply_and_idempotency(temp_db_url):
    # Run 1: Initial apply
    res1 = run_bootstrap(mode="apply", db_url=temp_db_url)
    assert res1["records_inserted"] == 1661
    assert res1["records_updated"] == 0
    assert res1["records_unchanged"] == 0

    # Run 2: Re-apply identical data
    res2 = run_bootstrap(mode="apply", db_url=temp_db_url)
    assert res2["records_inserted"] == 0
    assert res2["records_updated"] == 0
    assert res2["records_unchanged"] == 1661
