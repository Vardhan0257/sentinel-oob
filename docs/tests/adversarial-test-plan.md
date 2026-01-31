# Adversarial Test Plan

**Project:** Sentinel-OOB
**Version:** v0.4
**Phase:** 4 — Adversarial Validation
**Objective:** Attempt to violate Sentinel-OOB’s security guarantees under realistic attacker capabilities.

---

## 1. Purpose of This Document

This document defines **deliberate attacker simulations** designed to test whether Sentinel-OOB upholds its core guarantees under hostile conditions.

Unlike unit tests, these scenarios:

* Assume **partial or full endpoint compromise**
* Treat the agent as **untrusted**
* Treat silence as **intentional attack behavior**
* Focus on **system failure modes**

---

## 2. Attacker Model

### Attacker Capabilities

The attacker **may**:

* Kill or stop the agent process
* Disable local notifications
* Tamper with outbound network traffic
* Replay or forge heartbeat messages
* Disconnect the host from the network
* Crash or restart the server
* Access the endpoint OS with user or admin privileges

The attacker **cannot**:

* Break cryptographic primitives (HMAC-SHA256)
* Access shared secrets stored securely on server
* Modify off-host alert destinations (Telegram, email)

---

## 3. Security Guarantees Under Test

| ID | Guarantee                                   |
| -- | ------------------------------------------- |
| G1 | Agent termination is detected               |
| G2 | Alert delivery cannot be suppressed locally |
| G3 | Silence is treated as compromise            |
| G4 | Presence context reduces false positives    |
| G5 | Telemetry tampering is rejected             |
| G6 | Replay attacks do not suppress alerts       |
| G7 | Alerts survive partial delivery failure     |

---

## 4. Test Environment

* **Agent OS:** Windows 10 / 11
* **Agent Mode:** Debug (non-service) and Service
* **Server:** FastAPI (local or remote)
* **Alert Channels:** Telegram + Email (at least one enabled)
* **Secrets:** Shared HMAC secret set on agent and server

---

## 5. Test Cases

---

### 🔴 Test 1 — Hard Agent Kill

**Guarantee:** G1 (Agent kill detection)

**Attack steps**

```powershell
taskkill /IM sentinel-agent.exe /F
```

**Expected result**

* No heartbeat after timeout
* Silence detection triggers alert

**Pass criteria**

* Alert delivered within expected window

---

### 🔴 Test 2 — Graceful Agent Stop

**Guarantee:** G1 (edge case)

**Attack steps**

```powershell
sc stop SentinelOOB
```

**Expected result**

* Treated identically to hard kill
* Alert still fired

**Pass criteria**

* Alert delivered

---

### 🔴 Test 3 — Local Notification Suppression

**Guarantee:** G2 (Out-of-band delivery)

**Attack steps**

* Disable Windows notifications
* Close Telegram desktop
* Close email client

**Expected result**

* Alerts still arrive externally (phone / external inbox)

**Pass criteria**

* Alert delivered via Telegram or email

---

### 🔴 Test 4 — Network Disconnect

**Guarantee:** G3 (Silence as signal)

**Attack steps**

* Disable Wi-Fi or unplug Ethernet
* Leave agent running

**Expected result**

* Heartbeats stop
* Silence triggers alert

**Pass criteria**

* Alert delivered

---

### 🔴 Test 5 — Presence False Positive Control

**Guarantee:** G4 (Context awareness)

#### Scenario A (No alert)

* User active
* Mouse/keyboard input
* Heartbeats flowing

#### Scenario B (Alert)

* Screen locked
* Inactivity threshold exceeded
* Agent stopped

**Pass criteria**

* Alert only in Scenario B

---

### 🔴 Test 6 — Telemetry Tampering

**Guarantee:** G5 (Signed telemetry)

**Attack steps**

```bash
curl -X POST http://server:8000/heartbeat \
  -d '{"host_id":"fake","timestamp":0,"locked":false}'
```

**Expected result**

* 403 rejection
* No state update

**Pass criteria**

* Server rejects tampered heartbeat

---

### 🔴 Test 7 — Replay Attack

**Guarantee:** G6 (Replay resistance)

**Attack steps**

* Capture a valid heartbeat
* Replay repeatedly after killing agent

**Expected result**

* Silence still detected
* Replay does not suppress alert

**Pass criteria**

* Alert delivered despite replay

---

### 🔴 Test 8 — Partial Alert Channel Failure

**Guarantee:** G7 (Delivery resilience)

**Attack steps**

* Remove Telegram credentials
* Break webhook URL
* Leave email enabled

**Expected result**

* Alert delivered via remaining channel

**Pass criteria**

* At least one channel succeeds

---

### 🔴 Test 9 — Server Crash Recovery (Bonus)

**Attack steps**

```bash
kill -9 server
restart server
```

**Expected result**

* Server recovers cleanly
* New heartbeats processed

**Pass criteria**

* No crash loops or undefined behavior

---

## 6. Result Recording Format

Create:

```
docs/adversarial-test-results.md
```

For **each test**:

```markdown
### Test X — <Name>

**Goal:**  
**Attack steps:**  
**Expected result:**  
**Observed result:**  
**Verdict:** PASSED / FAILED  
**Notes:**  
```

Failures **must be documented**, not hidden.

---

## 7. Success Criteria

Sentinel-OOB is considered **adversarially validated** if:

* All tests G1–G7 pass
* Failures (if any) are explicitly documented
* No silent failure modes exist

---

## 8. What This Proves

If successful, Sentinel-OOB demonstrates:

* Detection beyond local trust
* Robust silence-as-signal semantics
* Cryptographically enforced telemetry integrity
* Practical resilience against common attacker tactics

This elevates the project from **implementation** to **security research artifact**.

---

## 9. What Comes Next

After this phase:

1. Freeze code
2. Summarize failures & survivals
3. Finalize paper-style writeup

---