import time

from server.state import (
    last_heartbeat,
    last_inactive_seconds,
    presence_state,
)
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30
CHECK_INTERVAL = 5

alerted = set()

def silence_detection_loop():
    while True:
        now = time.time()

        for host, ts in last_heartbeat.items():
            if now - ts > HEARTBEAT_TIMEOUT:
                inactive = last_inactive_seconds.get(host, 0)
                presence = presence_state.get(host, "UNKNOWN")

                if (presence == "ABSENT" or inactive >= 300) and host not in alerted:
                    send_alert(
                        f"Sentinel-OOB: {host} silent "
                        f"(inactive={inactive}s, presence={presence})"
                    )
                    alerted.add(host)

        time.sleep(CHECK_INTERVAL)
