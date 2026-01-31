# Sentinel-OOB

**Out-of-Band Silence-Based Endpoint Compromise Detection**

---

## Overview

**Sentinel-OOB** is a defensive security system designed to detect **endpoint compromise, user incapacitation, or agent tampering** by treating **silence itself as a high-signal event**.

Instead of relying on local alerts, logs, or dashboards that malware can suppress, Sentinel-OOB:

* Continuously sends **signed heartbeat telemetry** from endpoints
* Treats **missing heartbeats** as a first-class security signal
* Escalates alerts **out-of-band** (Telegram / Email / Webhook)
* Assumes **endpoint compromise is possible**
* Assumes **local alerts cannot be trusted**

This is a **dead-man’s switch for endpoints**.

---

## Core Design Principle

> **If a protected endpoint goes silent while the user is absent, assume compromise.**

No malware classification.
No behavior modeling.
No trust in the endpoint once silence occurs.

---

## Architecture

```
┌──────────────┐         Signed Heartbeat         ┌──────────────────┐
│ Windows Host │ ──────────────────────────────▶ │ Sentinel-OOB      │
│ (Agent)      │                                  │ Server            │
│              │ ◀──── Out-of-Band Alerts ─────── │ (Watchman)        │
└──────────────┘                                  └──────────────────┘
```

---

## Components

### 1. Endpoint Agent (Go / Windows)

Runs as a **Windows Service** and periodically emits signed telemetry.

Collected signals:

* Stable `host_id`
* Heartbeat timestamp
* Session lock state
* User inactivity duration (seconds)
* Network trust context (domain-joined vs not)
* Agent version
* **HMAC signature (tamper resistance)**

The agent:

* Has **no local UI**
* Has **no local alerts**
* Cannot suppress escalation once silent

---

### 2. Server (Python / FastAPI)

Acts as a **paranoid remote watchman**.

Responsibilities:

* Verify HMAC-signed heartbeats
* Track last-seen state per host
* Infer **presence** from lock + inactivity
* Detect silence (`>30s`)
* Escalate via out-of-band channels
* Maintain off-host audit records

Non-responsibilities:

* Malware detection
* Dashboards
* Endpoint trust
* Forensics

---

## Detection Logic

### Presence Resolution (v0.2)

A host is considered **ABSENT** if **any** of the following are true:

* Session is locked
* User inactivity ≥ threshold (default: 60s)
* Presence state unknown

Otherwise: **PRESENT**

---

### Silence Rule (Core)

An alert is triggered if:

```
(no heartbeat > HEARTBEAT_TIMEOUT)
AND
(presence == ABSENT)
```

Silence while present does **not** escalate.

---

### Escalation Levels

Risk is weighted using **context**, not signatures:

| Condition                  | Escalation |
| -------------------------- | ---------- |
| ABSENT + UNTRUSTED network | Level 3    |
| ABSENT + TRUSTED network   | Level 2    |
| UNKNOWN presence           | Level 2    |
| Silent but PRESENT         | Level 1    |

Alerts are **one-shot per incident** (no storms).

---

## Alerting (Out-of-Band)

Supported channels:

* Telegram (primary)
* Email (SMTP)
* Generic Webhook
* Audit Webhook (append-only, off-host)

If **all channels fail**, the failure itself is logged.

---

## Security Properties

### Achieved Guarantees

* ✅ Detects agent termination
* ✅ Detects endpoint silence
* ✅ Bypasses local alert suppression
* ✅ Survives user-mode malware
* ✅ Signed telemetry prevents spoofing
* ✅ No reliance on endpoint logs
* ✅ No dashboards to blind

### Explicit Non-Guarantees

* ❌ Does not prevent compromise
* ❌ Does not attribute malware
* ❌ Does not resist kernel-level rootkits
* ❌ Does not provide forensic detail

This system is **detection-first**, not prevention.

---

## Threat Model (Summary)

Assumed attacker capabilities:

* Kill processes
* Disable Defender
* Block UI alerts
* Tamper with local logs
* Delay network traffic

Assumed attacker limitations:

* Cannot forge valid HMAC signatures
* Cannot suppress off-host alerts
* Cannot fake silence without detection

---

## Version History

### v0.1 — Dead-Man’s Switch

* Heartbeat liveness
* Silence detection
* Webhook escalation

### v0.2 — Context Awareness

* Presence inference
* Inactivity heuristic
* Network trust signal

### v0.3 — Transport Expansion

* Telegram alerts
* Email alerts
* Retry & backoff

### v0.4 — Integrity & Audit

* HMAC-signed telemetry
* Off-host audit hooks
* Tamper-evident alert trail

**Current Release:** `v0.4-final`

---

## Why This Is Different

Most security tools ask:

> “What does the endpoint say is happening?”

Sentinel-OOB asks:

> **“Why did the endpoint stop speaking?”**

That shift is the entire system.

---

## Project Status

🔒 **Feature-locked**
📌 **Code-frozen at v0.4**
🧠 **Threat model & adversarial testing in progress**

---

## Author Intent

This project is designed to:

* Survive attacker interference
* Fail loudly instead of silently
* Be understandable under incident pressure
* Trade complexity for reliability

