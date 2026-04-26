#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import re
import tempfile
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

API_BASE = os.environ.get("BENCH_API_BASE", "https://goon.gsquad.cc/api/v1").strip().rstrip("/")
API_KEY = os.environ.get("BENCH_API_KEY", "").strip()
HOST_ID = os.environ.get("BENCH_HOST_ID", "host_1ad3930ed744").strip()
INSTANCE_ID = os.environ.get("BENCH_INSTANCE_ID", "DCS-TexasBBQ").strip()
DURATION_S = os.environ.get("BENCH_DURATION_S", "1800").strip()
RUN_NOW = os.environ.get("BENCH_RUN_NOW", "1").lower() not in {"0", "false", "no"}
SUMMARY_PATH = os.environ.get("BENCH_QUEUE_SUMMARY", "bench-queue-summary.md")

MIZ_REF_RE = re.compile(r"(?P<ref>(?:https?://[^\s)>\]\"']+|[\w./@%+ -]+?\.miz))", re.IGNORECASE)


def clean_ref(ref):
    return unquote(ref.strip().strip("`\"'<>").rstrip(".,;)"))


def plausible_ref(ref):
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https"}:
        return True

    name = os.path.basename(ref)
    if name.lower() == ".miz" or not Path(name).stem.strip():
        return False

    # Avoid matching prose like "Queue one or more .miz" from issue template text.
    if " " in ref and "/" not in ref and "\\" not in ref:
        return False

    return True


def refs_from_text(text):
    refs = []
    seen = set()
    for match in MIZ_REF_RE.finditer(text or ""):
        ref = clean_ref(match.group("ref"))
        if ref and ref.lower().endswith(".miz") and plausible_ref(ref) and ref not in seen:
            refs.append(ref)
            seen.add(ref)
    return refs


def refs_from_event(path):
    with open(path) as f:
        event = json.load(f)
    issue = event.get("issue") or {}
    return refs_from_text("\n".join([issue.get("title") or "", issue.get("body") or ""]))


def refs_from_file(path):
    refs = []
    with open(path) as f:
        for line in f:
            ref = clean_ref(line)
            if ref:
                refs.append(ref)
    return refs


def download(url, tmpdir):
    parsed = urlparse(url)
    name = os.path.basename(parsed.path) or "mission.miz"
    target = Path(tmpdir) / name
    with urlopen(url, timeout=120) as response:
        target.write_bytes(response.read())
    return target


def resolve_ref(ref, tmpdir):
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https"}:
        return download(ref, tmpdir)

    path = Path(ref)
    if path.exists():
        return path

    raise FileNotFoundError(f"Mission file not found: {ref}")


def encode_multipart(fields, files):
    boundary = f"----goon-drop-point-{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")

    for name, path in files.items():
        filename = path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
        body.extend(path.read_bytes())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def request_json(method, url, data=None, content_type=None):
    headers = {"X-API-Key": API_KEY}
    if content_type:
        headers["Content-Type"] = content_type
    request = Request(url, data=data, method=method, headers=headers)
    with urlopen(request, timeout=120) as response:
        raw = response.read()
        return json.loads(raw.decode() or "{}")


def queue_file(path):
    body, content_type = encode_multipart(
        {
            "host_id": HOST_ID,
            "instance_id": INSTANCE_ID,
            "duration_s": DURATION_S,
        },
        {"miz": path},
    )
    item = request_json("POST", f"{API_BASE}/bench/queue", body, content_type)
    run_result = None
    run_error = None

    if RUN_NOW and item.get("id"):
        try:
            run_result = request_json("POST", f"{API_BASE}/bench/queue/{item['id']}/run")
        except HTTPError as exc:
            run_error = f"HTTP {exc.code}: {exc.read().decode(errors='replace')}"
        except (URLError, TimeoutError) as exc:
            run_error = str(exc)

    return item, run_result, run_error


def write_summary(results, errors):
    lines = ["## Benchmark Queue Request", ""]
    if results:
        lines.extend(["Queued mission file(s):", ""])
        for result in results:
            item = result["item"]
            lines.append(
                f"- `{result['source']}` -> queue `{item.get('id', 'unknown')}` "
                f"({item.get('status', 'unknown')})"
            )
            if result.get("run_result"):
                lines.append(f"  - run request accepted: `{result['run_result'].get('id', item.get('id'))}`")
            if result.get("run_error"):
                lines.append(f"  - run request not started immediately: {result['run_error']}")
        lines.append("")
    if errors:
        lines.extend(["Errors:", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")
    if not results and not errors:
        lines.append("No `.miz` references were found.")

    Path(SUMMARY_PATH).write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-event")
    parser.add_argument("--files-from")
    parser.add_argument("refs", nargs="*")
    args = parser.parse_args()

    if not API_KEY:
        raise SystemExit("BENCH_API_KEY is required")

    refs = []
    if args.issue_event:
        refs.extend(refs_from_event(args.issue_event))
    if args.files_from:
        refs.extend(refs_from_file(args.files_from))
    refs.extend(args.refs)

    deduped_refs = []
    seen = set()
    for ref in refs:
        ref = clean_ref(ref)
        if ref and ref not in seen:
            deduped_refs.append(ref)
            seen.add(ref)

    results = []
    errors = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for ref in deduped_refs:
            try:
                path = resolve_ref(ref, tmpdir)
                item, run_result, run_error = queue_file(path)
                results.append(
                    {
                        "source": ref,
                        "item": item,
                        "run_result": run_result,
                        "run_error": run_error,
                    }
                )
            except (FileNotFoundError, HTTPError, URLError, TimeoutError) as exc:
                errors.append(f"`{ref}`: {exc}")

    write_summary(results, errors)
    print(Path(SUMMARY_PATH).read_text())
    return 1 if errors or not results else 0


if __name__ == "__main__":
    raise SystemExit(main())
