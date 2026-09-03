#!/usr/bin/env python3
"""Injected-defect validation for the shielding checks.

This is the pattern registered as ASSET-0003, executed rather than proposed:
defects of known class, position and size are constructed, so detection,
localisation and size error are measurable without an oracle. The null control
carries as much weight as the detections — a checker that flags everything
scores perfect recall, and only a clean board that stays silent rules it out.

Requires shapely and pillow (`tools/pcbshield/requirements.txt`); the whole
module skips when they are absent, so the standard-library suite still runs.

    python3 -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

try:
    from pcbshield.checks import Params, run_all
    from pcbshield.geometry import (fold_features, layer_copper,
                                    segments_for, symbol_polygon)
    from pcbshield.odb import Feature, Layer, parse_symbol, read_job
    from pcbshield.render import Transform, evidence_image
    from pcbshield.synth import Defects, build_job
    DEPS = True
except ImportError:                                  # pragma: no cover
    DEPS = False

requires_deps = unittest.skipUnless(
    DEPS, "pcbshield needs shapely and pillow (see tools/pcbshield/requirements.txt)")

PARAMS = dict(signal_nets=["SIG"], shield_nets=["GND"], window_mm=1.0,
              max_via_pitch_mm=1.5)


def _run(defects=None):
    root = Path(tempfile.mkdtemp())
    injected = build_job(root, defects or Defects())
    job = read_job(root)
    params = Params(**PARAMS)
    return job, injected, run_all(job, params, "top", plane_layers=["l2"])


def _geometric(findings):
    return [f for f in findings if not f.check.startswith("Q")]


@requires_deps
class NullControlTest(unittest.TestCase):

    def test_clean_board_produces_no_findings(self) -> None:
        """The measure that stops a checker from earning recall by flagging
        everything. It is also the one that failed first in development: an
        anti-pad clipped by the signal footprint no longer contains its drill
        and was reported as a plane break."""
        job, injected, findings = _run()
        self.assertEqual(injected, [])
        self.assertEqual([f.message for f in findings], [])

    def test_clean_board_parses_without_warnings(self) -> None:
        job, _, _ = _run()
        self.assertEqual(job.warnings, [])
        self.assertTrue(job.has_net_attribution)
        self.assertEqual(sorted(job.nets()), ["GND", "SIG"])


@requires_deps
class DetectionTest(unittest.TestCase):

    def _only(self, findings, check):
        hits = [f for f in _geometric(findings) if f.check == check]
        self.assertEqual(len(hits), 1,
                         f"expected exactly one {check}, got "
                         f"{[f.check for f in _geometric(findings)]}")
        return hits[0]

    def test_guard_break_is_found_and_located(self) -> None:
        job, injected, findings = _run(Defects(guard_gap=(8.0, 11.0)))
        hit = self._only(findings, "S1-guard-continuity")
        truth = injected[0]
        self.assertAlmostEqual(hit.x_mm, truth.x_mm, delta=0.2)
        self.assertIn("left", hit.message)
        # The copper gap is shorter than the removed span by one line cap at
        # each end, and the measurement quantizes to the station pitch.
        pitch = hit.detail["station_pitch_mm"]
        self.assertLessEqual(hit.extent_mm, truth.size_mm)
        self.assertGreaterEqual(hit.extent_mm, truth.size_mm - 0.3 - 2 * pitch)

    def test_plane_void_is_found_and_sized(self) -> None:
        job, injected, findings = _run(Defects(plane_void=(9.0, 1.5)))
        hit = self._only(findings, "S3-plane-continuity")
        self.assertAlmostEqual(hit.x_mm, 9.0, delta=0.2)
        self.assertAlmostEqual(hit.y_mm, 5.0, delta=0.2)
        self.assertGreater(hit.detail["area_mm2"], 0.5)

    def test_shield_short_is_found(self) -> None:
        job, injected, findings = _run(Defects(shield_short=True))
        hit = self._only(findings, "S4-shield-overlap")
        self.assertAlmostEqual(hit.x_mm, 10.0, delta=0.2)
        self.assertGreater(hit.detail["area_mm2"], 0.0)

    def test_floating_shield_is_found(self) -> None:
        """The defect no capture-based method can find: the copper is all
        present and in the right place."""
        job, injected, findings = _run(Defects(floating_island=True))
        hit = self._only(findings, "S6-shield-connectivity")
        self.assertAlmostEqual(hit.x_mm, 2.0, delta=0.1)
        self.assertAlmostEqual(hit.detail["area_mm2"], 2.0, delta=0.05)

    def test_via_fence_gap_is_found(self) -> None:
        job, injected, findings = _run(Defects(via_fence_gap=(7.0, 12.0)))
        hits = [f for f in findings if f.check == "S2-via-fence-pitch"]
        self.assertEqual(len(hits), 1)
        self.assertGreater(hits[0].extent_mm, 1.5)

    def test_void_merged_with_an_antipad_is_reported_not_swallowed(self) -> None:
        """Containing a drill is not sufficient to call a void expected. A real
        void that touches an anti-pad merges with it, and accepting the merged
        component would hide the void completely."""
        job, injected, findings = _run(Defects(plane_void=(6.0, 1.5)))
        hit = self._only(findings, "S3-plane-continuity")
        self.assertIn("merges with an anti-pad", hit.message)


@requires_deps
class ModelCorrectnessTest(unittest.TestCase):

    def test_negative_features_subtract_in_file_order(self) -> None:
        """Folding, not unioning. Treating the feature list as a set turns a
        void back into copper."""
        sym = parse_symbol("s2", 1.0)
        pos = Feature(index=0, kind="P", polarity="P", symbol=sym,
                      start=(0.0, 0.0))
        neg = Feature(index=1, kind="P", polarity="N",
                      symbol=parse_symbol("s1", 1.0), start=(0.0, 0.0))
        folded = fold_features([pos, neg], 0.001)
        self.assertAlmostEqual(folded.area, 4.0 - 1.0, places=6)
        # Order matters: painting the positive last fills the void back in.
        self.assertAlmostEqual(fold_features([neg, pos], 0.001).area, 4.0,
                               places=6)

    def test_negative_layer_polarity_requires_the_board_outline(self) -> None:
        """A NEGATIVE plane layer's features are voids. Inverting them without
        an outline is impossible, and guessing one would invert the check."""
        layer = Layer(name="l2", polarity="NEGATIVE")
        with self.assertRaises(ValueError):
            layer_copper(layer, 0.001)

    def test_arc_tolerance_is_honoured(self) -> None:
        """The contract is the sagitta bound, not the area. Asserting area
        against pi*r^2 would assert the bias away instead of measuring it."""
        self.assertEqual(segments_for(0.15, 0.013), 8)
        self.assertEqual(segments_for(0.15, 0.001), 28)

        from shapely.geometry import Point
        radius, tol = 0.5, 0.0005
        fine = symbol_polygon(parse_symbol("r1", 1.0), tol)
        inradius = min(Point(0, 0).distance(Point(p))
                       for p in fine.exterior.coords)
        self.assertLessEqual(radius - inradius, tol + 1e-12)

        coarse = symbol_polygon(parse_symbol("r1", 1.0), 0.05)
        # Chords lie inside the arc, so a coarser tolerance removes copper.
        self.assertLess(coarse.area, fine.area)
        self.assertLess(fine.area, 3.14159265 * radius ** 2)

        # Circumscribing flips the bias, which is what makes bracketing a
        # measurement from both sides possible.
        out = symbol_polygon(parse_symbol("r1", 1.0), tol, circumscribe=True)
        self.assertGreater(out.area, 3.14159265 * radius ** 2)

    def test_unknown_symbol_is_reported_not_silently_dropped(self) -> None:
        """Missing copper reads as a shield break, so a symbol the reader does
        not understand has to surface as a finding."""
        root = Path(tempfile.mkdtemp())
        build_job(root, Defects())
        features = root / "steps" / "pcb" / "layers" / "top" / "features"
        text = features.read_text(encoding="utf-8")
        features.write_text(text.replace("$0 r0.2", "$0 thermal_rounded_x"),
                            encoding="utf-8")
        job = read_job(root)
        findings = run_all(job, Params(**PARAMS), "top")
        quality = [f for f in findings if f.check == "Q2-unresolved-symbol"]
        self.assertTrue(quality)
        self.assertIn("thermal_rounded_x", quality[0].message)

    def test_missing_net_attribution_refuses_rather_than_guesses(self) -> None:
        root = Path(tempfile.mkdtemp())
        build_job(root, Defects(shield_short=True))
        (root / "steps" / "pcb" / "eda" / "data").unlink()
        job = read_job(root)
        findings = run_all(job, Params(**PARAMS), "top")
        self.assertFalse(job.has_net_attribution)
        self.assertEqual([f.check for f in findings if f.severity == "error"],
                         ["Q1-net-attribution"])
        self.assertEqual(_geometric(findings), [])


@requires_deps
class EvidenceTest(unittest.TestCase):

    def test_pixels_invert_to_board_coordinates(self) -> None:
        tr = Transform(x0_mm=3.0, y1_mm=9.0, scale_um_px=5.0)
        px, py = tr.to_px(4.25, 7.5)
        self.assertEqual((px, py), (250.0, 300.0))
        self.assertEqual(tr.to_mm(px, py), (4.25, 7.5))

    def test_evidence_scale_makes_the_defect_judgeable(self) -> None:
        job, injected, findings = _run(Defects(guard_gap=(8.0, 11.0)))
        hit = [f for f in findings if f.check == "S1-guard-continuity"][0]
        out = Path(tempfile.mkdtemp()) / "evidence.png"
        evidence_image(job, hit, Params(**PARAMS), out)
        self.assertTrue(out.is_file())
        from PIL import Image
        with Image.open(out) as img:
            self.assertGreaterEqual(min(img.size), 200)


if __name__ == "__main__":
    unittest.main()
