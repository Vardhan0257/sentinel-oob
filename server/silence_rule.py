"""
Sentinel-OOB Silence Rule (v0.1)

Core invariant:
If an unattended endpoint stops sending heartbeats,
visibility is assumed lost and escalation must occur.

This rule is intentionally simple and conservative.
"""

# Pseudocode only — no logic yet
#
# if current_time - last_heartbeat[host_id] > HEARTBEAT_TIMEOUT:
#     if last_lock_state[host_id] is True or unknown:
#         send_alert(...)
