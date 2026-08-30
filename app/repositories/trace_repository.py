import os
import json
import tempfile
import logging
from typing import List, Dict, Any, Optional
from app.repositories.base import BaseTraceRepository
from app.config.config import settings

logger = logging.getLogger("trustlayer")

def atomic_write_json(file_path: str, data: Any):
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        try:
            os.replace(temp_path, file_path)
        except PermissionError:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise e


class JsonTraceRepository(BaseTraceRepository):
    """
    JSON trace storage adapter encapsulating reading and atomic writes of batch debug runs.
    """
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or settings.BATCH_DEBUG_FILE_PATH

    def get_history(self, run_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        resolved_path = os.path.abspath(self.file_path)
        if not os.path.exists(resolved_path):
            return []

        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                runs = data.get("runs", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        except Exception as e:
            logger.error(f"Error reading trace history from {resolved_path}: {e}")
            return []

        if run_id:
            runs = [r for r in runs if r.get("run_id") == run_id]

        if limit is not None and limit > 0:
            runs = runs[-limit:]

        runs_reversed = list(reversed(runs))
        return runs_reversed

    def save_run(self, run_result: Dict[str, Any]) -> bool:
        resolved_path = os.path.abspath(self.file_path)
        history = []

        if os.path.exists(resolved_path):
            try:
                with open(resolved_path, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    if isinstance(history_data, list):
                        history = history_data
                    elif isinstance(history_data, dict) and "runs" in history_data:
                        history = history_data["runs"]
            except Exception as e:
                logger.warning(f"Failed reading existing history, initializing fresh list: {e}")
                history = []

        history.append(run_result)
        if len(history) > 20:
            history = history[-20:]

        try:
            atomic_write_json(resolved_path, {"runs": history})
            return True
        except Exception as e:
            logger.error(f"Failed saving batch trace run: {e}")
            return False
