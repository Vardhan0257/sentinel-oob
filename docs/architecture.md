# Architecture — Sentinel-OOB

## Core Principle
Silence is the signal.

## Components

### Agent (Endpoint)
- Runs as a Windows service
- Sends periodic heartbeats
- Forwards Defender security events
- Stores no security-critical state locally

### Server (Remote Listener)
- Tracks last-seen heartbeat per host
- Treats missing heartbeat as compromise
- Triggers out-of-band alerts immediately

## Design Rules
- Agent is dumb and noisy
- Server is paranoid and stateful
- No local audit trail; all events are off-host
- Network isolation equals compromise
