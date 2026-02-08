# Sentinel-OOB Architecture

## Components

### Endpoint Agent
- Runs as a Windows service (v0.1)
- Emits periodic heartbeats
- Reports lock state and basic context
- Contains **no decision logic**
- Makes no attempt to hide, persist, or self-heal

### Server
- Receives heartbeats
- Maintains last-seen state per host
- Detects silence using time-based rules
- Applies escalation logic
- Sends alerts out-of-band

### Alert Channel
- Telegram / webhook / email / SMS (version dependent)
- Fully off-host
- Independent of endpoint integrity

## Data Flow

1. Agent sends heartbeat
2. Server updates in-memory state
3. Silence loop evaluates time since last heartbeat
4. Context is evaluated (presence, network)
5. Escalation is triggered
6. Alert is delivered externally

## Trust Boundaries

- Endpoint is untrusted after silence
- Server is trusted only until alert dispatch
- Alert channel is the final audit sink

## Core Principle

Silence is treated as a **security signal**, not a failure.
