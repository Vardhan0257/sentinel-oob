# Sentinel-OOB

Sentinel-OOB is a heartbeat-based security dead-man’s switch.
If an unattended endpoint stops speaking, it is assumed compromised.

The system focuses on alert delivery integrity, not malware detection or prevention.

## Project Structure

- `agent/` — Go-based Windows agent
- `server/` — Python FastAPI server
- `docs/` — Documentation
  - `specs/` — Architecture and protocols
  - `tests/` — Validation tests
  - `releases/` — Version changelogs
- `bin/` — Build outputs
- `CHANGELOG.md` — Project changelog
- `CONTRIBUTING.md` — Contribution guidelines
- `Makefile` — Build and run tasks

## Quick Start

1. Set `SENTINEL_HMAC_SECRET` environment variable.
2. Configure alert channels (webhook, Telegram, email).
3. Run server: `make run-server`
4. Run agent: `make run-agent`

See `docs/README.md` for detailed documentation.

## Roadmap

### v0.4 — Integrity & Audit Hardening (Current)
- Off-host append-only audit records
- Signed heartbeat messages
- Tamper-evident server logs
- Documented attacker evasion tests
- Adversarial validation completed

### Future
- Multi-platform agents
- Advanced presence detection
- Enterprise integrations
