# Sentinel-OOB

Sentinel-OOB is a heartbeat-based security dead-man’s switch.
If an unattended endpoint stops speaking, it is assumed compromised.

The system focuses on alert delivery integrity, not malware detection or prevention.

## Roadmap

### v0.1 — Dead-Man’s Switch (Current)
- Heartbeat-based endpoint liveness monitoring
- Silence-as-signal detection
- Windows service agent (Go)
- Server-side silence escalation
- Webhook-based out-of-band alerting
- No local logs, no ML, no dashboards

### v0.2 — Context-Aware Escalation
- Presence heuristics (lock state + inactivity)
- Network context awareness (public vs trusted Wi-Fi)
- Risk-weighted escalation rules
- Improved alert cooldown handling

### v0.3 — Platform & Transport Expansion
- Email and push notification providers
- Linux agent support (systemd + auditd heartbeat)
- Configurable heartbeat intervals
- Retry and backoff for unreliable networks

### v0.4 — Integrity & Audit Hardening
- Off-host append-only audit records
- Signed heartbeat messages
- Tamper-evident server logs
- Documented attacker evasion tests
