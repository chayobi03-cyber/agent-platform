#!/usr/bin/env python3
"""Guards the document defects found and fixed under DEC-0001.

Each check corresponds to a real defect that was present in `main`, not a
hypothetical one. The point is that the next occurrence fails a test instead of
surviving until someone reads all the documents side by side.

Historical records are exempt from the checks a fix would require editing them
into falsehood. Execution records under `docs/research/executions/` are
append-only evidence, and decision records under `docs/decisions/` must be able
to name what they retired — DEC-0001 cannot document the removal of `FB-*`
without writing `FB-*`. Both may legitimately quote a superseded identifier or
ordering; neither may be rewritten to satisfy a linter.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
# Append-only or historical: may quote superseded identifiers and orderings.
HISTORICAL_DIRS = (
    REPO / "docs" / "research" / "executions",
    REPO / "docs" / "decisions",
)
REGISTER = REPO / "docs" / "research" / "BENCHMARK_REGISTER.md"

DOC_PATH_RE = re.compile(r"docs/[A-Za-z0-9_/.-]*\.md")
# Real artifacts carry digits (fileciteturn6file0). The R3 predeclaration
# describes the defect using the placeholder `fileciteturnNfileM`, which must
# not trip this check.
CITATION_ARTIFACT_RE = re.compile(r"filecite\w*turn\d+file\d+")
FB_ID_RE = re.compile(r"\bFB-\d{4}\b")
BENCH_ID_RE = re.compile(r"BENCH-\d{4}")
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.S)
RETIRED_ORDER_HEADINGS = (
    "Initial Test Sequence",
    "First execution recommendation",
    "Initial execution order",
)


def markdown_files(include_historical: bool = True):
    for path in sorted(REPO.rglob("*.md")):
        if ".git" in path.parts:
            continue
        if not include_historical and any(d in path.parents for d in HISTORICAL_DIRS):
            continue
        yield path


class DocsIntegrityTest(unittest.TestCase):

    def test_no_dangling_document_references(self) -> None:
        """A reference to a document that does not exist is a provenance break.

        This is the defect the fileciteturn markers represented: a pointer in a
        traceability document that resolves to nothing.
        """
        dangling = []
        for path in markdown_files():
            for ref in set(DOC_PATH_RE.findall(path.read_text(encoding="utf-8"))):
                if not (REPO / ref).is_file():
                    dangling.append(f"{path.relative_to(REPO)} -> {ref}")
        self.assertEqual(dangling, [], f"dangling document references: {dangling}")

    def test_no_unresolved_citation_artifacts(self) -> None:
        """AI-tool citation markers must not survive into committed documents."""
        found = []
        for path in markdown_files():
            if CITATION_ARTIFACT_RE.search(path.read_text(encoding="utf-8")):
                found.append(str(path.relative_to(REPO)))
        self.assertEqual(found, [], f"unresolved citation artifacts in: {found}")

    def test_execution_order_is_declared_in_exactly_one_place(self) -> None:
        """Three documents once declared three different execution orders.

        A fenced block enumerating four or more distinct benchmark ids is an
        order declaration. Only the register may contain one.
        """
        declaring = []
        for path in markdown_files(include_historical=False):
            text = path.read_text(encoding="utf-8")
            for block in FENCED_BLOCK_RE.findall(text):
                if len(set(BENCH_ID_RE.findall(block))) >= 4:
                    declaring.append(str(path.relative_to(REPO)))
                    break
        self.assertEqual(
            declaring, [str(REGISTER.relative_to(REPO))],
            "the execution order must be declared only in BENCHMARK_REGISTER.md; "
            f"found declarations in: {declaring}",
        )

    def test_retired_order_headings_are_gone(self) -> None:
        found = []
        for path in markdown_files(include_historical=False):
            text = path.read_text(encoding="utf-8")
            for heading in RETIRED_ORDER_HEADINGS:
                if heading in text:
                    found.append(f"{path.relative_to(REPO)}: {heading}")
        self.assertEqual(found, [], f"retired order headings still present: {found}")

    def test_fb_identifiers_only_appear_in_the_mapping_table(self) -> None:
        """FB-* is retired in favour of BENCH-*, which every execution record
        filename already uses. The register keeps the mapping; nothing else may
        use the retired scheme."""
        offenders = []
        for path in markdown_files(include_historical=False):
            if path == REGISTER:
                continue
            if FB_ID_RE.search(path.read_text(encoding="utf-8")):
                offenders.append(str(path.relative_to(REPO)))
        self.assertEqual(offenders, [], f"retired FB-* identifiers in: {offenders}")

    def test_superseded_stubs_name_a_replacement_that_exists(self) -> None:
        """A stub exists to keep a cited path resolvable. One that points
        nowhere is worse than the deletion it was meant to avoid."""
        broken = []
        for path in markdown_files(include_historical=False):
            text = path.read_text(encoding="utf-8")
            if "**Status:** SUPERSEDED" not in text:
                continue
            match = re.search(r"\*\*Read instead:\*\*\s*`([^`]+)`", text)
            if not match:
                broken.append(f"{path.relative_to(REPO)}: no replacement named")
            elif not (REPO / match.group(1)).is_file():
                broken.append(f"{path.relative_to(REPO)} -> {match.group(1)}")
        self.assertEqual(broken, [], f"broken supersession stubs: {broken}")

    def test_decision_record_exists_for_the_consolidation(self) -> None:
        """DEC-0001 is cited across the consolidated documents; the Constitution
        requires the decision itself to be recorded, not merely referenced."""
        decision = REPO / "docs" / "decisions" / \
            "DEC-0001-benchmark-id-and-doc-consolidation.md"
        self.assertTrue(decision.is_file(), "DEC-0001 record is missing")
        text = decision.read_text(encoding="utf-8")
        for field in ("id:", "status:", "date:", "## Human decision",
                      "## Alternatives", "## Risks", "## Verification plan"):
            self.assertIn(field, text, f"DEC-0001 missing required field: {field}")


if __name__ == "__main__":
    unittest.main()
