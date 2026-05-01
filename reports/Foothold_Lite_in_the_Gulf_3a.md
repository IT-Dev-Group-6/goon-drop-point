# DCS Afterburner Report: Foothold_Lite_in_the_Gulf_3a

**Source:** `Foothold_Lite_in_the_Gulf_3a.miz`  
**Hash:** `sha256:c8ac95d964c75da58fc7067c072f5a9f96ada59c95a75298292356034cd324a9`  
**Theatre:** PersianGulf  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 1009 |
| Active at start | 61 |
| Late activation | 948 |
| Player slots | 0 |
| Groups (total) | 148 |
| Active groups | 22 |
| Static objects | 23 |
| Triggers | 157 |
| Trigger zones | 51 |

## Findings

### 🟡 `BLOT_003` — High trigger count

**Severity:** warning  
**Confidence:** 100%  

157 triggers (threshold: 150). Each trigger is evaluated every frame until it fires.

**Fix:** Consolidate triggers or move logic to a Lua script using event handlers.

