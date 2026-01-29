from time import time
from fastapi import FastAPI
from pydantic import BaseModel

from server.state import last_heartbeat, last_lock_state

app = FastAPI(title="Sentinel-OOB Server")

class Heartbeat(BaseModel):
    host_id: str
    timestamp: float
    locked: bool
    agent_version: str

@app.post("/heartbeat")
def receive_heartbeat(hb: Heartbeat):
    last_heartbeat[hb.host_id] = time()
    last_lock_state[hb.host_id] = hb.locked
    return {"status": "ok"}

@app.post("/event")
def receive_event():
    pass