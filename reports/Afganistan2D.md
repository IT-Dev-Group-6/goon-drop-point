# DCS Afterburner Report: Afganistan2D

**Source:** `Afganistan2D.miz`  
**Hash:** `sha256:d1f2ddeb4825cb1032b5e1aa912145fc89af9bbaa40f7684d919eb4fc3e81857`  
**Theatre:** Afghanistan  
**Risk:** 92/100 — LOW

## Mission Summary

| Metric | Value |
|--------|-------|
| Total units | 956 |
| Active at start | 145 |
| Late activation | 811 |
| Player slots | 6 |
| Groups (total) | 165 |
| Active groups | 26 |
| Static objects | 102 |
| Triggers | 39 |
| Trigger zones | 78 |

## Findings

### 🟡 `PERF_001` — CTLD script detected

**Severity:** warning  
**Confidence:** 100%  

CTLD detected in mission scripts. checkHoverStatus and checkAIStatus poll every 1–2s over all registered transport pilots — a steady CPU cost at scale.

**Fix:** Reduce the number of CTLD-registered transport pilot names, or consider switching to a version of CTLD with event-driven hooks instead of polling.

<!-- bench-runtime-start -->

## Runtime Bench Result

Latest matching orchestrator run for this mission.

| Metric | Value |
| --- | --- |
| Run ID | [`brun_dbcc9d0f5b5c`](https://goon.gsquad.cc/api/v1/bench/runs/brun_dbcc9d0f5b5c) |
| Mission loaded | `Afganistan2D.miz` |
| Started | 2026-04-26T16:13:29.732149+00:00 |
| Duration | 1801s |
| Mission samples | 360 |
| CPU samples | 359 |
| Groups | 159 -> 252 (max 252) |
| Units | 950 -> 1635 (max 1635) |
| CPU | avg 2.9%, max 3.9% |
| Memory | 11414.5 MB -> 3491.4 MB (max 12121.0 MB) |
| Threads max | 45 |
| Runtime findings | 1 |

<!-- bench-runtime-end -->
