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


def verified_section(text):
    m = re.search(
        r"(?is)(?:\*\*|#+\s*)Verified by execution.*?(?=\n(?:\*\*|#+\s*)|\Z)", text
    )
    return m.group(0) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--head", default="")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--inline", default="")
    ap.add_argument("--evidence", default="")
    ap.add_argument("--strict-evidence", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors, warnings = [], []
    with open(args.draft, encoding="utf-8") as f:
        text = f.read()
    inline = []
    if args.inline and os.path.exists(args.inline):
        with open(args.inline, encoding="utf-8") as f:
            inline = json.load(f)
        for c in inline:
            text += "\n\n" + (c.get("body") or "")

    if not re.search(r"(?m)^Basis:", text):
        errors.append("missing Basis: line")
    for pat in (
        "GH_TOKEN",
        "REVIEW_ASSISTANT_GH_TOKEN",
        "write.env",
        "client.conf",
        "BEGIN PRIVATE KEY",
        "sudo ",
    ):
        if pat in text:
            errors.append(f"unsafe token/path in draft: {pat}")

    try:
        pull = Pull(args.repo, args.pr, args.head)
    except GH_FAILURES as e:
        print(f"claim-verification: cannot read PR: {e}")
        return 2

    if re.search(
        r"(?i)\ball\s+(?:checks?|CI)\s+(?:are\s+)?(?:green|pass|passing|successful)\b",
        text,
    ):
        bad = [c for c in pull.checks() if c["state"] != "SUCCESS"]
        if bad:
            errors.append(
                "'all checks green' but not all SUCCESS: "
                + ", ".join(f"{c['name']}={c['state']}" for c in bad[:8])
            )
    failing = pull.failing()
    if failing:
        if re.search(r"(?i)\b(?:CI|checks?)\b.{0,80}\bin progress\b", text):
            errors.append(
                "CI has failing checks but the draft says in progress: "
                + ", ".join(f"{c['name']}={c['state']}" for c in failing[:8])
            )
        missing = [c["name"] for c in failing if c["name"] not in text]
        if missing:
            warnings.append(
                "failing checks not named in draft: " + ", ".join(missing[:8])
            )

    for m in re.finditer(r"reviewDecision[`:\s=]+([A-Z_]+)", text):
        actual = pull.data.get("reviewDecision") or ""
        if m.group(1) != actual:
            errors.append(
                f"reviewDecision claimed {m.group(1)}, actual {actual or 'none'}"
            )

    actual_files, sources, ci_errors = pull.circleci_files()
    claims = extract_file_claims(text)
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

    sec = verified_section(text)
    cmds = re.findall(r"`([^`]*(?:make|prove|perl|python|tools/|gh |git )[^`]*)`", sec)
    if sec and not cmds and not args.strict_evidence:
        warnings.append(
            "Verified by execution has no command; gate verified CI claims independently"
        )
    if args.strict_evidence and sec and cmds and not args.evidence:
        errors.append("strict evidence: no --evidence file for Verified by execution")
    if args.evidence and os.path.exists(args.evidence):
        with open(args.evidence, encoding="utf-8", errors="replace") as f:
            ev = f.read()
        for cmd in cmds:
            key = " ".join(cmd.split())
            if key not in ev:
                errors.append(f"verified command not in evidence log: {key[:100]}")
            elif not re.search(
                re.escape(key) + r".{0,400}?(?:exit|rc)[=:\s]*0", ev, re.DOTALL
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

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
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
