#!/usr/bin/env python3
"""Pins the numbers quoted in the PCB/ODB++ shielding methodology document.

The document argues from arithmetic: a cheap whole-board raster is blind to the
defects being hunted, and a raster that can measure them is expensive. If those
figures drift, the argument changes and the document silently stops matching its
own evidence. That is the failure this guards.

Run:
    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

from research.pcb_shield_budget import (  # noqa: E402
    arc_flattening,
    guaranteed_samples,
    knee_frequency_mhz,
    min_detectable_gap_um,
    raster_budget,
    stitch_pitch,
)

DOC = REPO / "docs" / "research" / \
    "PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md"


class RasterBudgetTest(unittest.TestCase):

    def test_cheap_raster_is_blind_to_the_defects_being_hunted(self) -> None:
        """The core claim of section 5. A 25um/px capture — already 366 MB for
        an 8-layer stack — cannot be relied on to show a 25um gap at all."""
        self.assertEqual(guaranteed_samples(25.0, 25.0), 0)
        self.assertEqual(guaranteed_samples(50.0, 25.0), 1)
        self.assertEqual(guaranteed_samples(25.0, 50.0), 0)

    def test_measurement_grade_raster_is_expensive(self) -> None:
        """5um/px measures a 50um gap to +/-5um and costs ~9GB per stack."""
        row = raster_budget(200.0, 150.0, 5.0, 8)
        self.assertEqual((row.px_w, row.px_h), (40000, 30000))
        self.assertAlmostEqual(row.megapixels, 1200.0, places=6)
        self.assertEqual(round(row.mb_8bpp_stack), 9155)
        self.assertEqual(guaranteed_samples(50.0, 5.0), 9)

    def test_detectability_inverts_the_sampling_bound(self) -> None:
        """The bound is open: strictly wider than n*s clears n samples, and
        exactly n*s does not. Both halves matter — quoting the closed form
        would overstate what a given pixel pitch can be relied on to show."""
        for scale in (1.0, 2.0, 5.0, 10.0, 25.0, 50.0):
            for required in (1, 2, 3):
                width = min_detectable_gap_um(scale, required)
                self.assertEqual(guaranteed_samples(width, scale),
                                 required - 1)
                self.assertGreaterEqual(
                    guaranteed_samples(width + scale * 1e-6, scale), required)


class StitchPitchTest(unittest.TestCase):

    def test_the_circulating_1ghz_figure_is_the_free_space_one(self) -> None:
        """Contradiction C1: secondary guidance quotes ~15mm at 1GHz "in FR-4",
        which is lambda_0/20, not lambda_g/20."""
        row = stitch_pitch(1000.0, 4.2)
        self.assertAlmostEqual(row.pitch_free_space_mm, 14.99, places=2)
        self.assertAlmostEqual(row.pitch_in_dielectric_mm, 7.31, places=2)

    def test_knee_frequency(self) -> None:
        self.assertAlmostEqual(knee_frequency_mhz(100.0), 3500.0, places=6)
        self.assertAlmostEqual(knee_frequency_mhz(500.0), 700.0, places=6)

    def test_fast_edges_demand_sub_millimetre_pitch(self) -> None:
        row = stitch_pitch(knee_frequency_mhz(35.0), 3.5)
        self.assertLess(row.pitch_in_dielectric_mm, 1.0)


class ArcFlatteningTest(unittest.TestCase):

    def test_cad_default_tolerance_is_defect_sized(self) -> None:
        """Failure mode F4: a 13um default on a 0.15mm radius leaves an 11um
        edge error, the same order as a 25um defect."""
        row = arc_flattening(0.15, 0.013)
        self.assertEqual(row.segments, 8)
        self.assertAlmostEqual(row.actual_sagitta_um, 11.42, places=2)

    def test_achieved_sagitta_never_exceeds_the_tolerance(self) -> None:
        for radius, tol in ((0.15, 0.013), (0.15, 0.005), (0.15, 0.001),
                            (1.0, 0.001), (5.0, 0.002)):
            row = arc_flattening(radius, tol)
            self.assertLessEqual(row.actual_sagitta_um, tol * 1000.0 + 1e-9)

    def test_tolerance_must_be_below_the_radius(self) -> None:
        with self.assertRaises(ValueError):
            arc_flattening(0.15, 0.15)


class DocumentAgreementTest(unittest.TestCase):
    """The document is the deliverable; the calculator is only its evidence.
    These check that the two still say the same thing."""

    def setUp(self) -> None:
        self.text = DOC.read_text(encoding="utf-8")

    def test_document_exists_and_cites_the_calculator(self) -> None:
        self.assertIn("tools/research/pcb_shield_budget.py", self.text)

    def test_quoted_figures_appear_in_the_document(self) -> None:
        for figure in ("40000 × 30000", "9,155", "14.99", "7.31", "11.4 µm"):
            self.assertIn(figure, self.text, f"figure missing: {figure}")


if __name__ == "__main__":
    unittest.main()
