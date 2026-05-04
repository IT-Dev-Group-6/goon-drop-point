#!/usr/bin/env python3
import json
import html
import re
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


def mins_label(elapsed_s):
    if elapsed_s is None:
        return ""
    return f"{round(elapsed_s / 60):.0f}m"


def render_svg(title, labels, series_defs, height=240):
    width = 900
    pad_left, pad_right, pad_top, pad_bottom = 54, 18, 26, 40
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom

    all_values = [value for _, values, _ in series_defs for value in values if value is not None]
    if not all_values:
        return (
            f'<div style="padding:16px;color:#a6adc8;background:#181825;border:1px solid #313244;'
            f'border-radius:6px">No data available for {html.escape(title)}.</div>'
        )

    min_v = min(all_values)
    max_v = max(all_values)
    if min_v == max_v:
        pad = 1 if min_v == 0 else abs(min_v) * 0.1
        min_v -= pad
        max_v += pad
    else:
        pad = (max_v - min_v) * 0.1
        min_v -= pad
        max_v += pad

    def scale_x(idx, count):
        if count <= 1:
            return pad_left
        return pad_left + (idx * plot_w / (count - 1))

    def scale_y(value):
        return pad_top + ((max_v - value) / (max_v - min_v) * plot_h)

    svg = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'preserveAspectRatio="none" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="6" fill="#181825"/>',
        f'<text x="{pad_left}" y="18" fill="#a6adc8" font-size="12" font-family="Fira Code, monospace" '
        f'text-transform="uppercase">{html.escape(title)}</text>',
    ]

    grid_lines = 4
    for i in range(grid_lines + 1):
        y = pad_top + (plot_h * i / grid_lines)
        svg.append(f'<line x1="{pad_left}" y1="{y:.1f}" x2="{width - pad_right}" y2="{y:.1f}" stroke="#313244" stroke-width="1"/>')
        val = max_v - ((max_v - min_v) * i / grid_lines)
        svg.append(
            f'<text x="8" y="{y + 4:.1f}" fill="#6c7086" font-size="10" font-family="Fira Code, monospace">{val:.1f}</text>'
        )

    x_count = max(len(labels), max(len(values) for _, values, _ in series_defs))
    x_ticks = min(10, x_count)
    for i in range(x_ticks + 1):
        idx = round((x_count - 1) * i / x_ticks) if x_count > 1 else 0
        x = scale_x(idx, x_count)
        svg.append(f'<line x1="{x:.1f}" y1="{pad_top}" x2="{x:.1f}" y2="{pad_top + plot_h}" stroke="#313244" stroke-width="1"/>')
        label = labels[idx] if idx < len(labels) else ""
        svg.append(
            f'<text x="{x:.1f}" y="{height - 10}" fill="#6c7086" font-size="10" font-family="Fira Code, monospace" '
            f'text-anchor="middle" transform="rotate(-45 {x:.1f} {height - 10})">{html.escape(label)}</text>'
        )

    legend_x = pad_left + 180
    for name, values, color in series_defs:
        svg.append(
            f'<rect x="{legend_x}" y="10" width="14" height="14" rx="2" fill="none" stroke="{color}" stroke-width="2"/>'
        )
        svg.append(
            f'<text x="{legend_x + 20}" y="22" fill="#a6adc8" font-size="11" font-family="Fira Code, monospace">'
            f'{html.escape(name)}</text>'
        )
        legend_x += 120

    for name, values, color in series_defs:
        points = []
        for idx, value in enumerate(values):
            if value is None:
                continue
            x = scale_x(idx, len(values))
            y = scale_y(value)
            points.append(f"{x:.1f},{y:.1f}")
        if not points:
            continue
        svg.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2" '
            f'points="{" ".join(points)}"/>'
        )

        # Fill area for a stronger dashboard look.
        baseline = pad_top + plot_h
        first_x = points[0].split(",")[0]
        last_x = points[-1].split(",")[0]
        fill_points = [f"{first_x},{baseline:.1f}"] + points + [f"{last_x},{baseline:.1f}"]
        svg.append(
            f'<polygon fill="{color}" fill-opacity="0.14" points="{" ".join(fill_points)}"/>'
        )

    svg.append("</svg>")
    return "\n".join(svg)


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

    bench_rows = data.get("bench_timeseries") or []
    cpu_rows = data.get("cpu_timeseries") or []

    bench_labels = [mins_label(row.get("elapsed_s")) for row in bench_rows]
    cpu_labels = [mins_label(row.get("elapsed_s")) for row in cpu_rows]

    drift_series = [("drift (s)", [row.get("drift_s") for row in bench_rows], "#f38ba8")]
    load_series = [
        ("groups", [row.get("groups") for row in bench_rows], "#89b4fa"),
        ("units", [row.get("units") for row in bench_rows], "#a6e3a1"),
    ]
    cpu_series = [("cpu %", [row.get("cpu_pct") for row in cpu_rows], "#fab387")]
    mem_series = [("mem MB", [row.get("mem_mb") for row in cpu_rows], "#cba6f7")]
    no_cpu_samples = (
        '<div style="padding:16px;color:#a6adc8">No CPU samples captured.</div>'
    )

    charts = "\n".join(
        [
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0 18px;">',
            f'<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;">{render_svg("Scheduler Drift (s)", bench_labels, drift_series)}</div>',
            f'<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;">{render_svg("Active Groups / Units", bench_labels, load_series)}</div>',
            (
                f'<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;">'
                f'{render_svg("CPU %", cpu_labels, cpu_series) if cpu_rows else no_cpu_samples}</div>'
            ),
            (
                f'<div style="background:#181825;border:1px solid #313244;border-radius:6px;padding:12px;">'
                f'{render_svg("Memory (MB)", cpu_labels, mem_series) if cpu_rows else no_cpu_samples}</div>'
            ),
            "</div>",
        ]
    )

    table = "\n".join(f"| {name} | {value} |" for name, value in rows)
    return (
        "## Runtime Bench Result\n\n"
        "Latest matching orchestrator run for this mission.\n\n"
        "| Metric | Value |\n"
        "| --- | --- |\n"
        f"{table}\n\n"
        f"{charts}\n"
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

    if not benches:
        print("No bench results to merge.")
        return 0

    processed = 0
    for stem, data in benches.items():
        report_path = REPORTS_DIR / f"{stem}.md"
        existing = report_path.read_text() if report_path.exists() else ""
        action = "Created" if not existing else "Updated"
        report_path.write_text(merge_markdown(existing, bench_markdown(data)))
        processed += 1
        print(f"{action} {report_path}")

    print(f"Updated {processed} report(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
