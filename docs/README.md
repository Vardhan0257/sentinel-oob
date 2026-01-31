# Sentinel-OOB — Documentation Guide

This directory contains the **authoritative design and security documentation**
for Sentinel-OOB.

Sentinel-OOB is **not malware detection software**.
It is an **out-of-band dead-man’s switch** that assumes compromise on silence.

## Directory Structure

- `specs/` — Core system specifications
  - `architecture.md` — System overview and components
  - `protocol.md` — Heartbeat protocol and silence rules
  - `threat-model.md` — Attacker model and assumptions
  - `security/` — Security specifications
    - `heartbeat-signing-spec.md`
    - `heartbeat-signing.md`
- `releases/` — Version-specific documentation
  - `v0.1.md` to `v0.4.md`
- `tests/` — Validation and testing
  - `adversarial-test-plan.md`
  - `adversarial-test-results.md`
- `audit-integrity.md` — Integrity properties
- `paper.md` — Research paper
- `roadmap.md` — Development roadmap

## How to Read

1. Start with `specs/architecture.md` to understand the system.
2. Read `specs/protocol.md` to understand heartbeat and silence rules.
3. Read `specs/threat-model.md` to understand attacker assumptions.
4. Read `releases/` for version-specific behavior guarantees.
5. `audit-integrity.md` defines v0.4 integrity properties.
6. `roadmap.md` shows what is done and what is explicitly deferred.

## Design Rule

If a behavior is not documented here, it is **not guaranteed**.
