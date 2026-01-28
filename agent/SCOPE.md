# Sentinel-OOB Agent v0.1 — Scope

## Primary Role
Emit periodic heartbeats to the Sentinel-OOB server.

## Responsibilities
- Generate a stable host_id
- Send heartbeat every fixed interval (10s)
- Include lock state in each heartbeat
- Exit loudly on fatal errors

## Explicit Non-Responsibilities
- No silence detection
- No alerting
- No retries or buffering
- No local persistence
- No configuration files
- No auto-update logic

## Failure Semantics
- Agent crash = silence
- Network failure = silence
- Process kill = silence
