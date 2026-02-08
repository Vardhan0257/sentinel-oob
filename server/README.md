# Sentinel-OOB Server (v0.4)

## Purpose
Act as the remote watchman that detects endpoint silence and escalates alerts.

## Technology Choice
- Language: Python
- Reason: fast iteration, clear logic, sufficient for v0.4

## Responsibilities
- Receive heartbeat packets
- Track last-seen state per host
- Detect silence (>30s)
- Trigger out-of-band alert

## Explicit Non-Goals
- High availability
- Horizontal scaling
- Enterprise hardening
