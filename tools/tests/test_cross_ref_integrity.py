#!/usr/bin/env python3
"""Guards the defects that exist between refs rather than inside one.

`test_docs_integrity.py` reads the working tree. Every check it makes was
green on `main` on 2026-09-02 while the repository simultaneously held three
different decisions numbered `DEC-0001`, two different experiments named
`BENCH-0004 Round 3` reaching opposite conclusions, and a benchmark recorded
`UNTESTED` that another ref had already executed. None of that is a defect in
any one tree, so nothing that reads one tree can find it.

These checks read every ref. They fail on divergence that is not recorded in
`tools/apfguard/divergence_ledger.json`, and equally on a ledger row that has
gone stale or has nothing left to describe — see `apfguard/ledger.py` for why
the ledger is a forcing function rather than a place to write "known issue".

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from apfguard import divergence, ledger, refs  # noqa: E402


class CrossRefIntegrityTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.observed = divergence.observed()
        cls.recorded = ledger.load()
        cls.heads = {refs.short(r): refs.head(r) for r in refs.branch_refs()}

    def _reconcile(self, section: str) -> None:
        problems = ledger.reconcile(
            section, self.observed[section], self.recorded.get(section, {}))
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_every_decision_identifier_names_one_decision(self) -> None:
        """Three decisions were numbered DEC-0001 on three refs, two of them
        marked DECIDED. A citation of DEC-0001 resolves to whichever branch the
        reader happens to be on."""
        self._reconcile("decision_id_collisions")

    def test_register_state_matches_what_some_ref_has_executed(self) -> None:
        """BENCH-0006 was the recorded next action on main and had already been
        executed on another ref. BENCH-0001 likewise."""
        self._reconcile("untested_but_executed")

    def test_execution_identifiers_name_one_execution(self) -> None:
        """Two experiments named BENCH-0004 Round 3, an hour apart, different
        corpora, opposite conclusions."""
        self._reconcile("execution_collisions")

    def test_work_off_main_is_accounted_for(self) -> None:
        """Forty of seventy-five commits never reached main. Divergence itself
        is not a defect; unrecorded divergence is."""
        self._reconcile("divergent_refs")

    def test_ledger_rows_are_still_pinned_to_what_they_describe(self) -> None:
        """A branch that moved after someone decided what to do about it needs
        deciding again, and a ref this clone cannot see means the guard is not
        looking rather than passing."""
        problems = ledger.stale_pins(self.recorded, self.heads)
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_dispositions_are_from_the_declared_vocabulary(self) -> None:
        """A free-text disposition is prose again, and prose is what failed."""
        allowed = set(self.recorded["_dispositions"]) - {"RESOLVED"}
        bad = [
            f"{section}/{key}: {body.get('disposition')!r}"
            for section in ledger.SECTIONS
            for key, body in sorted(self.recorded.get(section, {}).items())
            if body.get("disposition") not in allowed
        ]
        self.assertEqual(bad, [], f"disposition must be one of {sorted(allowed)}: {bad}")

    def test_the_guard_can_see_more_than_one_ref(self) -> None:
        """A single-ref clone would pass every check above by seeing nothing."""
        seen = refs.branch_refs()
        self.assertGreater(
            len(seen), 1,
            "only one ref is visible, so no cross-ref check can fail. Run: "
            "git fetch origin '+refs/heads/*:refs/remotes/origin/*'")


if __name__ == "__main__":
    unittest.main()
