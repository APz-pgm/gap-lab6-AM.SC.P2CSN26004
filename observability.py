from __future__ import annotations
import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

RUN_LOG_PATH = Path(os.getenv("RUN_LOG_PATH", "run_log.jsonl"))

def log_call(*, outcome, model, prompt_tokens=None, completion_tokens=None, cost=None,
             latency_ms=None, attempt=1, error=None, run_id=None):
    # Preserve the nine-field Lab 5 observability contract; unknowns stay null.
    row = {"timestamp": datetime.now(timezone.utc).isoformat(),
           "run_id": run_id or uuid.uuid4().hex[:12], "model": model,
           "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
           "cost": cost, "latency_ms": latency_ms, "attempt": attempt,
           "outcome": outcome}
    RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RUN_LOG_PATH.open("a", encoding="utf-8") as f: f.write(json.dumps(row)+"\n")
    return row
