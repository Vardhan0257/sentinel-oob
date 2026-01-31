## Sentinel-OOB: Silence-as-Signal for Out-of-Band Endpoint Compromise Detection

### Abstract

* What problem exists
* Why it’s hard
* What Sentinel-OOB does differently
* What threat model you assume
* What the system achieves

### 1. Introduction

Purpose:

* Set context
* Explain *why this problem matters*

You should answer:

* Why EDRs fail after compromise
* Why attackers try to suppress alerts
* Why “agent silence” is meaningful

No implementation details yet.

---

### 2. Problem Statement

Be precise and brutal.

State clearly:

* What attackers do after gaining access
* Why local logging and alerts cannot be trusted
* Why existing heartbeat systems are insufficient

End with:

> **Goal:** Detect endpoint compromise even when the endpoint is actively hostile.

---

### 3. System Overview

High-level architecture (no code).

Describe:

* Agent
* Server
* Out-of-band alerting
* Trust boundaries

Mention:

* Heartbeats
* Presence + inactivity
* HMAC-signed telemetry
* External alert channels

This section explains *what exists*, not how it’s implemented.

---

### 4. Threat Model

This should reference your threat model document.

Include:

* Attacker capabilities (user-level malware, network blocking, alert disruption)
* Explicit non-goals (kernel rootkits, hardware compromise)

Make it clear you **chose constraints deliberately**.

---

### 5. Design Decisions

This is where your project becomes impressive.

Explain **why** you chose:

* Silence-as-signal instead of event detection
* Out-of-band delivery
* HMAC instead of TLS client certs
* Fail-loud behavior instead of fail-silent

Each decision should be defended in 2–4 sentences.

---

### 6. Adversarial Evaluation

Reference your adversarial test plan.

Summarize:

* What attacks were attempted
* What guarantees held
* What partially failed
* What failed by design

This is where honesty increases credibility.

---

### 7. Limitations

This section is mandatory.

Explicitly list:

* Network trust heuristic limitations
* Lack of cryptographic audit chaining
* Dependence on external alert channels
* No kernel-level integrity

A reviewer trusts a system **more** when limitations are clear.

---

### 8. Future Work

Short, realistic, non-fantasy:

* Hash-chained audit logs
* Hardware-backed secrets
* Richer network context
* Policy-driven escalation

No promises. Just directions.

---

### 9. Conclusion

Restate:

* What Sentinel-OOB proves
* Why silence-based detection is valuable
* What survived adversarial pressure

End strong but restrained.

---