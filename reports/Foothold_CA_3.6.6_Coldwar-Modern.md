# DCS Afterburner Report: Foothold_CA_3.6.6_Coldwar-Modern

**Source:** `Foothold_CA_3.6.6_Coldwar-Modern.miz`  
**Hash:** `sha256:0470d3ca54671c268e3ecccd9fd72e8588719d6be23a482c20578c769c16beb1`  
**Theatre:** Caucasus  
**Risk:** 76/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 1072 |
| Active at start | 39 |
| Late activation | 1033 |
| Player slots | 33 |
| Groups (total) | 383 |
| Active groups | 37 |
| Static objects | 171 |
| Triggers | 7 |
| Trigger zones | 787 |

## Findings

### 🟡 `BLOT_004` — High trigger zone count

**Severity:** warning  
**Confidence:** 100%  

787 trigger zones (threshold: 90). Zones used in triggers are evaluated every frame.

**Fix:** Remove unused zones or merge overlapping zones.

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

### 🟡 `SCPT_001` — High script line count

**Severity:** warning  
**Confidence:** 100%  

8,829 non-blank lines of mission-specific Lua (frameworks excluded): MA_Setup_CA.lua (4,775), WelcomeMessage.lua (1,914), Foothold Config.lua (1,044), EWRS.lua (1,009), Zeus.lua (87). Threshold: warning >5,000, critical >15,000.

**Fix:** Audit script files for dead code, commented-out blocks, or redundant copies of frameworks. Consider stripping/minifying large libraries before packing into the .miz. Remove scripts that are loaded but not used.

