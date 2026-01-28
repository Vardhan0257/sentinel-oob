"""
Sentinel-OOB Server v0.1

Remote watchman responsible for detecting endpoint silence
and escalating alerts.
"""

import threading
import uvicorn

from api import app
from silence_rule import silence_detection_loop

if __name__ == "__main__":
    t = threading.Thread(target=silence_detection_loop, daemon=True)
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)
