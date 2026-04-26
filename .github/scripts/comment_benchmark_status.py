#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BENCH_API_BASE = os.environ.get("BENCH_API_BASE", "https://goon.gsquad.cc/api/v1").strip().rstrip("/")
BENCH_API_KEY = os.environ.get("BENCH_API_KEY", "").strip()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "").strip()
FORCE_STATUS_COMMENT = os.environ.get("FORCE_STATUS_COMMENT", "0").lower() in {"1", "true", "yes"}

QUEUE_ID_RE = re.compile(r"\b(bq_[0-9a-f]+)\b")
RUN_ID_RE = re.compile(r"\b(brun_[0-9a-f]+)\b")


def github_json(method, path, data=None):
    if not GITHUB_TOKEN:
        raise SystemExit("GITHUB_TOKEN is required")
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}{path}"
    body = None
    if data is not None:
        body = json.dumps(data).encode()
    request = Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urlopen(request, timeout=60) as response:
        raw = response.read()
        return json.loads(raw.decode() or "{}")


def bench_json(path):
    if not BENCH_API_KEY:
        raise SystemExit("BENCH_API_KEY is required")
    request = Request(
        f"{BENCH_API_BASE}{path}",
        headers={"X-API-Key": BENCH_API_KEY},
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read()
        return json.loads(raw.decode() or "{}")


def list_open_benchmark_issues():
    query = urlencode({"state": "open", "labels": "benchmark", "per_page": "100"})
    return github_json("GET", f"/issues?{query}")


def list_comments(issue_number):
    query = urlencode({"per_page": "100"})
    return github_json("GET", f"/issues/{issue_number}/comments?{query}")


def comment(issue_number, body):
    return github_json("POST", f"/issues/{issue_number}/comments", {"body": body})


def queue_items_by_id():
    items = bench_json("/bench/queue")
    return {item.get("id"): item for item in items if item.get("id")}


def run_details(run_id):
    try:
        return bench_json(f"/bench/runs/{run_id}")
    except (HTTPError, URLError, TimeoutError):
        return None


def extract_queue_ids(comments):
    ids = []
    seen = set()
    for item in comments:
        for queue_id in QUEUE_ID_RE.findall(item.get("body") or ""):
            if queue_id not in seen:
                ids.append(queue_id)
                seen.add(queue_id)
    return ids


def already_commented_today(comments, marker):
    if FORCE_STATUS_COMMENT:
        return False
    return any(marker in (item.get("body") or "") for item in comments)


def fmt_item(item, details):
    queue_id = item.get("id", "unknown")
    mission = item.get("miz_filename") or "unknown mission"
    status = item.get("status") or "unknown"
    duration = item.get("duration_s")
    line = f"- `{queue_id}` `{mission}`: **{status}**"
    if duration:
        line += f" ({duration}s requested)"

    if item.get("run_id"):
        line += f", run `{item['run_id']}`"

    if status == "done" and details:
        bench = details.get("bench_timeseries") or []
        cpu = details.get("cpu_timeseries") or []
        findings = details.get("findings") or []
        line += f" - mission samples {len(bench)}, CPU samples {len(cpu)}, findings {len(findings)}"
    elif status == "failed" and item.get("error"):
        error = str(item["error"]).replace("\r", " ").replace("\n", " ")
        if len(error) > 220:
            error = error[:217] + "..."
        line += f" - error: `{error}`"
    elif status in {"pending", "running"}:
        line += " - still waiting/running"

    return line


def status_body(queue_ids, queue_by_id):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    marker = f"<!-- benchmark-status:{today} -->"
    lines = [
        marker,
        "## Benchmark Status",
        "",
        "Daily 07:02 Eastern queue check.",
        "",
    ]

    if not queue_ids:
        lines.append("No benchmark queue IDs were found in this issue yet.")
        return "\n".join(lines) + "\n"

    missing = []
    for queue_id in queue_ids:
        item = queue_by_id.get(queue_id)
        if not item:
            missing.append(queue_id)
            continue
        details = run_details(item["run_id"]) if item.get("run_id") else None
        lines.append(fmt_item(item, details))

    if missing:
        lines.extend(["", "Queue IDs not found in orchestrator:"])
        lines.extend(f"- `{queue_id}`" for queue_id in missing)

    lines.append("")
    return "\n".join(lines)


def main():
    if not GITHUB_REPOSITORY:
        raise SystemExit("GITHUB_REPOSITORY is required")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    marker = f"<!-- benchmark-status:{today} -->"
    queue_by_id = queue_items_by_id()
    issues = list_open_benchmark_issues()

    for issue in issues:
        if "pull_request" in issue:
            continue
        number = issue["number"]
        comments = list_comments(number)
        if already_commented_today(comments, marker):
            print(f"Skipping issue #{number}: already commented today")
            continue
        queue_ids = extract_queue_ids(comments)
        body = status_body(queue_ids, queue_by_id)
        comment(number, body)
        print(f"Commented on issue #{number}")


if __name__ == "__main__":
    raise SystemExit(main())
