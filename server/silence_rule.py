import time
from server.state import last_heartbeat, presence_state, network_state
from server.alerting import send_alert

HEARTBEAT_TIMEOUT = 30
CHECK_INTERVAL = 5

alerted = set()

def silence_detection_loop():
    while True:
        now = time.time()

        for host, ts in last_heartbeat.items():
            if now - ts <= HEARTBEAT_TIMEOUT:
                continue

            presence = presence_state.get(host, "UNKNOWN")
            network = network_state.get(host, "UNKNOWN")

            # Determine escalation level
            if presence == "ABSENT" and network == "UNTRUSTED":
                level = "LEVEL 3"
            elif presence in ("ABSENT", "UNKNOWN") and network == "TRUSTED":
                level = "LEVEL 2"
            elif presence == "UNKNOWN":
                level = "LEVEL 2"
            else:
                level = "LEVEL 1"

            if host not in alerted:
                send_alert(
                    f"Sentinel-OOB {level}: {host} silent "
                    f"(presence={presence}, network={network})"
                )
                alerted.add(host)

        time.sleep(CHECK_INTERVAL)
