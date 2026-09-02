#!/usr/bin/env python3
"""Guards F6 and F7: a benchmark that never measures what it declared.

BENCH-0004 declared six primary measures, ran three rounds, and measured one of
them. Nothing failed, because the gap lived in the difference between two
documents — the case declaration and the execution record — and no reader ever
held both open at once.

The trap this had to avoid is recorded in the handoff that commissioned it: a
keyword search for "unsupported-claim rate" hits all three execution records,
because each one says the metric was not measured. Searching for the name of a
measure finds the sentence explaining its absence. So these checks read a
declared status, and let `measured` stand only when a named key exists in
committed raw results.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from apfguard import measures  # noqa: E402


class DeclaredMeasuresTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = measures.cases()
        cls.evidence = measures.evidence_keys()

    def executed_cases(self):
        return {b: block for b, block in self.cases.items()
                if measures.has_executions(block)}

    def test_every_executed_benchmark_declares_a_measurement_status(self) -> None:
        """Silence is what let three rounds pass without three of six measures.
        A benchmark that has run must state, per measure, whether it measured it."""
        missing = [b for b, block in self.executed_cases().items()
                   if measures.measurement_status(block) is None]
        self.assertEqual(
            missing, [],
            "executed benchmarks with no '**Measurement status:**' block in "
            f"BENCHMARK_REGISTER.md: {missing}")

    def test_status_covers_exactly_the_declared_measures(self) -> None:
        """A status block that quietly drops a measure is the original defect
        with an extra step: relevant-case precision and false-positive rate went
        unmeasured for three rounds and unmentioned in every record."""
        problems = []
        for bench, block in sorted(self.executed_cases().items()):
            status = measures.measurement_status(block) or {}
            declared = set(measures.declared_measures(block))
            for measure in sorted(declared - set(status)):
                problems.append(f"{bench}: declared but absent from status: {measure!r}")
            for measure in sorted(set(status) - declared):
                problems.append(f"{bench}: in status but never declared: {measure!r}")
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_measured_means_a_key_in_committed_raw_results(self) -> None:
        """The check that makes the status block worth having. `measured:` is a
        claim about evidence, and the evidence is machine-readable."""
        problems = []
        for bench, block in sorted(self.executed_cases().items()):
            for measure, key in sorted((measures.measurement_status(block) or {}).items()):
                if key is None:
                    continue
                if key == "!unparseable":
                    problems.append(
                        f"{bench}: {measure!r} status line is not "
                        f"'<measure> = measured:<key>' or '<measure> = unmeasured'")
                elif key not in self.evidence:
                    problems.append(
                        f"{bench}: {measure!r} claims measured:{key}, but no "
                        f"committed raw-results file contains that key")
        self.assertEqual(problems, [], "\n  " + "\n  ".join(problems))

    def test_raw_results_are_actually_readable(self) -> None:
        """If no evidence can be loaded, every `measured:` claim above would
        fail for the wrong reason and every `unmeasured` would pass vacuously."""
        self.assertGreater(len(self.evidence), 0,
                           "no committed raw results found under docs/research/executions/")


if __name__ == "__main__":
    unittest.main()
