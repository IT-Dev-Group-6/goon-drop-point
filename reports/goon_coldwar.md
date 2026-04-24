# DCS Afterburner Report: goon_coldwar

**Source:** `goon_coldwar.miz`  
**Hash:** `sha256:23b0da1dd044fac4e319d5533979197b20b182c05e749da5b2628e2cd2c75bb6`  
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

