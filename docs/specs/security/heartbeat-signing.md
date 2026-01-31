# Signed Heartbeats — Sentinel-OOB

## Threat Addressed
An attacker may spoof heartbeat packets to suppress silence-based alerts.

## Assumption
The attacker does not possess the shared secret stored on the endpoint and server.

## Design
Each heartbeat includes an HMAC-SHA256 signature computed over the payload.

## Verification
The server verifies the signature before accepting heartbeat state updates.

## Failure Mode
Invalid or missing signatures are treated as heartbeat loss.

## Non-Goals
- Preventing kernel-level key extraction
- Protecting against full OS compromise
