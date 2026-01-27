# Server Responsibilities — Sentinel-OOB (v0.1)

## Core Role
Act as the paranoid watchman. Assume compromise on silence.

## Inputs
- Heartbeat packets from endpoints
- Security event packets (Defender)

## State Tracked
- Last heartbeat timestamp per host
- Last known lock state per host

## Decision Rule
If no heartbeat is received for >30 seconds
AND last known state is locked or unknown,
then escalate immediately.

## Outputs
- Out-of-band alert via webhook/push
- Off-host audit record of the event

## Non-Responsibilities
- No malware detection
- No correlation engine
- No dashboards
- No local endpoint trust
