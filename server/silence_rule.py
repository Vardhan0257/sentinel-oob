import time
from server.state import last_heartbeat, last_lock_state
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30
CHECK_INTERVAL = 5

alerted = set()

def silence_detection_loop():
    while True:
        now = time.time()

        for host, ts in last_heartbeat.items():
            if now - ts > HEARTBEAT_TIMEOUT:
                locked = last_lock_state.get(host, True)
                if locked and host not in alerted:
                    send_alert(
                        f"Sentinel-OOB: {host} silent while unattended"
                    )
                    alerted.add(host)

        time.sleep(CHECK_INTERVAL)
