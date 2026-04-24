# DCS Afterburner Report: GTFreeFlyers_Marianas_Mayhem_v1.1

**Source:** `GTFreeFlyers_Marianas_Mayhem_v1.1.miz`  
**Hash:** `sha256:591c6c51e7bad4a5bd84a9a974a55a15e714fc3f82df114ea26ae7c9d3ce1f98`  
**Theatre:** MarianaIslands  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 626 |
| Active at start | 66 |
| Late activation | 560 |
| Player slots | 47 |
| Groups (total) | 251 |
| Active groups | 52 |
| Static objects | 133 |
| Triggers | 238 |
| Trigger zones | 59 |

## Findings

### 🟡 `BLOT_003` — High trigger count

**Severity:** warning  
**Confidence:** 100%  

238 triggers (threshold: 150). Each trigger is evaluated every frame until it fires.

**Fix:** Consolidate triggers or move logic to a Lua script using event handlers.

