#!/usr/bin/env python3
"""Verify factual claims in a review draft before posting.

Deterministic, read-only gate. Exits non-zero on hard mismatches so the
review command can refuse to post. No LLM, no second model, no writes.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

FAIL_STATES = {"FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED", "STALE"}
REPORT_SECTIONS = {"Verified by execution": "verified", "Read only": "readonly"}
BOOKKEEPING = ("Basis:", "Round:", "Verified by execution", "Read only", "<details>")
UNSAFE = (
    "GH_TOKEN",
    "REVIEW_ASSISTANT_GH_TOKEN",
    "write.env",
    "client.conf",
    "BEGIN PRIVATE KEY",
    "sudo ",
)
VERIFIED_ENTRY = re.compile(r"^`([^`]+)`\s+at\s+([0-9a-f]{7,40}):\s*exit 0$")
SHINGLE_WORDS = 8
MAX_ONE_LINER = 200
CI_TIMEOUT = 30
MAX_LOG_BYTES = 8_000_000
GH_FAILURES = (RuntimeError, ValueError, KeyError, TypeError, AttributeError, OSError)


def gh_bin():
    return shutil.which("gh-as-bot") or shutil.which("gh") or "gh"


def run(cmd, cwd=None):
    return subprocess.run(cmd, check=False, cwd=cwd, text=True, capture_output=True)


def gh_json(args):
    p = run([gh_bin()] + args)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip())
    return json.loads(p.stdout)


def fetch(url, limit=MAX_LOG_BYTES):
    with urllib.request.urlopen(url, timeout=CI_TIMEOUT) as r:
        return r.read(limit).decode("utf-8", "replace")


def parse_failing_files(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\n")
    sections = text.split("Test Summary Report")[1:]
    if not sections:
        return None
    files = set()
    for sec in sections:
        files.update(
            re.findall(r"(?m)^\s*([A-Za-z0-9_./-]+\.(?:t|py|js|pm))\s+\(Wstat:", sec)
        )
    return files


class Pull:
    def __init__(self, repo, pr, head):
        self.repo = repo
        self.pr = pr
        self.data = gh_json(
            [
                "pr",
                "view",
                str(pr),
                "-R",
                repo,
                "--json",
                "reviews,reviewDecision,statusCheckRollup,files,headRefOid",
            ]
        )
        self.head = self.data.get("headRefOid") or head
        self.files = {
            f["path"] for f in (self.data.get("files") or []) if f.get("path")
        }
        self.rollup = self.data.get("statusCheckRollup") or []
        self._ci = None

    def checks(self):
        out = []
        for c in self.rollup:
            if c.get("__typename") == "StatusContext":
                out.append(
                    {
                        "name": c.get("context"),
                        "state": c.get("state"),
                        "url": c.get("targetUrl"),
                    }
                )
            elif c.get("__typename") == "CheckRun":
                out.append(
                    {
                        "name": c.get("name"),
                        "state": c.get("conclusion"),
                        "url": c.get("detailsUrl"),
                    }
                )
        return out

    def failing(self):
        return [c for c in self.checks() if c["state"] in FAIL_STATES]

    def circleci_files(self):
        if self._ci is not None:
            return self._ci
        files, sources, errors = set(), [], []
        for c in self.failing():
            url = c.get("url") or ""
            m = re.search(
                r"app\.circleci\.com/workflow/([0-9a-f-]+)/job/([0-9a-f-]+)", url
            )
            if not m:
                continue
            wf, jid = m.group(1), m.group(2)
            try:
                jobs = gh_json(
                    ["api", f"https://circleci.com/api/v2/workflow/{wf}/job"]
                )
                job = next(
                    (j for j in jobs.get("items", []) if j.get("id") == jid), None
                )
                if not job:
                    errors.append(f"{c['name']}: no workflow job for {jid}")
                    continue
                num = job.get("job_number")
                detail = gh_json(
                    [
                        "api",
                        f"https://circleci.com/api/v1.1/project/github/{self.repo}/{num}",
                    ]
                )
                text = ""
                seen = set()
                for step in detail.get("steps", []):
                    for action in step.get("actions", []):
                        u = action.get("output_url")
                        if u and u not in seen:
                            seen.add(u)
                            text += fetch(u)
                parsed = parse_failing_files(text)
                if parsed is None:
                    errors.append(f"{c['name']}: no Test Summary Report in job {num}")
                    continue
                files |= parsed
                sources.append(f"{c['name']} job {num}")
            except GH_FAILURES as e:
                errors.append(f"{c['name']}: {e}")
        self._ci = (files, sources, errors)
        return self._ci


def extract_file_claims(text):
    claims = []
    for para in re.split(r"\n\s*\n", text):
        for m in re.finditer(
            r"(?i)(\d+)\s+(?:UI\s+|unit\s+|integration\s+)?test\s+(?:files|suites)",
            para,
        ):
            paths = set(re.findall(r"\b((?:t|test)/[\w./-]+\.(?:t|py|js|pm))\b", para))
            claims.append(
                {
                    "n": int(m.group(1)),
                    "paths": paths,
                    "para": " ".join(para.split())[:240],
                }
            )
    return claims


def read_text(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def read_json(path):
    text = read_text(path)
    return json.loads(text) if text.strip() else []


def report_block(report):
    """Split the model's report into basis, round, verified, read-only and stray lines."""
    basis, round_text, section = "", "", ""
    verified, readonly, stray = [], [], []
    for raw in report.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Basis:"):
            basis, section = line, ""
        elif line.startswith("Round:"):
            round_text, section = line[len("Round:") :].strip(), ""
        elif line.rstrip(":") in REPORT_SECTIONS:
            section = REPORT_SECTIONS[line.rstrip(":")]
        elif line.startswith("- ") and section:
            (verified if section == "verified" else readonly).append(line[2:].strip())
        else:
            stray.append(line)
    return basis, round_text, verified, readonly, stray


def shingles(text):
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {
        " ".join(words[i : i + SHINGLE_WORDS])
        for i in range(len(words) - SHINGLE_WORDS + 1)
    }


def restatement(body, inline):
    """Return the 8-word shingles the body shares with an inline comment."""
    body_shingles = shingles(body)
    shared = set()
    for c in inline:
        shared |= body_shingles & shingles(c.get("body"))
    return shared


def login(comment):
    return (comment.get("user") or {}).get("login") or ""


def created(comment):
    return comment.get("created_at") or ""


def still_open(threads, bot):
    """Bot root comments whose thread carries no human reply after the bot's last word."""
    replies = {}
    for c in threads:
        if c.get("in_reply_to_id"):
            replies.setdefault(c["in_reply_to_id"], []).append(c)
    open_roots = []
    for root in threads:
        if root.get("in_reply_to_id") or login(root) != bot:
            continue
        thread = sorted([root] + replies.get(root.get("id"), []), key=created)
        last = max((c for c in thread if login(c) == bot), key=created)
        if not any(login(c) != bot and created(c) > created(last) for c in thread):
            open_roots.append(root)
    return open_roots


def bot_login():
    try:
        return gh_json(["api", "user"]).get("login") or ""
    except GH_FAILURES:
        return ""


def last_review_date(pull, bot):
    dates = [
        r.get("submittedAt") or ""
        for r in (pull.data.get("reviews") or [])
        if (r.get("author") or {}).get("login") == bot
    ]
    return max(dates, default="")[:10]


def compose_one_liner(round_text, open_count, review_date):
    clause = ""
    if open_count:
        root = f" from the {review_date} review" if review_date else ""
        clause = f"{open_count} point{'s' if open_count > 1 else ''}{root} still open."
    round_text = round_text.strip().rstrip(".")
    round_text = round_text[:1].upper() + round_text[1:]
    return " ".join(
        part for part in (f"{round_text}." if round_text else "", clause) if part
    )


def compose_body(findings, one_liner, report):
    """Return the posted body: one line, unanchored findings, collapsed verification."""
    parts = [part for part in (one_liner, findings.strip()) if part]
    if not parts:
        return ""
    basis, _, verified, readonly, _ = report_block(report)
    block = ["<details><summary>What was checked</summary>", ""]
    if basis:
        block.append(basis)
    if verified:
        block += ["Verified by execution:"] + [f"- {e}" for e in verified]
    if readonly:
        block += ["Read only:"] + [f"- {e}" for e in readonly]
    block += ["", "</details>"]
    parts.append("\n".join(block))
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--head", default="")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--report", default="")
    ap.add_argument("--threads", default="")
    ap.add_argument("--replies", default="")
    ap.add_argument("--bot", default="")
    ap.add_argument("--inline", default="")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--strict-evidence", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors, warnings = [], []
    text = read_text(args.draft)
    report = read_text(args.report)
    basis, round_text, verified, _, stray = report_block(report)
    inline = read_json(args.inline)
    threads = read_json(args.threads)
    replies = read_json(args.replies)
    scanned = "\n\n".join([text, report] + [(c.get("body") or "") for c in inline])

    if not report:
        errors.append(
            "--report missing: the basis, evidence and read-only lines belong there"
        )
    if not basis:
        errors.append("report has no Basis: line")
    for line in stray:
        errors.append(f"report line outside a section: {line[:80]}")
    for marker in BOOKKEEPING:
        if marker in text:
            errors.append(
                f"draft carries {marker}: the report holds it, the gate composes the body"
            )
    shared = restatement(f"{text}\n{round_text}", inline)
    if shared:
        errors.append(f'body repeats an inline comment: "{min(shared)}"')
    for pat in UNSAFE:
        if pat in scanned:
            errors.append(f"unsafe token/path in draft: {pat}")

    try:
        pull = Pull(args.repo, args.pr, args.head)
    except GH_FAILURES as e:
        print(f"claim-verification: cannot read PR: {e}")
        return 2

    if re.search(
        r"(?i)\ball\s+(?:checks?|CI)\s+(?:are\s+)?(?:green|pass|passing|successful)\b",
        scanned,
    ):
        bad = [c for c in pull.checks() if c["state"] != "SUCCESS"]
        if bad:
            errors.append(
                "'all checks green' but not all SUCCESS: "
                + ", ".join(f"{c['name']}={c['state']}" for c in bad[:8])
            )
    failing = pull.failing()
    if failing:
        if re.search(r"(?i)\b(?:CI|checks?)\b.{0,80}\bin progress\b", scanned):
            errors.append(
                "CI has failing checks but the draft says in progress: "
                + ", ".join(f"{c['name']}={c['state']}" for c in failing[:8])
            )
        missing = [c["name"] for c in failing if c["name"] not in scanned]
        if missing:
            warnings.append(
                "failing checks not named in draft: " + ", ".join(missing[:8])
            )

    for m in re.finditer(r"reviewDecision[`:\s=]+([A-Z_]+)", scanned):
        actual = pull.data.get("reviewDecision") or ""
        if m.group(1) != actual:
            errors.append(
                f"reviewDecision claimed {m.group(1)}, actual {actual or 'none'}"
            )

    actual_files, sources, ci_errors = pull.circleci_files()
    claims = extract_file_claims(scanned)
    if claims:
        if ci_errors:
            errors.extend(ci_errors)
        for c in claims:
            if c["paths"]:
                if c["n"] != len(c["paths"]):
                    errors.append(
                        f"claimed {c['n']} test files but lists {len(c['paths'])}"
                    )
                missing = c["paths"] - actual_files
                if missing:
                    errors.append(
                        "test files not in failing report: "
                        + ", ".join(sorted(missing))
                    )
            elif c["n"] != len(actual_files):
                errors.append(
                    f"claimed {c['n']} test files; report has {len(actual_files)}"
                )
            if not actual_files and not ci_errors:
                errors.append("no failing test report to verify test-file claim")

    cmds = []
    for entry in verified:
        m = VERIFIED_ENTRY.match(entry)
        if not m:
            errors.append(
                f"verified line must read '- `cmd` at <sha>: exit 0': {entry[:80]}"
            )
            continue
        cmds.append(m.group(1))
    if "Verified by execution" in report and not verified:
        warnings.append("Verified by execution has no entry")
    evidence = read_text(args.evidence)
    if args.strict_evidence and cmds and not evidence:
        errors.append("strict evidence: no --evidence file for the verified commands")
    for cmd in cmds:
        key = " ".join(cmd.split())
        if not evidence:
            continue
        if key not in evidence:
            errors.append(f"verified command not in evidence log: {key[:100]}")
        elif not re.search(
            re.escape(key) + r".{0,400}?(?:exit|rc)[=:\s]*0", evidence, re.DOTALL
        ):
            errors.append(
                f"verified command has no exit 0 in evidence log: {key[:100]}"
            )

    for c in inline:
        path, line = c.get("path"), c.get("line")
        if path not in pull.files:
            errors.append(f"inline path not in PR: {path}")
            continue
        p = run(["git", "-C", os.getcwd(), "show", f"{pull.head}:{path}"])
        if p.returncode != 0:
            errors.append(f"inline path missing at head: {path}")
            continue
        n = len(p.stdout.splitlines())
        if not isinstance(line, int) or line < 1 or line > n:
            errors.append(f"inline line {line} outside {path} (1..{n})")

    bot = args.bot or bot_login()
    if threads and not bot:
        errors.append("cannot tell which comments are the bot's: pass --bot")
    open_roots = still_open(threads, bot) if bot else []
    open_ids = {c.get("id") for c in open_roots}
    one_liner = compose_one_liner(
        round_text, len(open_roots), last_review_date(pull, bot)
    )
    if len(one_liner) > MAX_ONE_LINER:
        errors.append(f"one-liner is {len(one_liner)} chars, limit {MAX_ONE_LINER}")

    for r in replies:
        if r.get("id") not in open_ids:
            errors.append(
                f"reply targets thread {r.get('id')}: not an open thread of the bot"
            )
        if not (r.get("body") or "").strip():
            errors.append(f"reply {r.get('id')} has no body")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "body": compose_body(text, one_liner, report),
        "one_liner": one_liner,
        "still_open": sorted(i for i in open_ids if i),
        "failing_test_files": sorted(actual_files),
        "sources": sources,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for e in errors:
            print(f"ERROR {e}")
        for w in warnings:
            print(f"WARN  {w}")
        print(
            f"claim-verification: {'OK' if not errors else 'FAILED'} "
            f"({len(errors)} error(s), {len(warnings)} warning(s))"
        )
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
