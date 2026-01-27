# Sentinel-OOB Agent (v0.1)

## Purpose
Act as a dumb, noisy hostage.
Continuously signal liveness and forward critical security events.

## Technology Choice
- Language: Go
- Form: Windows Service
- Reason: single static binary, low overhead, predictable runtime

## Responsibilities
- Emit heartbeat every fixed interval
- Report Windows Defender detection events
- Attach minimal context (host_id, lock state)
- Store no security-critical state locally

## Design Rules
- No local audit logs
- No retry queues
- No buffering
- Silence is failure

## Explicit Non-Goals
- Malware detection
- Prevention or blocking
- Local decision-making
