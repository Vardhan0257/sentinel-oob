# Sentinel-OOB — Documentation Guide

This directory contains the **authoritative design and security documentation**
for Sentinel-OOB.

Sentinel-OOB is **not malware detection software**.
It is an **out-of-band dead-man’s switch** that assumes compromise on silence.

## How to Read

1. Start with `architecture.md` to understand the system.
2. Read `protocol.md` to understand heartbeat and silence rules.
3. Read `threat-model.md` to understand attacker assumptions.
4. Read `versions/` for version-specific behavior guarantees.
5. `audit-integrity.md` defines v0.4 integrity properties.
6. `roadmap.md` shows what is done and what is explicitly deferred.

## Design Rule

If a behavior is not documented here, it is **not guaranteed**.
