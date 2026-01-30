from time import time
from fastapi import FastAPI
from pydantic import BaseModel

from server.state import (
    last_heartbeat,
    last_lock_state,
    last_inactive_seconds,
    presence_state,
    network_state,
)

app = FastAPI(title="Sentinel-OOB Server")


class Heartbeat(BaseModel):
    host_id: str
    timestamp: float
    locked: bool
    inactive_seconds: int
    agent_version: str


@app.post("/heartbeat")
def receive_heartbeat(hb: Heartbeat):
    last_heartbeat[hb.host_id] = time()
    last_lock_state[hb.host_id] = hb.locked
    last_inactive_seconds[hb.host_id] = hb.inactive_seconds

    # v0.2 presence resolution
    if hb.inactive_seconds >= 60:
        presence_state[hb.host_id] = "ABSENT"
    elif hb.locked is True:
        presence_state[hb.host_id] = "ABSENT"
    elif hb.locked is False:
        presence_state[hb.host_id] = "PRESENT"
    else:
        presence_state[hb.host_id] = "UNKNOWN"

    # v0.2 placeholder
    network_state[hb.host_id] = "UNKNOWN"

    return {"status": "ok"}


@app.post("/event")
def receive_event():
    pass

