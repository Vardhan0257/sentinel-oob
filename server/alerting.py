import os
import requests
from server.telegram import send_telegram_alert
from server.email import send_email_alert


ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")

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

    # Telegram delivery (v0.3)
    try:
        send_telegram_alert(message)
        delivered = True
    except Exception as e:
        print(f"[ALERT] telegram failed: {e}")

    # Email delivery (v0.3)
    try:
        send_email_alert(message)
        delivered = True
    except Exception as e:
        print(f"[ALERT] email failed: {e}")

    if not delivered:
        raise RuntimeError("Alert delivery failed on all channels")

    print("ALERT DELIVERED")
