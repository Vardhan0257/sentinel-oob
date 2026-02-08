import os
import json
import hashlib
import time
import threading

AUDIT_LOG_PATH = os.getenv("SENTINEL_AUDIT_LOG", "audit.log")

_lock = threading.Lock()
_last_hash = None


def _hash_entry(entry: dict) -> str:
    raw = json.dumps(entry, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def append_audit(event_type: str, data: dict):
    """
    Append-only, hash-chained audit record.
    If any record is modified or removed, the chain breaks.
    """
    global _last_hash

    with _lock:
        entry = {
            "ts": time.time(),
            "event": event_type,
            "data": data,
            "prev_hash": _last_hash,
        }

        entry_hash = _hash_entry(entry)
        entry["hash"] = entry_hash

        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        _last_hash = entry_hash
