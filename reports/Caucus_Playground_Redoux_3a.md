# DCS Afterburner Report: Caucus_Playground_Redoux_3a

**Source:** `Caucus_Playground_Redoux_3a.miz`  
**Hash:** `sha256:c415c96f6214283211f05cb40673fd4c1ed402076e4111057c15efccf09c0501`  
**Theatre:** Caucasus  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 605 |
| Active at start | 219 |
| Late activation | 386 |
| Player slots | 1 |
| Groups (total) | 99 |
| Active groups | 27 |
| Static objects | 31 |
| Triggers | 20 |
| Trigger zones | 34 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

