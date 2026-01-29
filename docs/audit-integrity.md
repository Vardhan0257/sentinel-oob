# Sentinel-OOB Audit Integrity (v0.4)

## Goal
Ensure security-relevant events cannot be silently erased after detection.

## Design Choice
Sentinel-OOB does not rely on local audit logs for security guarantees.

## Rationale
Any data stored solely on the endpoint is assumed deletable by a local attacker.

## Audit Strategy
- All alerts are transmitted off-host immediately
- External systems (webhook / Telegram) act as the audit sink
- Loss of connectivity is itself treated as a security signal

## Properties
- Tamper-evident by design
- Not tamper-proof
- Survives local process termination
- Survives local log deletion

## Explicit Limitations
- No cryptographic immutability guarantees
- No blockchain or append-only local logs
- No forensic reconstruction after full compromise

## Trust Boundary
Audit trust begins only once the alert leaves the endpoint.
