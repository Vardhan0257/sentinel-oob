import time
from state import last_heartbeat, last_lock_state
from alerting import send_alert

HEARTBEAT_TIMEOUT = 30  # seconds
CHECK_INTERVAL = 5      # seconds


def silence_detection_loop():
    """
    Periodically checks for endpoint silence.
    Silence during locked or unknown state triggers escalation.
    """
    while True:
        now = time.time()

        for host_id, last_seen in last_heartbeat.items():
            if now - last_seen > HEARTBEAT_TIMEOUT:
                locked = last_lock_state.get(host_id)

                if locked is True or locked is None:
                    send_alert(
                        f"Sentinel-OOB: endpoint {host_id} silent while unattended"
                    )

        time.sleep(CHECK_INTERVAL)
