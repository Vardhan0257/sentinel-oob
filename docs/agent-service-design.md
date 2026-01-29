# Sentinel-OOB Agent — Windows Service Design (v0.1)

## Objective
Ensure the agent runs automatically, survives reboots, and stops only on deliberate administrative action.

## Service Characteristics
- Runs as a Windows Service
- Starts automatically on system boot
- Runs under LocalSystem or NetworkService
- No user interaction or UI

## Startup Behavior
- Service starts before user login
- Begins emitting heartbeats immediately
- Does not wait for network readiness

## Shutdown Behavior
- Service stop is treated as silence
- No graceful shutdown signaling
- No local cleanup or logging

## Failure Behavior
- Service crash or termination results in heartbeat loss
- Server interprets silence as potential compromise
- No restart logic inside the agent

## Installation Model
- Installed via `sc.exe` or PowerShell
- Single static Go binary
- No external runtime dependencies

## Security Posture
- Service is not hardened against admin attackers
- No attempt to hide or resist termination
- Relies on off-host detection for response
