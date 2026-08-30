"""TrustLayer-AI development runner."""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"


def get_npm_command() -> str | None:
    return shutil.which("npm") or (shutil.which("npm.cmd") if os.name == "nt" else None)


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None or (os.name == "nt" and shutil.which(f"{command}.cmd") is not None)


def run_command(command: list[str], cwd: Path = ROOT) -> int:
    is_windows = os.name == "nt"
    use_shell = is_windows and command[0] in ("npm", "npx")
    return subprocess.run(command, cwd=cwd, shell=use_shell).returncode


def start_services() -> int:
    python = sys.executable
    api = subprocess.Popen(
        [python, "-m", "uvicorn", "app.api.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=ROOT,
    )

    frontend = None
    npm_cmd = get_npm_command()
    try:
        if not npm_cmd:
            print("\n[!] npm was not found in PATH. Starting FastAPI backend only.")
            print("[*] API Docs: http://127.0.0.1:8000/docs")
            return api.wait()

        # Auto-install frontend dependencies if missing
        if not (FRONTEND / "node_modules").exists():
            print("[*] Installing frontend dependencies (node_modules)...")
            subprocess.run([npm_cmd, "install"], cwd=FRONTEND, shell=os.name == "nt", check=False)

        frontend = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=FRONTEND,
            shell=os.name == "nt",
        )
        print("\n" + "=" * 60)
        print("🚀 TrustLayer-AI Services Successfully Started!")
        print("=" * 60)
        print("📖 Backend API (Swagger): http://127.0.0.1:8000/docs")
        print("🌐 Frontend Next.js UI:   http://localhost:3000")
        print("=" * 60)
        print("Press Ctrl+C to gracefully stop both services.\n")

        while True:
            api_code = api.poll()
            frontend_code = frontend.poll()
            if api_code is not None:
                print(f"API exited with code {api_code}.")
                return api_code
            if frontend_code is not None:
                print(f"Frontend exited with code {frontend_code}.")
                return frontend_code
            signal.pause() if hasattr(signal, "pause") else subprocess.run(
                [python, "-c", "import time; time.sleep(0.5)"], check=False
            )
    except KeyboardInterrupt:
        print("\nStopping TrustLayer-AI services...")
        return 0
    finally:
        for process in (frontend, api):
            if process is not None and process.poll() is None:
                process.terminate()
        for process in (frontend, api):
            if process is not None:
                process.wait()


def doctor() -> int:
    checks = {
        "Python": sys.executable,
        "vector store": ROOT / "data" / "vector_store",
        "frontend dependencies": FRONTEND / "node_modules",
        "npm": shutil.which("npm") or "missing",
    }
    failed = False
    for name, value in checks.items():
        available = Path(value).exists() if isinstance(value, Path) else bool(value)
        print(f"{'OK' if available else 'MISSING':7} {name}: {value}")
        failed = failed or not available

    for module in ("fastapi", "uvicorn", "chromadb"):
        available = importlib.util.find_spec(module) is not None
        print(f"{'OK' if available else 'MISSING':7} Python module: {module}")
        failed = failed or not available
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TrustLayer-AI development services and workflows.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--backend", action="store_true", help="Run the FastAPI backend only")
    modes.add_argument("--frontend", action="store_true", help="Run the Next.js frontend only")
    modes.add_argument("--doctor", action="store_true", help="Check local runtime prerequisites")
    modes.add_argument("--test", action="store_true", help="Run the pytest test suite")
    modes.add_argument("--build-vectors", action="store_true", help="Rebuild the ChromaDB vector store")
    modes.add_argument("--pipeline", action="store_true", help="Run the master data pipeline")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = sys.executable

    if args.doctor:
        return doctor()
    if args.test:
        return run_command([python, "-m", "pytest"])
    if args.build_vectors:
        return run_command([python, "-m", "scripts.rag.build_vector_store"])
    if args.pipeline:
        return run_command([python, "-m", "scripts.orchestrator", "full"])
    if args.backend:
        return run_command([python, "-m", "uvicorn", "app.api.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])
    if args.frontend:
        npm_cmd = get_npm_command()
        if not npm_cmd:
            print("[!] npm was not found in PATH.")
            return 1
        return run_command([npm_cmd, "run", "dev"], cwd=FRONTEND)
    return start_services()


if __name__ == "__main__":
    raise SystemExit(main())
