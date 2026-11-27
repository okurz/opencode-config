"""Keep the review command working with the gate's composed body."""

from pathlib import Path

import pytest
import yaml

COMMAND = Path(__file__).resolve().parent.parent / "commands" / "review-as-bot.md"
PROMPTS = Path.home() / ".pi" / "agent" / "prompts"


def split_command():
    _, front, body = COMMAND.read_text(encoding="utf-8").split("---\n", 2)
    return yaml.safe_load(front), body


def test_frontmatter_declares_the_command():
    front, _ = split_command()
    assert front["description"]
    assert front["argument-hint"] == "<pr|url> [--post] [--dry-run] [--comment]"


@pytest.mark.parametrize(
    "dropped",
    [
        "Record the basis in the draft",
        "Formulate a concise, pragmatic review summary",
    ],
)
def test_command_no_longer_asks_for_a_summary_or_a_basis_in_the_draft(dropped):
    _, body = split_command()
    assert dropped not in body


@pytest.mark.parametrize(
    "kept",
    [
        "$REVIEW_BOT_REPORT",
        ".report.md",
        "--report",
        "`body` in the gate's JSON",
        "An empty body is the expected result",
        "collapsed block with the report",
        "at most 300 characters",
        "8-word run with an inline comment",
        ".threads.json",
        ".replies.json",
        "comments/<id>/replies",
        "replied in <n> thread(s)",
        "no bot thread waits for an answer",
        "never needs a review of its own",
    ],
)
def test_command_states_the_body_rules_and_the_report_file(kept):
    _, body = split_command()
    assert kept in body


def test_pi_reads_the_same_commands_directory():
    if not PROMPTS.is_symlink():
        pytest.skip("not a pi checkout with a linked prompts directory")
    assert PROMPTS.resolve() == COMMAND.parent.resolve()
