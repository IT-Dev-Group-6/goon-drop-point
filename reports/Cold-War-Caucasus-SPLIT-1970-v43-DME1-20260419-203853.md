# DCS Afterburner Report: Cold-War-Caucasus-SPLIT-1970-v43-DME1-20260419-203853

**Source:** `Cold-War-Caucasus-SPLIT-1970-v43-DME1-20260419-203853.miz`  
**Hash:** `sha256:57c92a5f85a56b84d9393b5cb6472fb8e4f2e810a2836febd5a27fa039f57572`  
**Theatre:** Caucasus  
**Risk:** 69/100 — HIGH

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 334 |
| Active at start | 333 |
| Late activation | 1 |
| Player slots | 111 |
| Groups (total) | 155 |
| Active groups | 154 |
| Static objects | 1005 |
| Triggers | 4 |
| Trigger zones | 3010 |

## Findings

### 🔴 `BLOT_002` — Excessive static objects

**Severity:** critical  
**Confidence:** 100%  

1005 static objects (threshold: 800). Statics are always active and are a major FPS cost.

**Fix:** Remove decorative statics or replace dense clusters with scenery objects.

### 🟡 `BLOT_004` — High trigger zone count

**Severity:** warning  
**Confidence:** 100%  

3010 trigger zones (threshold: 90). Zones used in triggers are evaluated every frame.

**Fix:** Remove unused zones or merge overlapping zones.

### 🟡 `BLOT_005` — Very high player slot count

**Severity:** warning  
**Confidence:** 100%  

111 player slots (threshold: 80). Excess slots waste group slots and can confuse server browsers.

**Fix:** Remove unused player slots, especially duplicate airframes at the same base.

