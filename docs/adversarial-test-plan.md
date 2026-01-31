## Adversarial Test Plan — Sentinel-OOB v0.4

### 1. Test Scope

**System under test:** Sentinel-OOB
**Version:** v0.4
**Goal:** Validate security guarantees defined in the threat model by simulating realistic attacker behavior.

Out-of-scope attacks are explicitly ignored.

---

### 2. Attacker Models

| Attacker | Description                                        |
| -------- | -------------------------------------------------- |
| A1       | Malware running with user privileges               |
| A2       | Insider with local access                          |
| A3       | Network attacker (can block traffic)               |
| A4       | Alert-channel attacker (Telegram/Email disruption) |

---

### 3. Security Guarantees Under Test

| ID | Guarantee                            |
| -- | ------------------------------------ |
| G1 | Endpoint silence is detected         |
| G2 | Agent termination triggers alert     |
| G3 | Alerts cannot be suppressed silently |
| G4 | Forged heartbeats are rejected       |
| G5 | Alerts escape the compromised host   |

---

### 4. Test Cases

Now the important part.

#### **Test Case T1 — Kill the Agent**

**Attacker:** A1
**Action:**

* Terminate agent process / Windows service

**Expected Result:**

* No further heartbeats
* Server detects silence after timeout
* Out-of-band alert sent

**Observed Result:**

* ✅ Alert delivered via Telegram / Email

**Status:** PASS

---

#### **Test Case T2 — Block Network Connectivity**

**Attacker:** A3
**Action:**

* Disable network / firewall outbound traffic

**Expected Result:**

* Heartbeats stop
* Silence detected
* Alert sent via alternate channel if possible

**Observed Result:**

* ✅ Silence detected
* ⚠️ Delivery depends on channel availability

**Status:** PARTIAL PASS
**Notes:** Network dependency acknowledged in threat model.

---

#### **Test Case T3 — Forge Heartbeat Without Secret**

**Attacker:** A1
**Action:**

* Send fake `/heartbeat` without valid HMAC

**Expected Result:**

* Server rejects heartbeat
* No state update

**Observed Result:**

* ✅ HTTP 403 returned

**Status:** PASS

---

#### **Test Case T4 — Modify Heartbeat Payload**

**Attacker:** A1
**Action:**

* Change inactive_seconds / presence fields

**Expected Result:**

* Signature mismatch
* Heartbeat rejected

**Observed Result:**

* ✅ Rejected

**Status:** PASS

---

#### **Test Case T5 — Kill Alert Channel**

**Attacker:** A4
**Action:**

* Remove Telegram credentials
* Disable email

**Expected Result:**

* Alert attempts logged
* Failure visible
* No silent success

**Observed Result:**

* ✅ Alert failure logged
* Silence loop continues

**Status:** PASS

---

### 5. Known Limitations

* Network trust heuristic is coarse (domain membership only)
* No cryptographic chaining of audit logs
* No hardware-backed agent integrity

These are documented and accepted risks.

---

### 6. Summary

All **in-scope attacker actions either triggered alerts or failed visibly**.
No tested attack bypassed detection silently.

---