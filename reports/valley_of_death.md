# DCS Afterburner Report: Valley of Death

**Source:** `valley_of_death.miz`  
**Hash:** `sha256:bd9bd25db7cdd9d388698d6e5da3c6666efdf235665c06c4993c23a1bed53883`  
**Theatre:** MarianaIslands  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 79 |
| Active at start | 79 |
| Late activation | 0 |
| Player slots | 17 |
| Groups (total) | 25 |
| Active groups | 25 |
| Static objects | 0 |
| Triggers | 3 |
| Trigger zones | 13 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

