# DCS Afterburner Report: South_of_the_Border1A1

**Source:** `South_of_the_Border1A1.miz`  
**Hash:** `sha256:7b9118763688e4fb6afc6da084689ab8a0a01e88680eacfa93d86fc8a27c52e0`  
**Theatre:** Caucasus  
**Risk:** 90/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 239 |
| Active at start | 202 |
| Late activation | 37 |
| Player slots | 48 |
| Groups (total) | 55 |
| Active groups | 45 |
| Static objects | 21 |
| Triggers | 13 |
| Trigger zones | 17 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

### 🔵 `PERF_002` — CSAR script detected

**Severity:** info  
**Confidence:** 100%  

CSAR detected in mission scripts. Timer accumulation (N helis × M wounded groups) can grow on long sessions with many active rescues.

**Fix:** Monitor timer count on long sessions. If issues arise, restart the mission periodically or use a CSAR version that cleans up completed timers.

