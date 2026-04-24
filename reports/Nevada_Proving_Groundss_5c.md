# DCS Afterburner Report: Nevada_Proving_Groundss_5c

**Source:** `Nevada_Proving_Groundss_5c.miz`  
**Hash:** `sha256:784dc9f66e11ed478b62e5b6070e785a3e6189fd8ea8aa9d98ac39319d5ad148`  
**Theatre:** Nevada  
**Risk:** 84/100 — MODERATE

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 481 |
| Active at start | 90 |
| Late activation | 391 |
| Player slots | 35 |
| Groups (total) | 68 |
| Active groups | 20 |
| Static objects | 41 |
| Triggers | 17 |
| Trigger zones | 37 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

### 🟡 `SCPT_001` — High script line count

**Severity:** warning  
**Confidence:** 100%  

7,854 non-blank lines of mission-specific Lua (frameworks excluded): OpForAC.lua (6,091), Jtac_Zeus.lua (1,008), flight_message.lua (331), PlaygroundMenuNelis2.lua (188), arty_strike.lua (188), NellisGroundSpawns.lua (48). Threshold: warning >5,000, critical >15,000.

**Fix:** Audit script files for dead code, commented-out blocks, or redundant copies of frameworks. Consider stripping/minifying large libraries before packing into the .miz. Remove scripts that are loaded but not used.

