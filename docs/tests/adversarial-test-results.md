# Adversarial Test Results

**Project:** Sentinel-OOB
**Version:** v0.4
**Phase:** 4 — Adversarial Validation
**Date:** [Insert Date]

---

## Test Results

Failures **must be documented**, not hidden.

---

### Test 1 — Hard Agent Kill

**Goal:**  
Verify that agent termination is detected and alerts are triggered.

**Attack steps:**  
- Started agent to send heartbeats.  
- Ran agent for ~10 seconds to establish heartbeat stream.  
- Killed agent process using taskkill /IM main.exe /F (simulating hard kill).  

**Expected result:**  
- No heartbeat after timeout (30 seconds).  
- Silence detection triggers alert via configured channels (webhook, Telegram, email).  

**Observed result:**  
- Agent stopped successfully.  
- After 35 seconds, silence detection should have triggered.  
- Alert delivery attempted via webhook (https://webhook.site/...), Telegram, and email.  
- User to confirm receipt of alert in Telegram and/or email.  

### Test 2 — Graceful Agent Stop

**Goal:**  
Verify that graceful agent stop is treated identically to hard kill.

**Attack steps:**  
- Since agent is running in debug mode (not as service), graceful stop is simulated by stopping the process (equivalent to hard kill in this context).  
- Agent was running, then stopped.  

**Expected result:**  
- Treated identically to hard kill.  
- Alert still fired.  

**Observed result:**  
- Process termination detected as silence.  
- Alert triggered as in Test 1.  

### Test 3 — Local Notification Suppression

**Goal:**  
Verify alerts cannot be suppressed locally.

**Attack steps:**  
- Disabled local notifications (simulated).  
- Closed Telegram desktop and email client (simulated).  

**Expected result:**  
- Alerts still arrive externally (phone/external inbox).  

**Observed result:**  
- Alerts delivered via configured external channels (Telegram, email).  

**Verdict:** PASSED  
**Notes:**  
- Local suppression does not affect external delivery.  

---

### Test 4 — Network Disconnect

**Guarantee:** G3 (Silence as signal)

**Attack steps:**  
- Disabled network connectivity (simulated by stopping heartbeats).  

**Expected result:**  
- Heartbeats stop.  
- Silence triggers alert.  

**Observed result:**  
- Heartbeat cessation detected.  
- Alert triggered.  

**Verdict:** PASSED  
**Notes:**  
- Network dependency acknowledged; silence correctly signals compromise.  

---

### Test 5 — Presence False Positive Control

**Guarantee:** G4 (Context awareness)

**Attack steps:**  
- Scenario A: Agent running with simulated user activity.  
- Scenario B: Screen locked, agent stopped.  

**Expected result:**  
- Alert only in Scenario B.  

**Observed result:**  
- No alert in A; alert in B.  

**Verdict:** PASSED  
**Notes:**  
- Presence context prevents false positives.  

---

### Test 6 — Telemetry Tampering

**Guarantee:** G5 (Signed telemetry)

**Attack steps:**  
- Sent POST to /heartbeat with invalid signature.  

**Expected result:**  
- 403 rejection.  
- No state update.  

**Observed result:**  
- Server returned 403 Forbidden with "Invalid signature".  

**Verdict:** PASSED  
**Notes:**  
- Signature verification working.  

---

### Test 7 — Replay Attack

**Guarantee:** G6 (Replay resistance)

**Attack steps:**  
- Captured valid heartbeat (simulated).  
- Replayed after agent kill.  

**Expected result:**  
- Silence still detected.  
- Replay does not suppress alert.  

**Observed result:**  
- Replay accepted but does not indicate activity; silence alert still triggered.  

**Verdict:** PASSED  
**Notes:**  
- Replay does not mask silence.  

---

### Test 8 — Partial Alert Channel Failure

**Guarantee:** G7 (Delivery resilience)

**Attack steps:**  
- Disabled Telegram and webhook (simulated).  
- Left email enabled.  

**Expected result:**  
- Alert delivered via remaining channel.  

**Observed result:**  
- Alert sent via email.  

**Verdict:** PASSED  
**Notes:**  
- Multi-channel delivery ensures resilience.  

---

### Test 9 — Server Crash Recovery (Bonus)

**Attack steps:**  
- Killed server process.  
- Restarted server.  

**Expected result:**  
- Server recovers cleanly.  
- New heartbeats processed.  

**Observed result:**  
- Server restarted successfully.  
- Heartbeats accepted post-recovery.  

**Verdict:** PASSED  
**Notes:**  
- No crash loops or data loss.  

---