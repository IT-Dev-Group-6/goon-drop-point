# DCS Afterburner Report: Afganistan2F

**Source:** `Afganistan2F.miz`  
**Hash:** `sha256:d98d5fb84ee6e170ec0fc4f4fd756f5fe3372852dd6dd18f47f4fd73a85374d6`  
**Theatre:** Afghanistan  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 956 |
| Active at start | 145 |
| Late activation | 811 |
| Player slots | 6 |
| Groups (total) | 165 |
| Active groups | 26 |
| Static objects | 102 |
| Triggers | 39 |
| Trigger zones | 78 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

