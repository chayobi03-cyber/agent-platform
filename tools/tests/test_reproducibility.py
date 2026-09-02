#!/usr/bin/env python3
"""Guards that recorded benchmark evidence stays reproducible.

BENCH-0004 Round 3's results are committed evidence. Any refactoring of the
harness must leave every recorded number untouched. This test re-runs the
harness and compares its output against the committed results file.

The harness is invoked through its command-line interface rather than imported,
so this test keeps working across changes to the module layout. That is the
point: it is the fixed baseline a refactor is measured against.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HARNESS = REPO / "tools" / "bench" / "bench0004_r3.py"
RECORDED = REPO / "docs" / "research" / "executions" / "raw" / "BENCH-0004_R3_results.json"

# Every key that must reproduce exactly. `latency_ms_per_query` is deliberately
# excluded: it measures wall-clock time and legitimately varies between runs.
DETERMINISTIC_KEYS = (
    "frozen_commit",
    "alpha_primary",
    "seed",
    "null_seeds",
    "corpus_size",
    "task_count",
    "primary",
    "alpha_sweep",
    "null_models",
    "deviation_normalised_provenance",
    "graph_edges",
    "commit_order",
    "provenance_text",
)


class ReproducibilityTest(unittest.TestCase):
    """BENCH-0004 R3 must reproduce bit-identically."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.recorded = json.loads(RECORDED.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rerun.json"
            proc = subprocess.run(
                [sys.executable, str(HARNESS), "--out", str(out)],
                cwd=REPO, capture_output=True, text=True,
            )
            if proc.returncode != 0:
                raise AssertionError(
                    f"harness failed (exit {proc.returncode}):\n{proc.stderr}"
                )
            cls.rerun = json.loads(out.read_text(encoding="utf-8"))

    def test_deterministic_outputs_match_recorded_evidence(self) -> None:
        mismatched = [k for k in DETERMINISTIC_KEYS
                      if self.recorded.get(k) != self.rerun.get(k)]
        self.assertEqual(
            mismatched, [],
            "Recorded BENCH-0004 R3 evidence changed. A refactor must not alter "
            f"any recorded number. Differing keys: {mismatched}",
        )

    def test_headline_result_is_unchanged(self) -> None:
        """The falsifying result itself, stated explicitly.

        If a refactor silently flipped this, the claim state recorded in
        CLAIM_INVENTORY would no longer follow from the evidence.
        """
        c = self.rerun["primary"]["C"]["aggregate"]["cov3"]
        d4 = self.rerun["primary"]["D4"]["aggregate"]["cov3"]
        self.assertAlmostEqual(c, 0.7291666666666666, places=12)
        self.assertAlmostEqual(d4, 0.5937500000000000, places=12)
        self.assertLess(d4, c, "D4 must remain below the C baseline (falsifier F2)")

    def test_corpus_is_read_from_the_frozen_commit(self) -> None:
        """Corpus documents keep changing; the frozen read is what makes the
        recorded numbers replayable at any later HEAD."""
        self.assertEqual(
            self.rerun["frozen_commit"],
            "0d2776986d742eb8e9443a2dc9a95bcc3374efbb",
        )
        self.assertEqual(self.rerun["corpus_size"], 21)
        self.assertEqual(self.rerun["task_count"], 16)


if __name__ == "__main__":
    unittest.main()
