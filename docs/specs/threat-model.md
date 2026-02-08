# Sentinel-OOB — Formal Threat Model (Final)

## 1. System Goal (What This System Is Actually For)

### Primary Goal

> Detect endpoint compromise, user incapacitation, or agent tampering by observing **loss of trusted telemetry**, and escalate alerts **outside the endpoint’s control**.

Sentinel-OOB treats **silence as a security signal**.

### Explicitly NOT the Goal

Sentinel-OOB is **not** designed for:

* Malware detection
* Intrusion prevention
* Endpoint hardening
* Digital forensics
* Root-cause analysis

It is a **last-line detection and escalation system**, activated when traditional controls are bypassed or disabled.

---

## 2. Assets to Protect

These assets define what Sentinel-OOB is responsible for signaling or preserving.

### Primary Assets

| Asset                 | Description                               |
| --------------------- | ----------------------------------------- |
| Endpoint liveness     | Whether the endpoint is operational       |
| User presence         | Whether a human is actively present       |
| Telemetry integrity   | Whether heartbeats are authentic          |
| Alert delivery        | Whether alerts escape endpoint control    |
| Detection reliability | Whether silence is detected and escalated |

### Explicit Non-Assets (Out of Scope)

The system does **not** protect:

* Filesystem integrity
* Memory integrity
* Credential secrecy
* Malware samples
* Kernel or rootkit detection

Failure to protect these is **intentional**, not a flaw.

---

## 3. Deployment Assumptions

Sentinel-OOB assumes:

* A **secure initial provisioning phase** where secrets are installed out-of-band
* At least **one successful registration** with the server
* The Sentinel-OOB server and alert channels are reachable during normal operation

If these assumptions fail, the system **fails loud**.

---

## 4. Trust Boundaries

Trust boundaries define where security assumptions stop.

### Fully Trusted

* Sentinel-OOB server
* Out-of-band alert channels (Telegram / Email / Webhook)
* Shared HMAC secret (provisioned out-of-band)

### Conditionally Trusted

* Endpoint **only while it emits valid, signed heartbeats**

### Explicitly Untrusted

* Endpoint operating system
* Endpoint user space
* Local logs
* Local alerts
* Local UI
* Local clock
* Endpoint network environment

> **Once the endpoint goes silent, it is assumed hostile or dead.**

---

## 5. Attacker Model

### Attacker Capabilities (Assumed)

The attacker **can**:

* Kill or suspend the Sentinel-OOB agent
* Disable Windows services
* Disable Defender or EDR
* Suppress local alerts and UI
* Modify or erase local logs
* Delay, drop, or shape outbound traffic
* Operate with Administrator privileges
* Persist across reboots
* Act while the user is absent

This represents a **strong, realistic attacker**.

---

### Attacker Capabilities (Not Assumed)

The attacker **cannot**:

* Forge valid HMAC signatures without the shared secret
* Suppress external alert channels
* Modify server-side state
* Prevent silence detection after heartbeats stop
* Reliably fake user presence remotely

These are **hard trust boundaries**.

---

## 6. Threats Considered

### T1 — Agent Termination

**Attack**
Attacker kills or disables the agent.

**Detection**

* Heartbeats stop
* Silence timeout triggers escalation

**Status**
✅ Detected

---

### T2 — Agent Tampering / Spoofed Heartbeats

**Attack**
Attacker sends forged heartbeats.

**Detection**

* Invalid HMAC signature
* Heartbeat rejected

**Status**
✅ Prevented

---

### T3 — Local Alert Suppression

**Attack**
Attacker disables popups, logs, Defender alerts.

**Detection**

* Alerts are out-of-band
* Endpoint has no control over escalation

**Status**
✅ Immune by design

---

### T4 — User-Absent Compromise

**Attack**
Attacker compromises endpoint while user is away.

**Detection**

* User inactivity heuristic
* Lock state correlation
* Silence escalation

**Status**
✅ Detected

---

### T5 — Network Manipulation

**Attack**
Attacker operates on an untrusted or hostile network.

**Detection**

* Network context reduces trust level
* Escalation severity increases

**Status**
⚠️ Minimal heuristic (domain-join / context only)

---

### T6 — Replay Attacks

**Attack**
Attacker replays old signed heartbeats.

**Detection**

* Timestamp mismatch
* Heartbeat window validation

**Status**
⚠️ Partially mitigated

**Planned Improvement**

* Monotonic counters or server-issued nonces

---

### T7 — Server Compromise

**Attack**
Attacker compromises Sentinel-OOB server.

**Detection**

* Out of scope

**Status**
❌ Explicitly not defended

This is an **acceptable limitation**.

---

## 7. Explicit Security Guarantees

Sentinel-OOB **guarantees**:

1. If the endpoint goes silent, it will be detected
2. If the agent is killed, detection occurs
3. If local alerts are suppressed, escalation still happens
4. If telemetry is tampered with, it is rejected
5. If the user is absent, silence is treated as suspicious
6. If network trust degrades, escalation severity increases

These guarantees hold **only while the server and secrets remain uncompromised**.

---

## 8. Explicit Non-Guarantees

Sentinel-OOB does **not** guarantee:

* Detection of stealthy kernel rootkits
* Protection against hardware implants
* Detection if the attacker perfectly mimics valid heartbeats
* Detection if the server is compromised
* Prevention of endpoint compromise

These exclusions are **intentional and documented**.

---

## 9. Failure Modes (Fail-Loud Design)

| Failure               | System Behavior |
| --------------------- | --------------- |
| Agent crash           | Alert           |
| Network outage        | Alert           |
| Signature mismatch    | Reject + alert  |
| Alert channel failure | Retry + log     |
| All channels fail     | Hard error      |

> Network outages are **indistinguishable from adversarial suppression** and are escalated by design.

Sentinel-OOB **fails loud**, not safe.

---

## 10. Why This Threat Model Is Strong

This threat model:

* States attacker power explicitly
* Refuses impossible guarantees
* Defines trust boundaries clearly
* Treats silence as meaningful telemetry
* Remains valid under endpoint compromise

This makes Sentinel-OOB **defensible under review, viva, or security audit**.


