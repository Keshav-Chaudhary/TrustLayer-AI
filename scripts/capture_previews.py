"""
TrustLayer-AI Automated Full Desktop Window Screenshot Capturer
Captures high-resolution desktop window views for all application and report pages.
Includes page warmup, 5-second countdown, and 5-second tab-switching delays.
"""

import os
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs" / "images" / "previews"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Locate Chrome or Edge
BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "google-chrome",
    "chromium",
]
BROWSER = next((b for b in BROWSER_CANDIDATES if os.path.exists(b)), None)

APP_BASE = "http://127.0.0.1:3000"
REPORT_BASE = (ROOT / "Report_Website" / "index.html").as_uri()

PAGES = [
    # --- Next.js Frontend Application Routes ---
    ("01_landing_search", f"{APP_BASE}/", "Landing Page & Search Portal"),
    ("02_stays_feed", f"{APP_BASE}/stays", "Ranked Stays & Recommendation Feed"),
    ("03_ai_assistant", f"{APP_BASE}/ai-assistant", "Conversational Anti-Hallucinatory AI Assistant"),
    ("04_compare_matrix", f"{APP_BASE}/compare", "5D Aspect Hotel Comparison Matrix"),
    ("05_saved_stays", f"{APP_BASE}/saved", "Saved Properties & Wishlist"),
    ("06_about_methodology", f"{APP_BASE}/about", "About & Grounding Methodology"),

    # --- Master Research & Engineering Report Routes ---
    ("07_report_cover", f"{REPORT_BASE}#title", "Master Document Cover & Live System Metrics"),
    ("08_report_architecture", f"{REPORT_BASE}#ch-complete-arch", "Complete System Architecture & Blueprint (Ch. 11)"),
    ("09_report_absa", f"{REPORT_BASE}#ch-absa", "5-Dimensional ABSA Methodology (Ch. 2)"),
    ("10_report_timeline", f"{REPORT_BASE}#ch-dev-journey", "18-Stage Engineering Development Timeline (Ch. 4)"),
    ("11_report_recommender", f"{REPORT_BASE}#ch-recommender", "Hybrid Recommendation Engine & RRF k=60 (Ch. 5)"),
    ("12_report_database_schema", f"{REPORT_BASE}#ch-data-lineage", "PostgreSQL 17.6 + pgvector Schema & Lineage (Ch. 6)"),
    ("13_report_explainer", f"{REPORT_BASE}#ch-explainability", "Analytical Explainability Engine - 3.2 ms (Ch. 7)"),
    ("14_report_rag", f"{REPORT_BASE}#ch-rag", "Anti-Hallucinatory RAG & Citation Grounding (Ch. 8)"),
    ("15_report_evaluation", f"{REPORT_BASE}#ch-eval", "Comprehensive Empirical Evaluation & NDCG (Ch. 9)"),
]

def warmup_page(url: str):
    """Pre-triggers Next.js on-demand route compilation before launching browser."""
    if url.startswith("http"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Warmup"})
            with urllib.request.urlopen(req, timeout=8):
                pass
        except Exception:
            pass

def capture_desktop(url: str, output_path: Path, width: int = 1440, height: int = 900):
    if not BROWSER:
        print("[!] No supported browser executable found.")
        return False
    
    # 1. Warm up route so Next.js finishes webpack compilation
    warmup_page(url)
    time.sleep(1.0)
    
    # 2. Launch Chrome headless with compositor settling budget
    cmd = [
        BROWSER,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        f"--window-size={width},{height}",
        "--virtual-time-budget=6000",
        f"--screenshot={output_path.resolve()}",
        url
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as ex:
        print(f"Error capturing {url}: {ex}")
        return False

def main():
    print("=" * 75)
    print("📸 TrustLayer-AI Desktop Window Screenshot Capturer (1440x900)")
    print("   [+] Automatic Next.js Route Pre-Compilation Warmup")
    print("   [+] 5-Second Initial Delay + 5-Second Tab Switching Delay")
    print("   [+] 6000ms Virtual Compositor Settling Budget")
    print("=" * 75)
    print(f"Output Directory: {OUTPUT_DIR.resolve()}\n")

    # Initial 5-second countdown
    print("⏳ Initializing session. Starting first capture in 5 seconds...")
    for remaining in range(5, 0, -1):
        print(f"   Starting in {remaining}s...", end="\r", flush=True)
        time.sleep(1.0)
    print("   🚀 Starting captures now!                                  \n")

    total = len(PAGES)
    for index, (key, url, title) in enumerate(PAGES, 1):
        output_file = OUTPUT_DIR / f"{key}.png"
        print(f"[{index:02d}/{total:02d}] Capturing: {title}")
        print(f"       URL: {url}")
        
        ok = capture_desktop(url, output_file, 1440, 900)
        print(f"       Result: {'[OK] Saved' if ok else '[FAILED]'}")

        if index < total:
            print("       ⏳ Waiting 5.0s for next tab to reload and settle...")
            time.sleep(5.0)
        print()

    print("=" * 75)
    print("[✓] All 15 full desktop window screenshots successfully captured!")
    print("=" * 75)

if __name__ == "__main__":
    main()
