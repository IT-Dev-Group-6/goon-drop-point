#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path
from statistics import mean

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "reports"
BENCH_RESULTS_DIR = REPO_ROOT / "bench-results"
START_MARKER = "<!-- bench-runtime-start -->"
END_MARKER = "<!-- bench-runtime-end -->"


def load_bench_results():
    results = {}
    if not BENCH_RESULTS_DIR.exists():
        return results
    for path in sorted(BENCH_RESULTS_DIR.glob("*.json")):
        with path.open() as f:
            results[path.stem] = json.load(f)
    return results


def repo_miz_by_stem():
    mapping = {}
    skip_parts = {".git", ".github", "pictures", "web"}
    for path in REPO_ROOT.rglob("*.miz"):
        if any(part in skip_parts for part in path.parts):
            continue
        mapping.setdefault(path.stem, path)
    return mapping


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


def fmt_num(value, suffix="", digits=1):
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}{suffix}"
    return f"{value}{suffix}"


def fmt_range(start, end, suffix="", digits=1):
    if start is None and end is None:
        return "n/a"
    return f"{fmt_num(start, suffix, digits)} -> {fmt_num(end, suffix, digits)}"


def bench_markdown(data):
    bench = data.get("bench") or {}
    cpu = data.get("cpu") or {}
    findings = data.get("findings") or {}
    mission = data.get("mission_stem") or data.get("mission") or "n/a"
    source_url = data.get("source_url") or ""
    run_id = data.get("run_id") or "n/a"

    rows = [
        ("Run ID", f"[`{run_id}`]({source_url})" if source_url else f"`{run_id}`"),
        ("Mission loaded", f"`{mission}.miz`" if not mission.endswith(".miz") else f"`{mission}`"),
        ("Started", data.get("started_at") or data.get("created_at") or "n/a"),
        ("Duration", fmt_num(data.get("duration_s"), "s", 0)),
        ("Mission samples", fmt_num(bench.get("samples"), "", 0)),
        ("CPU samples", fmt_num(cpu.get("samples"), "", 0)),
        (
            "Groups",
            f"{fmt_range(bench.get('groups_start'), bench.get('groups_end'), '', 0)}"
            f" (max {fmt_num(bench.get('groups_max'), '', 0)})",
        ),
        (
            "Units",
            f"{fmt_range(bench.get('units_start'), bench.get('units_end'), '', 0)}"
            f" (max {fmt_num(bench.get('units_max'), '', 0)})",
        ),
        (
            "CPU",
            f"avg {fmt_num(cpu.get('cpu_avg_pct'), '%')}, max {fmt_num(cpu.get('cpu_max_pct'), '%')}",
        ),
        (
            "Memory",
            f"{fmt_range(cpu.get('mem_start_mb'), cpu.get('mem_end_mb'), ' MB')}"
            f" (max {fmt_num(cpu.get('mem_max_mb'), ' MB')})",
        ),
        ("Threads max", fmt_num(cpu.get("threads_max"), "", 0)),
        ("Runtime findings", fmt_num(findings.get("count"), "", 0)),
    ]

    table = "\n".join(f"| {name} | {value} |" for name, value in rows)
    return (
        "## Runtime Bench Result\n\n"
        "Latest matching orchestrator run for this mission.\n\n"
        "| Metric | Value |\n"
        "| --- | --- |\n"
        f"{table}\n"
    )


def merge_markdown(existing, bench_section):
    replacement = (
        f"{START_MARKER}\n\n"
        f"{bench_section.rstrip()}\n\n"
        f"{END_MARKER}"
    )
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.S,
    )
    if pattern.search(existing):
        return pattern.sub(replacement, existing).rstrip() + "\n"

    base = existing.rstrip()
    if base:
        base += "\n\n"
    return f"{base}{replacement}\n"


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    benches = load_bench_results()
    miz_by_stem = repo_miz_by_stem()

    if not benches:
        print("No bench results to merge.")
        return 0

    processed = 0
    for stem, data in benches.items():
        miz_path = miz_by_stem.get(stem)
        if not miz_path:
            print(f"Skipping {stem}: no matching .miz in repo")
            continue

        report_path = REPORTS_DIR / f"{stem}.md"
        with report_path.open("w") as out:
            subprocess.run(
                ["afterburner", "report", str(miz_path), "--format", "md"],
                check=True,
                stdout=out,
                text=True,
            )

        existing = report_path.read_text()
        report_path.write_text(merge_markdown(existing, bench_markdown(data)))
        processed += 1
        print(f"Updated {report_path}")

    print(f"Updated {processed} report(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
