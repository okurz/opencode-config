"""Cover the claim gate's composed body and its new body/bookkeeping checks."""

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parent.parent / "tools" / "verify-review-claims.py"
BOT = "os-autoinst-review"
HEAD = "abc1234def5678"
REPORT = """Basis: review-checklist.md; skills: none
Verified by execution:
- `make test` at abc1234: exit 0
Read only:
- t/01-foo.t covers the empty case
"""
EVIDENCE = "$ make test\nexit=0\n"


def pr_view(files=("t/01-foo.t",), reviews=None):
    return {
        "reviews": reviews
        or [{"author": {"login": BOT}, "submittedAt": "2026-11-27T10:00:00Z"}],
        "reviewDecision": "",
        "statusCheckRollup": [],
        "files": [{"path": path} for path in files],
        "headRefOid": HEAD,
    }


def comment(
    id,
    body,
    login=BOT,
    created="2026-11-27T10:00:00Z",
    reply_to=None,
    path=None,
    line=None,
):
    entry = {"id": id, "body": body, "user": {"login": login}, "created_at": created}
    if reply_to:
        entry["in_reply_to_id"] = reply_to
    if path:
        entry.update(path=path, line=line)
    return entry


class Gate:
    """Run the real CLI on files in a temporary directory and return its result."""

    def __init__(self, module, tmp_path, monkeypatch, capsys):
        self.module = module
        self.tmp_path = tmp_path
        self.monkeypatch = monkeypatch
        self.capsys = capsys

    def __call__(
        self,
        *,
        draft="",
        report=REPORT,
        inline=None,
        threads=None,
        replies=None,
        evidence=EVIDENCE,
        strict=False,
        view=None,
    ):
        paths = {}
        for name, content in (
            ("draft.md", draft),
            ("report.md", report),
            ("evidence.log", evidence),
        ):
            paths[name] = self.tmp_path / name
            paths[name].write_text(content, encoding="utf-8")
        argv = [
            "verify",
            "--repo",
            "owner/repo",
            "--pr",
            "1",
            "--head",
            HEAD,
            "--draft",
            str(paths["draft.md"]),
            "--report",
            str(paths["report.md"]),
            "--bot",
            BOT,
            "--json",
        ]
        for name, data in (
            ("inline.json", inline),
            ("threads.json", threads),
            ("replies.json", replies),
        ):
            if data is None:
                continue
            path = self.tmp_path / name
            path.write_text(json.dumps(data), encoding="utf-8")
            argv += ["--" + name.split(".")[0], str(path)]
        if evidence is not None:
            argv += ["--evidence", str(paths["evidence.log"])]
        if strict:
            argv.append("--strict-evidence")
        view = view or pr_view()
        self.monkeypatch.setattr(
            self.module,
            "gh_json",
            lambda args: view if args[0] == "pr" else {"login": BOT},
        )
        self.monkeypatch.setattr(
            self.module,
            "run",
            lambda cmd, cwd=None: subprocess.CompletedProcess(
                cmd, 0, "line\n" * 40, ""
            ),
        )
        self.monkeypatch.setattr(sys, "argv", argv)
        code = self.module.main()
        return code, json.loads(self.capsys.readouterr().out)


@pytest.fixture
def gate(tmp_path, monkeypatch, capsys):
    loader = importlib.machinery.SourceFileLoader("verify_review_claims", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return Gate(module, tmp_path, monkeypatch, capsys)


def test_composes_one_liner_findings_and_collapsed_report(gate):
    report = REPORT.replace("Basis:", "Round: re-review after the fixup commit\nBasis:")
    threads = [comment(7, "The fetch_data point.", path="t/01-foo.t", line=3)]
    code, out = gate(
        draft="A finding that no line can carry.\n", report=report, threads=threads
    )
    assert code == 0, out["errors"]
    assert out["body"] == (
        "Re-review after the fixup commit. 1 point from the 2026-11-27 review still open.\n\n"
        "A finding that no line can carry.\n\n"
        "<details><summary>What was checked</summary>\n\n"
        "Basis: review-checklist.md; skills: none\n"
        "Verified by execution:\n"
        "- `make test` at abc1234: exit 0\n"
        "Read only:\n"
        "- t/01-foo.t covers the empty case\n"
        "\n"
        "</details>"
    )


def test_body_stays_empty_when_every_finding_is_anchored(gate):
    inline = [
        {"path": "t/01-foo.t", "line": 3, "body": "The fetch_data point is unread."}
    ]
    code, out = gate(draft="", inline=inline)
    assert code == 0, out["errors"]
    assert out["body"] == ""


def test_rejects_a_draft_finding_that_repeats_an_inline_comment(gate):
    inline = [
        {
            "path": "t/01-foo.t",
            "line": 3,
            "body": "the fetch_data helper is never read by any consumer",
        }
    ]
    code, out = gate(
        draft="The fetch_data helper is never read by any consumer here.\n",
        inline=inline,
    )
    assert code == 1
    assert any("repeats an inline comment" in error for error in out["errors"])


def test_rejects_a_one_liner_that_repeats_an_inline_comment(gate):
    report = REPORT.replace(
        "Basis:", "Round: the fetch_data helper is never read by any consumer\nBasis:"
    )
    inline = [
        {
            "path": "t/01-foo.t",
            "line": 3,
            "body": "the fetch_data helper is never read by any consumer",
        }
    ]
    code, out = gate(draft="", report=report, inline=inline)
    assert code == 1
    assert any("repeats an inline comment" in error for error in out["errors"])


@pytest.mark.parametrize(
    "marker",
    ["Basis: review-checklist.md", "Verified by execution:", "Read only:", "<details>"],
)
def test_rejects_bookkeeping_in_the_draft(gate, marker):
    code, out = gate(draft=f"{marker}\n- `make test` at abc1234: exit 0\n")
    assert code == 1
    assert any("draft carries" in error for error in out["errors"])


def test_rejects_a_one_liner_over_the_limit(gate):
    report = REPORT.replace("Basis:", f"Round: {'x' * 190}\nBasis:")
    threads = [comment(7, "The fetch_data point.", path="t/01-foo.t", line=3)]
    code, out = gate(report=report, threads=threads)
    assert code == 1
    assert any("limit 200" in error for error in out["errors"])


@pytest.mark.parametrize(
    "entry",
    [
        "`make test` exit 0",
        "`make test` at abc1234: exit 1",
        "`make test` at HEAD: exit 0",
    ],
)
def test_rejects_a_verified_line_without_a_sha_and_exit_zero(gate, entry):
    report = REPORT.replace("- `make test` at abc1234: exit 0", f"- {entry}")
    code, out = gate(report=report)
    assert code == 1
    assert any("verified line must read" in error for error in out["errors"])


def test_rejects_a_verified_command_missing_from_the_evidence_log(gate):
    code, out = gate(evidence="$ make check\nexit=0\n")
    assert code == 1
    assert any("not in evidence log" in error for error in out["errors"])


def test_rejects_a_verified_command_without_exit_zero_in_the_evidence_log(gate):
    code, out = gate(evidence="$ make test\nexit=1\n")
    assert code == 1
    assert any("no exit 0 in evidence log" in error for error in out["errors"])


def test_rejects_a_report_line_outside_a_section(gate):
    code, out = gate(report=REPORT + "a loose note\n")
    assert code == 1
    assert any("outside a section" in error for error in out["errors"])


def test_rejects_a_missing_report(gate):
    code, out = gate(report="")
    assert code == 1
    assert any("--report missing" in error for error in out["errors"])


def test_rejects_an_unsafe_path_in_the_report(gate):
    code, out = gate(
        report=REPORT.replace(
            "t/01-foo.t covers the empty case", "client.conf holds the token"
        )
    )
    assert code == 1
    assert any("unsafe token/path" in error for error in out["errors"])


def test_counts_only_bot_roots_without_a_human_reply(gate):
    threads = [
        comment(7, "The fetch_data point.", path="t/01-foo.t", line=3),
        comment(
            8,
            "The second point.",
            created="2026-11-27T09:00:00Z",
            path="t/02-foo.t",
            line=4,
        ),
        comment(
            9,
            "Fixed in 1a2b3c4.",
            login="okurz",
            created="2026-11-27T11:00:00Z",
            reply_to=8,
        ),
    ]
    code, out = gate(threads=threads)
    assert code == 0, out["errors"]
    assert out["still_open"] == [7]
    assert out["one_liner"] == "1 point from the 2026-11-27 review still open."


def test_counts_a_thread_the_bot_reopened_after_a_human_reply(gate):
    threads = [
        comment(7, "The fetch_data point."),
        comment(
            9,
            "Fixed in 1a2b3c4.",
            login="okurz",
            created="2026-11-27T11:00:00Z",
            reply_to=7,
        ),
        comment(10, "Still open at head.", created="2026-11-27T12:00:00Z", reply_to=7),
    ]
    code, out = gate(threads=threads)
    assert code == 0, out["errors"]
    assert out["one_liner"] == "1 point from the 2026-11-27 review still open."


def test_rejects_a_reply_to_a_closed_thread(gate):
    threads = [
        comment(7, "The fetch_data point."),
        comment(
            9,
            "Fixed in 1a2b3c4.",
            login="okurz",
            created="2026-11-27T11:00:00Z",
            reply_to=7,
        ),
    ]
    code, out = gate(threads=threads, replies=[{"id": 7, "body": "Still open."}])
    assert code == 1
    assert any("not an open thread of the bot" in error for error in out["errors"])


def test_rejects_a_reply_without_a_body(gate):
    threads = [comment(7, "The fetch_data point.")]
    code, out = gate(threads=threads, replies=[{"id": 7, "body": "  "}])
    assert code == 1
    assert any("has no body" in error for error in out["errors"])


def test_rejects_an_inline_comment_on_a_line_that_already_carries_a_bot_thread(gate):
    threads = [comment(7, "The fetch_data point.", path="t/01-foo.t", line=3)]
    inline = [
        {
            "path": "t/01-foo.t",
            "line": 3,
            "body": "A different wording of the same point.",
        }
    ]
    code, out = gate(inline=inline, threads=threads)
    assert code == 1
    assert any("reply in it" in error for error in out["errors"])


def test_allows_an_inline_comment_next_to_a_bot_thread_or_a_human_one(gate):
    threads = [
        comment(7, "The fetch_data point.", path="t/01-foo.t", line=3),
        comment(8, "A human point.", login="okurz", path="t/01-foo.t", line=9),
    ]
    inline = [
        {
            "path": "t/01-foo.t",
            "line": 9,
            "body": "The retry loop drops the last error.",
        },
        {"path": "t/01-foo.t", "line": 11, "body": "The guard is unreachable."},
    ]
    code, out = gate(inline=inline, threads=threads)
    assert code == 0, out["errors"]
