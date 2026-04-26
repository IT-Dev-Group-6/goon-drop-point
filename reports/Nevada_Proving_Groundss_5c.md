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

<!-- bench-runtime-start -->

## Runtime Bench Result

Latest matching orchestrator run for this mission.

| Metric | Value |
| --- | --- |
| Run ID | [`brun_518e5abf998e`](https://goon.gsquad.cc/api/v1/bench/runs/brun_518e5abf998e) |
| Mission loaded | `Nevada_Proving_Groundss_5c.miz` |
| Started | 2026-04-26T17:22:23.519454+00:00 |
| Duration | 1811s |
| Mission samples | 362 |
| CPU samples | 359 |
| Groups | 57 -> 67 (max 67) |
| Units | 446 -> 566 (max 566) |
| CPU | avg 1.1%, max 1.5% |
| Memory | 3737.4 MB -> 975.2 MB (max 3817.9 MB) |
| Threads max | 41 |
| Runtime findings | 2 |

<!-- bench-runtime-end -->
