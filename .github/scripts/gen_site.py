import glob
import json
import os
from datetime import datetime, timezone

import markdown

REPO_ROOT = os.getcwd()
WEB_DIR = os.path.join(REPO_ROOT, "web")
REPORTS_DIR = os.path.join(WEB_DIR, "reports")
REPORTS_SRC = os.path.join(REPO_ROOT, "reports")
BENCH_RESULTS_SRC = os.path.join(REPO_ROOT, "bench-results")
RAW_BASE = "https://github.com/IT-Dev-Group-6/goon-drop-point/raw/main"

SKIP_DIRS = {".git", ".github", "pictures", "web", "reports", "Testing"}


def discover_folders():
    entries = sorted(
        e for e in os.listdir(REPO_ROOT)
        if os.path.isdir(os.path.join(REPO_ROOT, e)) and e not in SKIP_DIRS
    )
    return entries

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Rajdhani:wght@400;600;700"
    "&family=Share+Tech+Mono&display=swap"
)

CSS = """
  :root {
    --bg:     #0a0e1a;
    --panel:  #0d1526;
    --border: #1b2d4a;
    --cyan:   #00c8ff;
    --cyan2:  #0088bb;
    --text:   #c8daea;
    --dim:    #5878a0;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    line-height: 1.5;
    min-height: 100vh;
  }
  header {
    padding: 2rem;
    background: var(--panel);
    border-bottom: 1px solid var(--border);
  }
  .hud-label {
    font-family: 'Share Tech Mono', monospace;
    color: var(--dim);
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    margin-bottom: 0.4rem;
  }
  h1 {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  main {
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  .corner-box {
    position: relative;
    padding: 1.5rem;
    border: 1px solid var(--border);
    background: var(--panel);
  }
  .corner-box::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 14px; height: 14px;
    border-top: 2px solid var(--cyan);
    border-left: 2px solid var(--cyan);
  }
  .corner-box::after {
    content: '';
    position: absolute;
    bottom: -1px; right: -1px;
    width: 14px; height: 14px;
    border-bottom: 2px solid var(--cyan);
    border-right: 2px solid var(--cyan);
  }
  .section-header {
    font-family: 'Share Tech Mono', monospace;
    color: var(--cyan);
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    padding-bottom: 0.75rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
  }
  .mission-list { list-style: none; }
  .mission-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--border);
  }
  .mission-item:last-child { border-bottom: none; }
  .mission-name {
    font-family: 'Share Tech Mono', monospace;
    flex: 1;
  }
  .mission-size {
    font-family: 'Share Tech Mono', monospace;
    color: var(--dim);
    font-size: 0.85rem;
    width: 6rem;
    text-align: right;
  }
  .mission-links { display: flex; gap: 0.6rem; }
  .mission-links a {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: var(--cyan);
    text-decoration: none;
    border: 1px solid var(--cyan2);
    padding: 0.1rem 0.5rem;
    letter-spacing: 0.04em;
  }
  .mission-links a:hover { background: rgba(0,200,255,0.08); }
  .empty {
    font-family: 'Share Tech Mono', monospace;
    color: var(--dim);
    font-size: 0.85rem;
  }
  footer {
    text-align: center;
    padding: 2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--dim);
    letter-spacing: 0.1em;
    border-top: 1px solid var(--border);
    margin-top: 1rem;
  }
  /* report page extras */
  .back-link {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--cyan);
    text-decoration: none;
    letter-spacing: 0.1em;
    display: inline-block;
    margin-bottom: 1.5rem;
  }
  .back-link:hover { text-decoration: underline; }
  .report-body h1, .report-body h2, .report-body h3 {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 1.5rem 0 0.5rem;
    color: var(--cyan);
  }
  .report-body h1 { font-size: 1.6rem; }
  .report-body h2 { font-size: 1.2rem; }
  .report-body h3 { font-size: 1rem; color: var(--text); }
  .report-body p { margin-bottom: 0.75rem; }
  .report-body ul, .report-body ol {
    margin: 0.5rem 0 0.75rem 1.5rem;
  }
  .report-body code {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85em;
    background: rgba(0,200,255,0.06);
    padding: 0.1em 0.3em;
    border: 1px solid var(--border);
  }
  .report-body pre {
    background: #060a14;
    border: 1px solid var(--border);
    padding: 1rem;
    overflow-x: auto;
    margin-bottom: 1rem;
  }
  .report-body pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: 0.82rem;
  }
  .report-body table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }
  .report-body th {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    color: var(--cyan);
    border-bottom: 1px solid var(--cyan2);
    padding: 0.4rem 0.6rem;
    text-align: left;
    background: rgba(0,200,255,0.04);
  }
  .report-body td {
    padding: 0.4rem 0.6rem;
    border-bottom: 1px solid var(--border);
  }
"""

INDEX_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT-Dev-Group-6 // Mission Drop Point</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="{fonts}" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <header>
    <div class="hud-label">IT-DEV-GROUP-6 // MISSION DROP POINT</div>
    <h1>Mission Files</h1>
  </header>
  <main>
{sections}
  </main>
  <footer>// GENERATED {generated} //</footer>
</body>
</html>
"""

REPORT_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} // Benchmark Report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="{fonts}" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <header>
    <div class="hud-label">BENCHMARK REPORT</div>
    <h1>{title}</h1>
  </header>
  <main>
    <a class="back-link" href="../index.html">[ &larr; BACK TO INDEX ]</a>
    <div class="corner-box">
      <div class="report-body">{content}</div>
    </div>
  </main>
  <footer>// GENERATED {generated} //</footer>
</body>
</html>
"""


def fmt_size(n):
    if n >= 1_048_576:
        return f"{n / 1_048_576:.1f} MB"
    return f"{n / 1024:.0f} KB"


def run_report(stem):
    md_path = os.path.join(REPORTS_SRC, f"{stem}.md")
    if os.path.exists(md_path):
        with open(md_path) as f:
            return f.read()
    return f"# {stem}\n\nNo benchmark report available yet."


def load_bench_result(stem):
    json_path = os.path.join(BENCH_RESULTS_SRC, f"{stem}.json")
    if not os.path.exists(json_path):
        return None
    with open(json_path) as f:
        return json.load(f)


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


def bench_markdown(stem):
    data = load_bench_result(stem)
    if not data:
        return ""

    bench = data.get("bench") or {}
    cpu = data.get("cpu") or {}
    findings = data.get("findings") or {}
    mission = data.get("mission") or stem
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
        "\n\n## Runtime Bench Result\n\n"
        "Latest matching orchestrator run for this mission.\n\n"
        "| Metric | Value |\n"
        "| --- | --- |\n"
        f"{table}\n"
    )


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    folders = discover_folders()
    missions = {}
    for folder in folders:
        folder_path = os.path.join(REPO_ROOT, folder)
        if not os.path.isdir(folder_path):
            missions[folder] = []
            continue
        files = sorted(glob.glob(os.path.join(folder_path, "*.miz")))
        missions[folder] = [(f, os.path.getsize(f)) for f in files]

    for folder, files in missions.items():
        for miz_path, _ in files:
            stem = os.path.splitext(os.path.basename(miz_path))[0]
            print(f"Reporting {miz_path}...")
            md = run_report(stem) + bench_markdown(stem)
            html_content = markdown.markdown(md, extensions=["fenced_code", "tables"])
            report_page = (
                REPORT_TMPL
                .replace("{title}", stem)
                .replace("{fonts}", FONTS)
                .replace("{css}", CSS)
                .replace("{content}", html_content)
                .replace("{generated}", now)
            )
            with open(os.path.join(REPORTS_DIR, f"{stem}.html"), "w") as f:
                f.write(report_page)

    sections_html = ""
    for folder in folders:
        files = missions.get(folder, [])
        if not files:
            items_html = f'    <p class="empty">// NO MISSIONS</p>'
        else:
            items = []
            for miz_path, size in files:
                stem = os.path.splitext(os.path.basename(miz_path))[0]
                rel = os.path.relpath(miz_path, REPO_ROOT).replace(os.sep, "/")
                dl_url = f"{RAW_BASE}/{rel}"
                rpt_url = f"reports/{stem}.html"
                items.append(
                    f'      <li class="mission-item">'
                    f'<span class="mission-name">{stem}.miz</span>'
                    f'<span class="mission-size">{fmt_size(size)}</span>'
                    f'<span class="mission-links">'
                    f'<a href="{dl_url}">[ DOWNLOAD ]</a>'
                    f'<a href="{rpt_url}">[ REPORT ]</a>'
                    f"</span></li>"
                )
            items_html = "      <ul class=\"mission-list\">\n" + "\n".join(items) + "\n      </ul>"

        sections_html += (
            f'    <section class="corner-box">\n'
            f'      <div class="section-header">// {folder.upper()}</div>\n'
            f"{items_html}\n"
            f"    </section>\n"
        )

    index_html = (
        INDEX_TMPL
        .replace("{fonts}", FONTS)
        .replace("{css}", CSS)
        .replace("{sections}", sections_html)
        .replace("{generated}", now)
    )
    with open(os.path.join(WEB_DIR, "index.html"), "w") as f:
        f.write(index_html)

    print(f"Site generated in {WEB_DIR}/")


if __name__ == "__main__":
    main()
