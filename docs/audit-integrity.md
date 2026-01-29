# Sentinel-OOB Audit Integrity (v0.4)

## Goal
Ensure alerts cannot be silently erased post-detection.

## Strategy
- Alerts leave the endpoint immediately
- External systems act as audit sinks
- Local logs are not trusted

## Properties
- Tamper-evident
- Not tamper-proof
- Survives agent termination
- Survives log deletion

## Explicit Non-Guarantees
- No cryptographic immutability
- No forensic reconstruction
- No blockchain or append-only local logs

## Trust Boundary
Audit trust begins only once the alert leaves the host.
