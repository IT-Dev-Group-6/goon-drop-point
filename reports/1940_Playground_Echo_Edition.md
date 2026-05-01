# DCS Afterburner Report: 1940_Playground_Echo_Edition

**Source:** `1940_Playground_Echo_Edition.miz`  
**Hash:** `sha256:2586433450b421bf6d16b474d8460a232b803b6dfd995508447d14eec17df73b`  
**Theatre:** Normandy  
**Risk:** 77/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 1307 |
| Active at start | 846 |
| Late activation | 461 |
| Player slots | 1 |
| Groups (total) | 132 |
| Active groups | 65 |
| Static objects | 5 |
| Triggers | 19 |
| Trigger zones | 36 |

## Findings

### 🔴 `BLOT_001` — Excessive active units

**Severity:** critical  
**Confidence:** 100%  

846 units active at mission start (threshold: 600). Expect severe FPS impact on entry-level servers.

**Fix:** Move non-essential groups to late activation or delete them.

### 🟡 `BLOT_008` — Very high total unit count

**Severity:** warning  
**Confidence:** 100%  

1307 total units in mission (threshold: 1200). Even late-activated units consume memory.

**Fix:** Audit late-activation groups and remove units not used by the mission flow.

