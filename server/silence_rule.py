import time
from server.state import last_heartbeat, last_lock_state
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30   # seconds
CHECK_INTERVAL = 5       # seconds

# host_id -> silence already alerted (bool)
silence_alerted = {}


def silence_detection_loop():
    while True:
        now = time.time()

        for host_id, last_seen in last_heartbeat.items():
            silent = now - last_seen > HEARTBEAT_TIMEOUT
            locked = last_lock_state.get(host_id)

            if silent and (locked is True or locked is None):
                if not silence_alerted.get(host_id, False):
                    send_alert(
                        f"Sentinel-OOB: endpoint {host_id} silent while unattended"
                    )
                    silence_alerted[host_id] = True
            else:
                # Reset latch when host speaks again
                silence_alerted[host_id] = False

        time.sleep(CHECK_INTERVAL)
