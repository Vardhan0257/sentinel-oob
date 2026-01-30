import os
import smtplib
from email.message import EmailMessage


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")


def send_email_alert(message: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_EMAIL_TO]):
        raise RuntimeError("Email credentials not set")

    msg = EmailMessage()
    msg["Subject"] = "Sentinel-OOB Alert"
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL_TO
    msg.set_content(message)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
