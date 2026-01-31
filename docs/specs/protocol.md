# Sentinel-OOB Protocol

## Heartbeat (Agent → Server)

Sent every 10 seconds by default.

Fields:
- host_id (string)
- timestamp (unix epoch)
- locked (boolean)
- agent_version (string)
- network (optional, v0.2+)

## Silence Rule

If no heartbeat is received for >30 seconds:
- Endpoint is considered silent
- Silence is evaluated against context
- Escalation may occur

## Security Events (Optional)

Event-based signals may be added, but **silence always dominates**.

## Protocol Philosophy

- No acknowledgements
- No retries at protocol level
- Loss of communication is intentional signal
