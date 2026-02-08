import time

from server.state import (
    last_heartbeat,
    last_inactive_seconds,
    presence_state,
    network_state,
)
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30      # seconds without heartbeat = silent
CHECK_INTERVAL = 5          # loop interval

alerted = set()


def silence_detection_loop():
    while True:
        now = time.time()

        for host, ts in list(last_heartbeat.items()):
            # Check silence
            if now - ts <= HEARTBEAT_TIMEOUT:
                continue

            inactive = last_inactive_seconds.get(host, 0)
            presence = presence_state.get(host, "UNKNOWN")
            network = network_state.get(host, "UNTRUSTED")

            if host in alerted:
                continue

            # -------- Risk-weighted escalation --------
            if presence == "ABSENT" and network == "UNTRUSTED":
                level = "LEVEL 3"
            elif inactive >= 300:
                level = "LEVEL 2"
            elif presence == "UNKNOWN":
                level = "LEVEL 1"
            else:
                continue
            # -----------------------------------------

            send_alert(
                f"Sentinel-OOB {level}: {host} silent "
                f"(inactive={inactive}s, presence={presence}, network={network})"
            )

            alerted.add(host)

        time.sleep(CHECK_INTERVAL)