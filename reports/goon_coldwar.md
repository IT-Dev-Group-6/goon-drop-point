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

<!-- bench-runtime-start -->

## Runtime Bench Result

Latest matching orchestrator run for this mission.

| Metric | Value |
| --- | --- |
| Run ID | [`brun_c930d6b46d09`](https://goon.gsquad.cc/api/v1/bench/runs/brun_c930d6b46d09) |
| Mission loaded | `goon_coldwar.miz` |
| Started | 2026-04-27T12:43:21.886651+00:00 |
| Duration | 300s |
| Mission samples | 1 |
| CPU samples | 59 |
| Groups | 53 -> 53 (max 53) |
| Units | 232 -> 232 (max 232) |
| CPU | avg 0.0%, max 0.1% |
| Memory | 4074.4 MB -> 816.4 MB (max 4074.4 MB) |
| Threads max | 41 |
| Runtime findings | 3 |

<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0 18px;">
<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;"><svg viewBox="0 0 900 240" width="100%" height="240" preserveAspectRatio="none" role="img" aria-label="Scheduler Drift (s)">
<rect x="0" y="0" width="900" height="240" rx="6" fill="#181825"/>
<text x="54" y="18" fill="#a6adc8" font-size="12" font-family="Fira Code, monospace" text-transform="uppercase">Scheduler Drift (s)</text>
<line x1="54" y1="26.0" x2="882" y2="26.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="30.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">1.0</text>
<line x1="54" y1="69.5" x2="882" y2="69.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="73.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.5</text>
<line x1="54" y1="113.0" x2="882" y2="113.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="117.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.0</text>
<line x1="54" y1="156.5" x2="882" y2="156.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="160.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">-0.5</text>
<line x1="54" y1="200.0" x2="882" y2="200.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="204.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">-1.0</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<rect x="234" y="10" width="14" height="14" rx="2" fill="none" stroke="#f38ba8" stroke-width="2"/>
<text x="254" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">drift (s)</text>
<polyline fill="none" stroke="#f38ba8" stroke-width="2" points="54.0,113.0"/>
<polygon fill="#f38ba8" fill-opacity="0.14" points="54.0,200.0 54.0,113.0 54.0,200.0"/>
</svg></div>
<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;"><svg viewBox="0 0 900 240" width="100%" height="240" preserveAspectRatio="none" role="img" aria-label="Active Groups / Units">
<rect x="0" y="0" width="900" height="240" rx="6" fill="#181825"/>
<text x="54" y="18" fill="#a6adc8" font-size="12" font-family="Fira Code, monospace" text-transform="uppercase">Active Groups / Units</text>
<line x1="54" y1="26.0" x2="882" y2="26.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="30.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">249.9</text>
<line x1="54" y1="69.5" x2="882" y2="69.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="73.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">196.2</text>
<line x1="54" y1="113.0" x2="882" y2="113.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="117.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">142.5</text>
<line x1="54" y1="156.5" x2="882" y2="156.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="160.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">88.8</text>
<line x1="54" y1="200.0" x2="882" y2="200.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="204.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">35.1</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<rect x="234" y="10" width="14" height="14" rx="2" fill="none" stroke="#89b4fa" stroke-width="2"/>
<text x="254" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">groups</text>
<rect x="354" y="10" width="14" height="14" rx="2" fill="none" stroke="#a6e3a1" stroke-width="2"/>
<text x="374" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">units</text>
<polyline fill="none" stroke="#89b4fa" stroke-width="2" points="54.0,185.5"/>
<polygon fill="#89b4fa" fill-opacity="0.14" points="54.0,200.0 54.0,185.5 54.0,200.0"/>
<polyline fill="none" stroke="#a6e3a1" stroke-width="2" points="54.0,40.5"/>
<polygon fill="#a6e3a1" fill-opacity="0.14" points="54.0,200.0 54.0,40.5 54.0,200.0"/>
</svg></div>
<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;"><svg viewBox="0 0 900 240" width="100%" height="240" preserveAspectRatio="none" role="img" aria-label="CPU %">
<rect x="0" y="0" width="900" height="240" rx="6" fill="#181825"/>
<text x="54" y="18" fill="#a6adc8" font-size="12" font-family="Fira Code, monospace" text-transform="uppercase">CPU %</text>
<line x1="54" y1="26.0" x2="882" y2="26.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="30.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.1</text>
<line x1="54" y1="69.5" x2="882" y2="69.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="73.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.1</text>
<line x1="54" y1="113.0" x2="882" y2="113.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="117.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.1</text>
<line x1="54" y1="156.5" x2="882" y2="156.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="160.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">0.0</text>
<line x1="54" y1="200.0" x2="882" y2="200.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="204.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">-0.0</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<line x1="139.7" y1="26" x2="139.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="139.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 139.7 230)">1m</text>
<line x1="225.3" y1="26" x2="225.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="225.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 225.3 230)">1m</text>
<line x1="296.7" y1="26" x2="296.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="296.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 296.7 230)">2m</text>
<line x1="382.3" y1="26" x2="382.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="382.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 382.3 230)">2m</text>
<line x1="468.0" y1="26" x2="468.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="468.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 468.0 230)">3m</text>
<line x1="553.7" y1="26" x2="553.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="553.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 553.7 230)">3m</text>
<line x1="639.3" y1="26" x2="639.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="639.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 639.3 230)">4m</text>
<line x1="710.7" y1="26" x2="710.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="710.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 710.7 230)">4m</text>
<line x1="796.3" y1="26" x2="796.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="796.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 796.3 230)">4m</text>
<line x1="882.0" y1="26" x2="882.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="882.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 882.0 230)">5m</text>
<rect x="234" y="10" width="14" height="14" rx="2" fill="none" stroke="#fab387" stroke-width="2"/>
<text x="254" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">cpu %</text>
<polyline fill="none" stroke="#fab387" stroke-width="2" points="54.0,127.5 68.3,156.5 82.6,156.5 96.8,156.5 111.1,185.5 125.4,127.5 139.7,185.5 153.9,185.5 168.2,127.5 182.5,185.5 196.8,156.5 211.0,185.5 225.3,156.5 239.6,156.5 253.9,127.5 268.1,156.5 282.4,185.5 296.7,185.5 311.0,156.5 325.2,98.5 339.5,127.5 353.8,185.5 368.1,127.5 382.3,98.5 396.6,156.5 410.9,156.5 425.2,156.5 439.4,127.5 453.7,185.5 468.0,185.5 482.3,156.5 496.6,156.5 510.8,156.5 525.1,185.5 539.4,156.5 553.7,127.5 567.9,127.5 582.2,127.5 596.5,40.5 610.8,185.5 625.0,127.5 639.3,98.5 653.6,185.5 667.9,156.5 682.1,185.5 696.4,156.5 710.7,84.0 725.0,156.5 739.2,156.5 753.5,185.5 767.8,156.5 782.1,98.5 796.3,185.5 810.6,84.0 824.9,127.5 839.2,156.5 853.4,156.5 867.7,185.5 882.0,185.5"/>
<polygon fill="#fab387" fill-opacity="0.14" points="54.0,200.0 54.0,127.5 68.3,156.5 82.6,156.5 96.8,156.5 111.1,185.5 125.4,127.5 139.7,185.5 153.9,185.5 168.2,127.5 182.5,185.5 196.8,156.5 211.0,185.5 225.3,156.5 239.6,156.5 253.9,127.5 268.1,156.5 282.4,185.5 296.7,185.5 311.0,156.5 325.2,98.5 339.5,127.5 353.8,185.5 368.1,127.5 382.3,98.5 396.6,156.5 410.9,156.5 425.2,156.5 439.4,127.5 453.7,185.5 468.0,185.5 482.3,156.5 496.6,156.5 510.8,156.5 525.1,185.5 539.4,156.5 553.7,127.5 567.9,127.5 582.2,127.5 596.5,40.5 610.8,185.5 625.0,127.5 639.3,98.5 653.6,185.5 667.9,156.5 682.1,185.5 696.4,156.5 710.7,84.0 725.0,156.5 739.2,156.5 753.5,185.5 767.8,156.5 782.1,98.5 796.3,185.5 810.6,84.0 824.9,127.5 839.2,156.5 853.4,156.5 867.7,185.5 882.0,185.5 882.0,200.0"/>
</svg></div>
<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;"><svg viewBox="0 0 900 240" width="100%" height="240" preserveAspectRatio="none" role="img" aria-label="Memory (MB)">
<rect x="0" y="0" width="900" height="240" rx="6" fill="#181825"/>
<text x="54" y="18" fill="#a6adc8" font-size="12" font-family="Fira Code, monospace" text-transform="uppercase">Memory (MB)</text>
<line x1="54" y1="26.0" x2="882" y2="26.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="30.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">4400.2</text>
<line x1="54" y1="69.5" x2="882" y2="69.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="73.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">3422.8</text>
<line x1="54" y1="113.0" x2="882" y2="113.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="117.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">2445.4</text>
<line x1="54" y1="156.5" x2="882" y2="156.5" stroke="#313244" stroke-width="1"/>
<text x="8" y="160.5" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">1468.0</text>
<line x1="54" y1="200.0" x2="882" y2="200.0" stroke="#313244" stroke-width="1"/>
<text x="8" y="204.0" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">490.6</text>
<line x1="54.0" y1="26" x2="54.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="54.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 54.0 230)">0m</text>
<line x1="139.7" y1="26" x2="139.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="139.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 139.7 230)">1m</text>
<line x1="225.3" y1="26" x2="225.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="225.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 225.3 230)">1m</text>
<line x1="296.7" y1="26" x2="296.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="296.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 296.7 230)">2m</text>
<line x1="382.3" y1="26" x2="382.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="382.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 382.3 230)">2m</text>
<line x1="468.0" y1="26" x2="468.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="468.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 468.0 230)">3m</text>
<line x1="553.7" y1="26" x2="553.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="553.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 553.7 230)">3m</text>
<line x1="639.3" y1="26" x2="639.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="639.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 639.3 230)">4m</text>
<line x1="710.7" y1="26" x2="710.7" y2="200" stroke="#313244" stroke-width="1"/>
<text x="710.7" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 710.7 230)">4m</text>
<line x1="796.3" y1="26" x2="796.3" y2="200" stroke="#313244" stroke-width="1"/>
<text x="796.3" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 796.3 230)">4m</text>
<line x1="882.0" y1="26" x2="882.0" y2="200" stroke="#313244" stroke-width="1"/>
<text x="882.0" y="230" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" text-anchor="middle" transform="rotate(-45 882.0 230)">5m</text>
<rect x="234" y="10" width="14" height="14" rx="2" fill="none" stroke="#cba6f7" stroke-width="2"/>
<text x="254" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">mem MB</text>
<polyline fill="none" stroke="#cba6f7" stroke-width="2" points="54.0,40.5 68.3,40.5 82.6,40.5 96.8,40.5 111.1,40.5 125.4,40.5 139.7,40.5 153.9,40.5 168.2,40.5 182.5,40.5 196.8,40.5 211.0,40.5 225.3,40.5 239.6,40.5 253.9,40.5 268.1,40.5 282.4,40.5 296.7,40.5 311.0,42.1 325.2,50.6 339.5,58.9 353.8,66.7 368.1,74.2 382.3,81.3 396.6,88.1 410.9,94.6 425.2,100.8 439.4,106.7 453.7,111.2 468.0,116.6 482.3,121.7 496.6,126.6 510.8,131.2 525.1,135.7 539.4,139.9 553.7,143.9 567.9,147.7 582.2,151.3 596.5,154.1 610.8,157.4 625.0,160.5 639.3,163.5 653.6,166.4 667.9,168.6 682.1,171.0 696.4,172.9 710.7,174.4 725.0,175.8 739.2,177.6 753.5,179.4 767.8,180.9 782.1,182.3 796.3,183.0 810.6,184.2 824.9,185.5 839.2,185.5 853.4,185.5 867.7,185.5 882.0,185.5"/>
<polygon fill="#cba6f7" fill-opacity="0.14" points="54.0,200.0 54.0,40.5 68.3,40.5 82.6,40.5 96.8,40.5 111.1,40.5 125.4,40.5 139.7,40.5 153.9,40.5 168.2,40.5 182.5,40.5 196.8,40.5 211.0,40.5 225.3,40.5 239.6,40.5 253.9,40.5 268.1,40.5 282.4,40.5 296.7,40.5 311.0,42.1 325.2,50.6 339.5,58.9 353.8,66.7 368.1,74.2 382.3,81.3 396.6,88.1 410.9,94.6 425.2,100.8 439.4,106.7 453.7,111.2 468.0,116.6 482.3,121.7 496.6,126.6 510.8,131.2 525.1,135.7 539.4,139.9 553.7,143.9 567.9,147.7 582.2,151.3 596.5,154.1 610.8,157.4 625.0,160.5 639.3,163.5 653.6,166.4 667.9,168.6 682.1,171.0 696.4,172.9 710.7,174.4 725.0,175.8 739.2,177.6 753.5,179.4 767.8,180.9 782.1,182.3 796.3,183.0 810.6,184.2 824.9,185.5 839.2,185.5 853.4,185.5 867.7,185.5 882.0,185.5 882.0,200.0"/>
</svg></div>
</div>

<!-- bench-runtime-end -->
