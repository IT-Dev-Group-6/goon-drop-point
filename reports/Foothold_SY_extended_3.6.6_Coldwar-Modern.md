# DCS Afterburner Report: Foothold_SY_extended_3.6.6_Coldwar-Modern

**Source:** `Foothold_SY_extended_3.6.6_Coldwar-Modern.miz`  
**Hash:** `sha256:bbe5de6747a174ad7f9a185c067e03b6a424b3492a897d775bcba917996ebcb5`  
**Theatre:** Syria  
**Risk:** 76/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 1189 |
| Active at start | 88 |
| Late activation | 1101 |
| Player slots | 61 |
| Groups (total) | 424 |
| Active groups | 67 |
| Static objects | 131 |
| Triggers | 6 |
| Trigger zones | 1174 |

## Findings

### 🟡 `BLOT_004` — High trigger zone count

**Severity:** warning  
**Confidence:** 100%  

1174 trigger zones (threshold: 90). Zones used in triggers are evaluated every frame.

**Fix:** Remove unused zones or merge overlapping zones.

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

### 🟡 `SCPT_001` — High script line count

**Severity:** warning  
**Confidence:** 100%  

9,885 non-blank lines of mission-specific Lua (frameworks excluded): footholdSyriaSetup.lua (5,831), WelcomeMessage.lua (1,914), Foothold Config.lua (1,044), EWRS.lua (1,009), Zeus.lua (87). Threshold: warning >5,000, critical >15,000.

**Fix:** Audit script files for dead code, commented-out blocks, or redundant copies of frameworks. Consider stripping/minifying large libraries before packing into the .miz. Remove scripts that are loaded but not used.

