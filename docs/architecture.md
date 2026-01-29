# Sentinel-OOB Architecture (v0.1)

## Components

### Endpoint Agent (Hostage)
- Runs as a lightweight process
- Emits periodic heartbeats
- Reports lock/unlock state
- Contains no decision logic

### Server (Watchman)
- Receives heartbeats and events
- Tracks last-seen state per host
- Detects silence using time-based rules
- Escalates alerts out-of-band

### Alert Channel
- Webhook / push / SMS / email
- Off-host by design
- Independent of endpoint state

## Data Flow

1. Agent sends heartbeat → Server
2. Server updates in-memory state
3. Silence detection loop evaluates time since last heartbeat
4. If silence exceeds threshold during unattended state → alert
5. Alert is delivered out-of-band

## Trust Boundaries

- Endpoint is untrusted after silence
- Server is trusted until alert delivery
- Alert channel is independent and external

## Design Principle

Silence is treated as a first-class security signal.
