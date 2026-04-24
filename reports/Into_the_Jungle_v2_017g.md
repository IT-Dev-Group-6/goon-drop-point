# DCS Afterburner Report: Into The Jungle v2

**Source:** `Into_the_Jungle_v2_017g.miz`  
**Hash:** `sha256:2d2fb34be391a5802d3a8b55a2e53c0b435bfa812c0bd80a8238e8a8930cdab5`  
**Theatre:** MarianaIslands  
**Risk:** 69/100 — HIGH

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 593 |
| Active at start | 315 |
| Late activation | 278 |
| Player slots | 91 |
| Groups (total) | 246 |
| Active groups | 186 |
| Static objects | 2276 |
| Triggers | 121 |
| Trigger zones | 225 |

## Findings

### 🔴 `BLOT_002` — Excessive static objects

**Severity:** critical  
**Confidence:** 100%  

2276 static objects (threshold: 800). Statics are always active and are a major FPS cost.

**Fix:** Remove decorative statics or replace dense clusters with scenery objects.

### 🟡 `BLOT_004` — High trigger zone count

**Severity:** warning  
**Confidence:** 100%  

225 trigger zones (threshold: 90). Zones used in triggers are evaluated every frame.

**Fix:** Remove unused zones or merge overlapping zones.

### 🟡 `BLOT_005` — Very high player slot count

**Severity:** warning  
**Confidence:** 100%  

91 player slots (threshold: 80). Excess slots waste group slots and can confuse server browsers.

**Fix:** Remove unused player slots, especially duplicate airframes at the same base.

