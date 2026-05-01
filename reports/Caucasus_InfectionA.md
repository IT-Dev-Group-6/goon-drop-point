# DCS Afterburner Report: Caucasus_InfectionA

**Source:** `Caucasus_InfectionA.miz`  
**Hash:** `sha256:696ce644a58a1277f19ef22bac53a1d011bb2ddd6912230a8545318f1b49ff11`  
**Theatre:** Caucasus  
**Risk:** 90/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 299 |
| Active at start | 299 |
| Late activation | 0 |
| Player slots | 79 |
| Groups (total) | 299 |
| Active groups | 299 |
| Static objects | 0 |
| Triggers | 6 |
| Trigger zones | 0 |

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

