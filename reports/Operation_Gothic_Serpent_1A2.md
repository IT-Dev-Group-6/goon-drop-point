# DCS Afterburner Report: Operation_Gothic_Serpent_1A2

**Source:** `Operation_Gothic_Serpent_1A2.miz`  
**Hash:** `sha256:3070e742a7ea65c932550e0de4e515c3742e2f3c578645baa9dfc2c575a0aef4`  
**Theatre:** PersianGulf  
**Risk:** 90/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 269 |
| Active at start | 269 |
| Late activation | 0 |
| Player slots | 36 |
| Groups (total) | 62 |
| Active groups | 62 |
| Static objects | 19 |
| Triggers | 10 |
| Trigger zones | 5 |

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

