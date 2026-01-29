import time
from server.state import last_heartbeat, presence_state
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30
CHECK_INTERVAL = 5

alerted = set()

def silence_detection_loop():
    while True:
        now = time.time()

        for host, ts in last_heartbeat.items():
            if now - ts > HEARTBEAT_TIMEOUT:
                state = presence_state.get(host, "UNKNOWN")

                if state in ("ABSENT", "UNKNOWN") and host not in alerted:
                    send_alert(
                        f"Sentinel-OOB: {host} silent while {state.lower()}"
                    )
                    alerted.add(host)

        time.sleep(CHECK_INTERVAL)
