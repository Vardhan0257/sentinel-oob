# Sentinel-OOB Agent (v0.1)

## Purpose
A dumb, noisy endpoint process that emits heartbeats.
Silence equals failure.

## Technology
- Language: Go
- Target OS: Windows
- Form: Console app (service later)

## Startup Contract
- Starts immediately
- Generates or loads a stable host_id
- Begins heartbeat loop
- Exits on fatal errors

## What This Is NOT
- Not a detector
- Not a protector
- Not resilient by itself
