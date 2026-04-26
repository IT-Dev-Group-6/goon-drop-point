#!/usr/bin/env python3
import json
import os
import re
from statistics import mean
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

API_BASE = os.environ.get("BENCH_API_BASE", "https://goon.gsquad.cc/api/v1").rstrip("/")
LIMIT = int(os.environ.get("BENCH_LIMIT", "200"))
OUT_DIR = os.environ.get("BENCH_RESULTS_DIR", "bench-results")
BENCH_SUFFIX_RE = re.compile(r"__bench_bq_[0-9a-f]+$")


def get_json(url):
    with urlopen(url, timeout=30) as response:
        return json.load(response)


def mission_stem(mission):
    name = os.path.basename(mission or "")
    if name.lower().endswith(".miz"):
        name = name[:-4]
    return BENCH_SUFFIX_RE.sub("", name)


def repo_mission_stems():
    stems = set()
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", ".github", "pictures", "web"}]
        for filename in files:
            if filename.lower().endswith(".miz"):
                stems.add(os.path.splitext(filename)[0])
    return stems


def values(rows, key):
    return [row[key] for row in rows if row.get(key) is not None]


def first_value(rows, key):
    vals = values(rows, key)
    return vals[0] if vals else None


def last_value(rows, key):
    vals = values(rows, key)
    return vals[-1] if vals else None


def max_value(rows, key):
    vals = values(rows, key)
    return max(vals) if vals else None


def avg_value(rows, key):
    vals = values(rows, key)
    return round(mean(vals), 2) if vals else None


def summarize(run):
    bench = run.get("bench_timeseries") or []
    cpu = run.get("cpu_timeseries") or []
    findings = run.get("findings") or []
    stem = mission_stem(run.get("mission"))

    return {
        "schema_version": 1,
        "run_id": run.get("id"),
        "source_url": f"{API_BASE}/bench/runs/{run.get('id')}",
        "mission": run.get("mission"),
        "mission_stem": stem,
        "host_id": run.get("host_id"),
        "started_at": run.get("started_at"),
        "ended_at": run.get("ended_at"),
        "created_at": run.get("created_at"),
        "duration_s": run.get("duration_s"),
        "bench_timeseries": bench,
        "cpu_timeseries": cpu,
        "bench": {
            "samples": len(bench),
            "elapsed_start_s": first_value(bench, "elapsed_s"),
            "elapsed_end_s": last_value(bench, "elapsed_s"),
            "drift_avg_s": avg_value(bench, "drift_s"),
            "drift_max_s": max_value(bench, "drift_s"),
            "groups_start": first_value(bench, "groups"),
            "groups_end": last_value(bench, "groups"),
            "groups_max": max_value(bench, "groups"),
            "units_start": first_value(bench, "units"),
            "units_end": last_value(bench, "units"),
            "units_max": max_value(bench, "units"),
        },
        "cpu": {
            "samples": len(cpu),
            "elapsed_start_s": first_value(cpu, "elapsed_s"),
            "elapsed_end_s": last_value(cpu, "elapsed_s"),
            "cpu_avg_pct": avg_value(cpu, "cpu_pct"),
            "cpu_max_pct": max_value(cpu, "cpu_pct"),
            "mem_start_mb": first_value(cpu, "mem_mb"),
            "mem_end_mb": last_value(cpu, "mem_mb"),
            "mem_max_mb": max_value(cpu, "mem_mb"),
            "threads_max": max_value(cpu, "threads"),
        },
        "findings": {
            "count": len(findings),
            "items": findings[:20],
        },
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    target_stems = repo_mission_stems()

    try:
        runs = get_json(f"{API_BASE}/bench/runs?limit={LIMIT}")
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"Unable to fetch bench runs: {exc}")
        return 0

    latest_by_stem = {}
    for item in runs:
        stem = mission_stem(item.get("mission"))
        if not stem or stem not in target_stems or stem in latest_by_stem:
            continue
        run_id = item.get("id")
        if not run_id:
            continue
        try:
            latest_by_stem[stem] = summarize(get_json(f"{API_BASE}/bench/runs/{run_id}"))
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"Skipping {run_id}: {exc}")

    for stem, summary in sorted(latest_by_stem.items()):
        path = os.path.join(OUT_DIR, f"{stem}.json")
        with open(path, "w") as f:
            json.dump(summary, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"Wrote {path}")

    for filename in os.listdir(OUT_DIR):
        if not filename.endswith(".json"):
            continue
        stem = os.path.splitext(filename)[0]
        if stem not in target_stems:
            path = os.path.join(OUT_DIR, filename)
            os.remove(path)
            print(f"Removed stale {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
