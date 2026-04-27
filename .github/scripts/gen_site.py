import glob
import os
from datetime import datetime, timezone

import markdown

REPO_ROOT = os.getcwd()
WEB_DIR = os.path.join(REPO_ROOT, "web")
REPORTS_DIR = os.path.join(WEB_DIR, "reports")
REPORTS_SRC = os.path.join(REPO_ROOT, "reports")
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
    "family=Fira+Code:wght@400;700"
    "&display=swap"
)

CSS = """
  :root {
    --base: #1e1e2e;
    --mantle: #181825;
    --crust: #11111b;
    --surface0: #313244;
    --surface1: #45475a;
    --surface2: #585b70;
    --overlay0: #6c7086;
    --overlay1: #7f849c;
    --text: #cdd6f4;
    --subtext0: #a6adc8;
    --subtext1: #bac2de;
    --blue: #89b4fa;
    --green: #a6e3a1;
    --red: #f38ba8;
    --yellow: #f9e2af;
    --peach: #fab387;
    --mauve: #cba6f7;
    --teal: #94e2d5;
    --sky: #89dceb;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { min-height: 100%; background: var(--crust); }
  body {
    font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--text);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 16px 48px;
    min-height: 100vh;
    background: var(--crust);
    gap: 20px;
  }

  .window {
    width: 100%;
    max-width: 1320px;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0,0,0,.7);
  }
  .titlebar {
    background: var(--mantle);
    padding: 11px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--surface0);
    user-select: none;
  }
  .win-controls { display: flex; gap: 7px; }
  .wc { width: 12px; height: 12px; border-radius: 50%; }
  .wc-close  { background: #f38ba8; }
  .wc-min    { background: #f9e2af; }
  .wc-max    { background: #a6e3a1; }
  .win-title { flex: 1; text-align: center; font-size: 12px; color: var(--overlay0); }

  .panel {
    background: var(--base);
    padding: 20px 24px;
  }
  .subtitle {
    color: var(--overlay1);
    font-size: 12px;
    margin-bottom: 20px;
  }
  h1 {
    font-size: 15px;
    font-weight: 700;
    color: var(--blue);
    margin-bottom: 4px;
  }

  .section-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--overlay1);
    margin: 16px 0 8px;
  }

  .corner-box, .chart-box, .mission-card, .report-shell {
    background: var(--mantle);
    border: 1px solid var(--surface0);
    border-radius: 6px;
  }
  .corner-box { padding: 14px; }
  .mission-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
  .mission-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    cursor: default;
  }
  .mission-item:hover { border-color: var(--blue); }
  .mission-name { color: var(--text); flex: 1; font-weight: 700; }
  .mission-size { color: var(--teal); font-size: 12px; white-space: nowrap; }
  .mission-links { display: flex; gap: 8px; }
  .mission-links a {
    color: var(--blue);
    text-decoration: none;
    border: 1px solid var(--surface1);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
  }
  .mission-links a:hover { border-color: var(--blue); background: rgba(137,180,250,0.08); }
  .empty { color: var(--overlay0); font-size: 12px; padding: 12px 0; }
  .folder-grid { display: flex; flex-direction: column; gap: 14px; }

  .back-link {
    background: none;
    border: 1px solid var(--surface1);
    border-radius: 4px;
    color: var(--subtext0);
    padding: 4px 10px;
    cursor: pointer;
    font-family: inherit;
    font-size: 12px;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 14px;
  }
  .back-link:hover { border-color: var(--blue); color: var(--blue); }

  .report-body h1, .report-body h2, .report-body h3 {
    font-weight: 700;
    color: var(--blue);
    margin: 18px 0 8px;
  }
  .report-body h1 { font-size: 16px; }
  .report-body h2 { font-size: 14px; }
  .report-body h3 { font-size: 13px; color: var(--text); }
  .report-body p { margin-bottom: 10px; }
  .report-body ul, .report-body ol { margin: 0.5rem 0 0.75rem 1.5rem; }
  .report-body a,
  .report-body a:visited {
    color: var(--sky);
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  .report-body a:hover { color: var(--teal); }
  .report-body code {
    font-family: 'Fira Code', monospace;
    font-size: 0.85em;
    background: rgba(137,180,250,0.06);
    padding: 0.1em 0.3em;
    border: 1px solid var(--surface0);
  }
  .report-body pre {
    background: var(--crust);
    border: 1px solid var(--surface0);
    padding: 1rem;
    overflow-x: auto;
    margin-bottom: 1rem;
    border-radius: 6px;
  }
  .report-body pre code { background: none; border: none; padding: 0; font-size: 0.82rem; }
  .report-body table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }
  .report-body th {
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    color: var(--blue);
    border-bottom: 1px solid var(--surface1);
    padding: 0.4rem 0.6rem;
    text-align: left;
    background: rgba(137,180,250,0.04);
  }
  .report-body td {
    padding: 0.4rem 0.6rem;
    border-bottom: 1px solid var(--surface0);
  }
  .report-grid { display: flex; flex-direction: column; gap: 14px; }
  .report-meta { color: var(--overlay1); font-size: 12px; }
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
  <div class="window">
    <div class="titlebar">
      <div class="win-controls">
        <div class="wc wc-close"></div>
        <div class="wc wc-min"></div>
        <div class="wc wc-max"></div>
      </div>
      <div class="win-title">goon-drop-point — mission files</div>
    </div>
    <div class="panel">
      <h1>Mission Files</h1>
      <div class="subtitle">Shared drop point for DCS World .miz mission files used by IT-Dev-Group-6.</div>
      <div class="folder-grid">
{sections}
      </div>
    </div>
  </div>
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
  <div class="window">
    <div class="titlebar">
      <div class="win-controls">
        <div class="wc wc-close"></div>
        <div class="wc wc-min"></div>
        <div class="wc wc-max"></div>
      </div>
      <div class="win-title">goon-drop-point — benchmark report</div>
    </div>
    <div class="panel">
      <a class="back-link" href="../index.html">← back</a>
      <div class="report-shell">
        <div class="report-body">{content}</div>
      </div>
    </div>
  </div>
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
            md = run_report(stem)
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
                    f'      <div class="mission-item mission-card">'
                    f'<span class="mission-name">{stem}.miz</span>'
                    f'<span class="mission-size">{fmt_size(size)}</span>'
                    f'<span class="mission-links">'
                    f'<a href="{dl_url}">download</a>'
                    f'<a href="{rpt_url}">report</a>'
                    f"</span></div>"
                )
            items_html = "      <div class=\"mission-list\">\n" + "\n".join(items) + "\n      </div>"

        sections_html += (
            f'    <section class="corner-box">\n'
            f'      <div class="section-title">{folder.upper()}</div>\n'
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
