# Sentinel-OOB Protocol (v0.1)

## Heartbeat
Sent every 10 seconds by the endpoint agent.

Fields:
- host_id (string)
- timestamp (unix epoch)
- locked (boolean)
- agent_version (string)

## Security Event
Sent immediately when detected.

Fields:
- host_id (string)
- event_type (string)
- event_id (integer)
- timestamp (unix epoch)

## Silence Rule
If no heartbeat is received for >30 seconds:
- Treat as visibility loss
- Trigger out-of-band alert immediately
