import os

HMAC_SECRET = os.getenv("SENTINEL_HMAC_SECRET")

if not HMAC_SECRET:
    raise RuntimeError("SENTINEL_HMAC_SECRET not set")
