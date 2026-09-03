#!/usr/bin/env python3
"""Guards F2, F3, F4: one subject declared in several documents at once.

`DEC-0001` fixed this by editing the documents, and the fix held on `main` and
nowhere else. `claude/handover-eu02yk` still has three documents declaring the
benchmark execution order — including `SESSION_STATE.md`, which the consolidation
was supposed to have cleared — and `claude/session-governance-decisions-6fi9vf`
has four declaring the claim state vocabulary. Both are open pull requests, so
the defect re-enters `main` with whichever merges first.

Ownership is declared in `apfguard/subject_manifest.json` rather than written
into these assertions, so adding a subject does not mean writing a test, and the
rule is stated once. Detectors identify a *declaration*: a document that cites
the register's order is not declaring one, and a fenced block enumerating four
benchmark ids is.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from apfguard import divergence, ledger, refs, subjects  # noqa: E402


class SubjectOwnershipTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = subjects.load()

    def test_every_subject_has_an_enforceable_detector(self) -> None:
        """A subject whose detector kind is unimplemented is a rule that reads
        as enforced and is not. That is the whole failure pattern in one line."""
        problems = []
        for name, subject in sorted(self.manifest["subjects"].items()):
            kind = subject.get("detector", {}).get("kind")
            if kind not in subjects.KINDS:
                problems.append(f"{name}: detector kind {kind!r} is not implemented")
            if not (Path(refs.REPO) / subject["owner"]).is_file():
                problems.append(f"{name}: owner {subject['owner']} does not exist")
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_each_owner_actually_declares_the_subject_it_owns(self) -> None:
        """Ownership without declaration means the subject is declared nowhere.
        A consolidation that empties every document is not a consolidation."""
        declaring = subjects.declarers_worktree()
        missing = [
            f"{name}: owner {subject['owner']} no longer declares it"
            for name, subject in sorted(self.manifest["subjects"].items())
            if subject["owner"] not in declaring[name]
        ]
        self.assertEqual(missing, [], "\n  " + "\n  ".join(missing))

    def test_no_document_here_declares_a_subject_it_does_not_own(self) -> None:
        """The working-tree check: files on disk, not the committed ref, so an
        edit fails before it is committed rather than one commit later."""
        found = subjects.violations_worktree()
        problems = [
            f"{subject}: declared by {path}, owned by "
            f"{self.manifest['subjects'][subject]['owner']}"
            for subject, paths in sorted(found.items()) for path in paths
        ]
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_ownership_violations_on_other_refs_are_recorded(self) -> None:
        """Two open pull requests carry the defect DEC-0001 retired. Recorded,
        not resolved — merging someone's branch is not the guard's decision."""
        problems = ledger.reconcile(
            "subject_ownership",
            divergence.observed()["subject_ownership"],
            ledger.load().get("subject_ownership", {}))
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))


if __name__ == "__main__":
    unittest.main()
