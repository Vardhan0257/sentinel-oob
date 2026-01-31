import os
import hmac
import hashlib
from time import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from server.state import (
    last_heartbeat,
    last_lock_state,
    last_inactive_seconds,
    presence_state,
    network_state,
)

# =========================
# HMAC CONFIG (FAIL HARD)
# =========================

HMAC_SECRET = os.getenv("SENTINEL_HMAC_SECRET")
if not HMAC_SECRET:
    raise RuntimeError("SENTINEL_HMAC_SECRET not set on server")

# =========================
# APP
# =========================

app = FastAPI(title="Sentinel-OOB Server")

# =========================
# MODELS
# =========================

class Heartbeat(BaseModel):
    host_id: str
    timestamp: float
    locked: bool
    inactive_seconds: int
    network: str
    agent_version: str
    signature: str

    class Config:
        extra = "ignore"

# =========================
# CANONICAL STRING (MUST MATCH AGENT)
# =========================

def canonical_string(hb: Heartbeat) -> str:
    return (
        f"{hb.host_id}|"
        f"{int(hb.timestamp)}|"
        f"{hb.locked}|"
        f"{hb.inactive_seconds}|"
        f"{hb.network}|"
        f"{hb.agent_version}"
    )

# =========================
# SIGNATURE VERIFICATION
# =========================

def verify_signature(hb: Heartbeat) -> bool:
    msg = canonical_string(hb).encode()

    expected = hmac.new(
        HMAC_SECRET.encode(),
        msg,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, hb.signature)

# =========================
# ENDPOINT
# =========================

@app.post("/heartbeat")
def receive_heartbeat(hb: Heartbeat):
    if not verify_signature(hb):
        raise HTTPException(status_code=403, detail="Invalid signature")

    last_heartbeat[hb.host_id] = time()
    last_lock_state[hb.host_id] = hb.locked
    last_inactive_seconds[hb.host_id] = hb.inactive_seconds

    if hb.inactive_seconds >= 60 or hb.locked:
        presence_state[hb.host_id] = "ABSENT"
    else:
        presence_state[hb.host_id] = "PRESENT"

    network_state[hb.host_id] = hb.network

    return {"status": "ok"}
