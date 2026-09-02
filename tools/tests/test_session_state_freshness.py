#!/usr/bin/env python3
"""Guards F9: the state document a session reads before it starts working.

`SESSION_STATE.md` was last written 2026-08-31 12:10. BENCH-0004 R1 and R2 were
executed at 12:22 and 12:25 and the state document was not touched. The next
session opened it, believed it, and planned against a repository position that
was two executions out of date.

Nothing detected that, because staleness is not visible in the file. It is only
visible in the relationship between the file and the commits after it — which
is a question about git, not about the working tree.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from apfguard import refs  # noqa: E402

STATE = "docs/handoff/SESSION_STATE.md"
# Evidence: a benchmark execution changes where the project stands, so a state
# document older than one is describing a position the project has left.
EVIDENCE = "docs/research/executions/"


def _log(*args: str) -> list[str]:
    out = subprocess.run(("git", "log", *args), cwd=refs.REPO,
                         check=True, capture_output=True, text=True).stdout
    return [line for line in out.splitlines() if line.strip()]


class SessionStateFreshnessTest(unittest.TestCase):

    def test_session_state_is_not_older_than_the_evidence_it_summarises(self) -> None:
        state_commits = _log("-1", "--format=%H", "HEAD", "--", STATE)
        self.assertTrue(state_commits, f"{STATE} has never been committed")
        newer = _log("--format=%h %ad %s", "--date=format:%Y-%m-%d %H:%M",
                     f"{state_commits[0]}..HEAD", "--", EVIDENCE)
        self.assertEqual(
            newer, [],
            f"\n  {STATE} was last updated before these execution commits, so a "
            f"session reading it would plan against a stale position:\n    "
            + "\n    ".join(newer))

    def test_session_state_names_a_working_branch_that_exists(self) -> None:
        """The state document names the branch the work is on. A branch that no
        longer exists means the reader is being pointed at nothing."""
        text = (refs.REPO / STATE).read_text(encoding="utf-8")
        import re
        named = re.findall(r"^\s*[-*]?\s*(?:\*\*)?Working branch:?(?:\*\*)?:?\s*`([^`]+)`",
                           text, re.M)
        self.assertTrue(
            named, f"{STATE} names no working branch; a session cannot check "
                   f"whether it is continuing work or forking it")
        visible = {refs.short(r) for r in refs.branch_refs()}
        missing = [b for b in named if b not in visible]
        self.assertEqual(missing, [],
                         f"{STATE} names branches that do not exist: {missing}")


if __name__ == "__main__":
    unittest.main()
