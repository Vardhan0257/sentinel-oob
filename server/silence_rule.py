import time
from server.state import last_heartbeat, last_lock_state
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30   # seconds
CHECK_INTERVAL = 5       # seconds

# host_id -> last alert timestamp
last_alert_sent = {}


def silence_detection_loop():
    while True:
        now = time.time()

        for host_id, last_seen in last_heartbeat.items():
            if now - last_seen > HEARTBEAT_TIMEOUT:
                locked = last_lock_state.get(host_id)

                if locked is True or locked is None:
                    last_alert = last_alert_sent.get(host_id)

                    # Send only one alert per silence episode
                    if last_alert is None or last_alert < last_seen:
                        send_alert(
                            f"Sentinel-OOB: endpoint {host_id} silent while unattended"
                        )
                        last_alert_sent[host_id] = now

        time.sleep(CHECK_INTERVAL)
