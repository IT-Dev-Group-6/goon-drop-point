# DCS Afterburner Report: Marianas_Turkey_Shoot

**Source:** `Marianas_Turkey_Shoot.miz`  
**Hash:** `sha256:aa15193885251217dd1558ca9ed94ccb9287a1d2b58ec30656284195f07608f4`  
**Theatre:** MarianaIslands  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 39 |
| Active at start | 34 |
| Late activation | 5 |
| Player slots | 2 |
| Groups (total) | 18 |
| Active groups | 14 |
| Static objects | 6 |
| Triggers | 33 |
| Trigger zones | 6 |

## Findings

### 🟡 `SCPT_001` — High script line count

**Severity:** warning  
**Confidence:** 100%  

6,038 non-blank lines of mission-specific Lua (frameworks excluded): RvB_Mariana_dyn.lua (4,932), EasyStatsPlus.lua (1,106). Threshold: warning >5,000, critical >15,000.

**Fix:** Audit script files for dead code, commented-out blocks, or redundant copies of frameworks. Consider stripping/minifying large libraries before packing into the .miz. Remove scripts that are loaded but not used.

