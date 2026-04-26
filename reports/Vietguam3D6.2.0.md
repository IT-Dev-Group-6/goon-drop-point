# DCS Afterburner Report: Vietguam3D6.2.0

**Source:** `Vietguam3D6.2.0.miz`  
**Hash:** `sha256:3c2e9eb70ac1a0399dbe56ef5e3b5e74f7ffc34a85c8d785b89909de9d9b2e9f`  
**Theatre:** MarianaIslands  
**Risk:** 66/100 — HIGH

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 1635 |
| Active at start | 452 |
| Late activation | 1183 |
| Player slots | 70 |
| Groups (total) | 262 |
| Active groups | 142 |
| Static objects | 107 |
| Triggers | 72 |
| Trigger zones | 256 |

## Findings

### 🟡 `BLOT_001` — High active unit count

**Severity:** warning  
**Confidence:** 100%  

452 units active at mission start (threshold: 350). May cause performance issues on lower-end servers.

**Fix:** Consider late-activating groups that spawn later in the mission.

### 🟡 `BLOT_008` — Very high total unit count

**Severity:** warning  
**Confidence:** 100%  

1635 total units in mission (threshold: 1200). Even late-activated units consume memory.

**Fix:** Audit late-activation groups and remove units not used by the mission flow.

### 🟡 `BLOT_004` — High trigger zone count

**Severity:** warning  
**Confidence:** 100%  

256 trigger zones (threshold: 90). Zones used in triggers are evaluated every frame.

**Fix:** Remove unused zones or merge overlapping zones.

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

### 🔵 `PERF_002` — CSAR script detected

**Severity:** info  
**Confidence:** 100%  

CSAR detected in mission scripts. Timer accumulation (N helis × M wounded groups) can grow on long sessions with many active rescues.

**Fix:** Monitor timer count on long sessions. If issues arise, restart the mission periodically or use a CSAR version that cleans up completed timers.

<!-- bench-runtime-start -->

## Runtime Bench Result

Latest matching orchestrator run for this mission.

| Metric | Value |
| --- | --- |
| Run ID | [`brun_0451253c2814`](https://goon.gsquad.cc/api/v1/bench/runs/brun_0451253c2814) |
| Mission loaded | `Vietguam3D6.2.0.miz` |
| Started | 2026-04-26T14:13:58.009910+00:00 |
| Duration | 311s |
| Mission samples | 62 |
| CPU samples | 59 |
| Groups | 192 -> 201 (max 201) |
| Units | 1565 -> 1626 (max 1626) |
| CPU | avg 3.6%, max 6.8% |
| Memory | 4950.0 MB -> 5253.3 MB (max 5661.2 MB) |
| Threads max | 45 |
| Runtime findings | 5 |

<!-- bench-runtime-end -->
