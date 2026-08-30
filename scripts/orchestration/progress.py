import os
import sys
import time
import math
from datetime import datetime
from typing import Dict, Any, Optional, List

class ProgressTracker:
    def __init__(self, run_id: str, total_stages: int = 6, log_file: Optional[str] = None):
        self.run_id = run_id
        self.total_stages = total_stages
        self.start_time = time.time()
        self.log_file = log_file
        self.stages = [
            {"num": 1, "name": "Source Acquisition", "script": "fetch_google_places.py", "status": "PENDING", "duration": 0, "records": 0, "output": "data/raw/"},
            {"num": 2, "name": "Data Cleaning", "script": "clean_hotel_metadata.py", "status": "PENDING", "duration": 0, "records": 0, "output": "data/processed/cleaned/"},
            {"num": 3, "name": "NLP & ABSA Extraction", "script": "analyze_sentiment.py", "status": "PENDING", "duration": 0, "records": 0, "output": "data/processed/features/"},
            {"num": 4, "name": "Hotel Feature Engineering", "script": "engineer_features.py", "status": "PENDING", "duration": 0, "records": 0, "output": "hotel_features.csv"},
            {"num": 5, "name": "Canonical Dataset Merge", "script": "merge_dataset.py", "status": "PENDING", "duration": 0, "records": 0, "output": "final_hotel_dataset.csv"},
            {"num": 6, "name": "Stage 26 Postgres Diff", "script": "diff_engine.py", "status": "PENDING", "duration": 0, "records": 0, "output": "dry_run.json"}
        ]
        self.current_stage_idx = 0
        self.current_script = ""
        self.current_processed = 0
        self.current_total = 0

        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            self._log_raw(f"=== PIPELINE LOG STARTED (RUN_ID: {self.run_id}) AT {datetime.utcnow().isoformat()} ===")

    def _log_raw(self, msg: str):
        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {msg}\n")

    def start_stage(self, stage_idx: int, script_name: str):
        self.current_stage_idx = stage_idx
        st = self.stages[stage_idx]
        st["status"] = "RUNNING"
        st["script"] = script_name
        st["start_time"] = time.time()
        self.current_script = script_name
        self.current_processed = 0
        self.current_total = 0
        self._log_raw(f"STAGE STARTED: [{st['num']}/{self.total_stages}] {st['name']} ({script_name})")
        self.render()

    def update_record_progress(self, processed: int, total: int):
        self.current_processed = processed
        self.current_total = total
        self.render()

    def complete_stage(self, stage_idx: int, records: int = 0, output_path: str = ""):
        st = self.stages[stage_idx]
        st["status"] = "COMPLETED"
        st["duration"] = time.time() - st.get("start_time", time.time())
        st["records"] = records
        if output_path:
            st["output"] = output_path
        self._log_raw(f"STAGE COMPLETED: [{st['num']}/{self.total_stages}] {st['name']} | Records: {records} | Duration: {st['duration']:.2f}s")
        self.render()

    def fail_stage(self, stage_idx: int, error_msg: str):
        st = self.stages[stage_idx]
        st["status"] = "FAILED"
        st["duration"] = time.time() - st.get("start_time", time.time())
        self._log_raw(f"STAGE FAILED: [{st['num']}/{self.total_stages}] {st['name']} | Error: {error_msg}")
        self.render()

    def render(self):
        elapsed = time.time() - self.start_time
        completed_count = sum(1 for s in self.stages if s["status"] == "COMPLETED")
        overall_pct = int((completed_count / self.total_stages) * 100)
        
        # Calculate ETA
        if completed_count > 0 and overall_pct < 100:
            avg_time_per_stage = elapsed / completed_count
            remaining_stages = self.total_stages - completed_count
            est_left_sec = avg_time_per_stage * remaining_stages
            eta_str = f"{int(est_left_sec // 60):02d}:{int(est_left_sec % 60):02d}"
        else:
            eta_str = "calculating..."

        elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"

        # Progress bar string
        bar_len = 20
        filled_len = int(bar_len * completed_count // self.total_stages)
        bar_str = "█" * filled_len + "░" * (bar_len - filled_len)

        print("\033[H\033[J", end="") # Clear terminal screen
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║              TRUSTLAYER-AI DATA PIPELINE                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║ RUN ID       : {self.run_id:<45} ║")
        print(f"║ MODE         : FULL DRY-RUN (Zero Postgres Mutation)        ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\nOverall Progress: [{bar_str}] {overall_pct}%")
        print(f"Elapsed       : {elapsed_str} | Estimated Left: {eta_str}\n")
        print("---------------------------------------------------------------")

        for s in self.stages:
            num = s["num"]
            name = s["name"]
            st_status = s["status"]
            dur = s["duration"]
            if st_status == "COMPLETED":
                icon = "✓ COMPLETED"
                dur_str = f"{dur:.1f}s"
            elif st_status == "RUNNING":
                icon = "→ RUNNING  "
                dur_str = f"{time.time() - s.get('start_time', time.time()):.1f}s"
            elif st_status == "FAILED":
                icon = "✗ FAILED   "
                dur_str = f"{dur:.1f}s"
            else:
                icon = "○ PENDING  "
                dur_str = "--"

            print(f"[{num}/{self.total_stages}] {name:<28} {icon:<12} {dur_str:>6}")

        print("---------------------------------------------------------------")
        if self.current_total > 0:
            rec_pct = (self.current_processed / self.current_total) * 100
            print(f"Active Task Progress : [{self.current_processed}/{self.current_total}] ({rec_pct:.1f}%)")
        print("PostgreSQL Safety    : DRY-RUN — ZERO MUTATION")
        print("Press Ctrl+C to safely interrupt.\n")
        sys.stdout.flush()
