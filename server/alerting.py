import os
import requests
import time
from server.telegram import send_telegram_alert
from server.email_alert import send_email_alert
from server.audit_log import append_audit

ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")
AUDIT_WEBHOOK_URL = os.getenv("AUDIT_WEBHOOK_URL")

def send_alert(message: str):
    delivered = False

    # Webhook delivery (v0.2 compatibility)
    if ALERT_WEBHOOK_URL:
        try:
            requests.post(
                ALERT_WEBHOOK_URL,
                json={"text": message},
                timeout=5,
            )
            delivered = True
        except Exception as e:
            print(f"[ALERT] webhook failed: {e}")

    # Telegram delivery with retry + backoff
    for attempt in range(3):
        try:
            send_telegram_alert(message)
            delivered = True
            break
        except Exception as e:
            print(f"[ALERT] telegram attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)

    # Email delivery (v0.3)
    try:
        send_email_alert(message)
        delivered = True
    except Exception as e:
        print(f"[ALERT] email failed: {e}")

    if not delivered:
        raise RuntimeError("Alert delivery failed on all channels")

    if delivered and AUDIT_WEBHOOK_URL:
        try:
            requests.post(
                AUDIT_WEBHOOK_URL,
                json={
                    "event": "ALERT_DELIVERED",
                    "message": message,
                    "timestamp": time.time(),
                },
                timeout=5,
            )
            print("[AUDIT] record sent")
        except Exception as e:
            print(f"[AUDIT] failed: {e}")

    append_audit(
        event_type="ALERT",
        data={"message": message}
    )

    print("ALERT DELIVERED")
