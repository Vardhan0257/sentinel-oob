"""
Sentinel-OOB Server API (v0.1)

Defines external interfaces only.
No business logic implemented here.
"""

from fastapi import FastAPI

app = FastAPI(title="Sentinel-OOB Server")

@app.post("/heartbeat")
def receive_heartbeat():
    pass

@app.post("/event")
def receive_event():
    pass
