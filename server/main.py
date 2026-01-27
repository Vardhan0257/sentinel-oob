"""
Sentinel-OOB Server v0.1

Remote watchman responsible for detecting endpoint silence
and escalating alerts.

No business logic implemented yet.
"""

import uvicorn
from api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
