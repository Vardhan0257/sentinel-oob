"""
Sentinel-OOB Server State (v0.2)

In-memory state only.
No persistence. No logic.
"""

# host_id -> last heartbeat timestamp
last_heartbeat = {}

# host_id -> last known lock state (True / False / None)
last_lock_state = {}

# host_id -> presence state (PRESENT / ABSENT / UNKNOWN)
presence_state = {}

# host_id -> network context (TRUSTED / UNTRUSTED / UNKNOWN)
network_state = {}

# host_id -> last reported inactivity seconds
last_inactive_seconds = {}
