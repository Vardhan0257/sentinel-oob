import os
import requests

ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")


def send_alert(message: str):
    if not ALERT_WEBHOOK_URL:
        raise RuntimeError("ALERT_WEBHOOK_URL is not set")

    payload = {
        "text": message
    }

    requests.post(ALERT_WEBHOOK_URL, json=payload, timeout=5)

    print("ALERT POST SENT")
