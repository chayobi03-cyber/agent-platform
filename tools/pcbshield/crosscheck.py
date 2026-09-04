"""Renderer XOR cross-check — does an independent implementation agree?

The geometry model in this package is derived from a reading of the ODB++
format. That reading can be wrong in ways no self-test catches, because the
test fixture and the reader share assumptions. Differencing our raster against
one produced by a separate implementation is the check that does not share
them.

It found a real defect on its first run: standard-symbol dimensions are
thousandths of the file unit (microns in an MM job), and the reader was taking
them as file units — every trace width and pad a thousand times too large. The
fixture wrote them the same wrong way, so the whole suite passed.

Usage — render a reference with any tool that can produce a per-layer SVG plus
PNG over the same viewBox, then:

    python3 -m pcbshield.crosscheck JOB_DIR --layer top \\
        --ref-svg ref/top.svg --ref-png ref/top.png --out xor/

A non-zero disagreement fraction is a parse gap somewhere, not a rounding
detail: both sides are painting the same copper.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops

from .checks import Params
from .geometry import fold_features
from .odb import read_job
from .render import BACKGROUND, render_window

VIEWBOX_RE = re.compile(
    r'viewBox\s*=\s*"\s*(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)\s+'
    r'(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)\s*"')


def read_viewbox(svg_path: Path) -> Tuple[float, float, float, float]:
    """(min x, min y, width, height) in the job's own units, from the SVG.

    The reference SVG flips y inside a transform, but its viewBox still spans
    the original coordinate range, so the window maps directly.
    """
    head = svg_path.read_text(encoding="utf-8", errors="replace")[:4000]
    m = VIEWBOX_RE.search(head)
    if not m:
        raise ValueError(f"no viewBox in {svg_path}")
    return tuple(float(g) for g in m.groups())  # type: ignore[return-value]


def _mask_ours(img: Image.Image) -> Image.Image:
    """Copper mask for our own render: anything that is not the ground.

    Thresholding on brightness would be wrong here — our copper roles are
    mid-tone by design, and a brightness rule silently classified all of them
    as background on the first run.
    """
    ground = Image.new("RGB", img.size, BACKGROUND)
    delta = ImageChops.difference(img.convert("RGB"), ground).convert("L")
    return delta.point(lambda v: 255 if v > 8 else 0).convert("1")


def _mask_reference(img: Image.Image, dark_on_white: bool) -> Image.Image:
    """Copper mask for the reference render, which is monochrome by request."""
    grey = img.convert("L")
    if dark_on_white:
        return grey.point(lambda v: 255 if v < 128 else 0).convert("1")
    return grey.point(lambda v: 255 if v > 128 else 0).convert("1")


def _count(mask: Image.Image) -> int:
    return mask.convert("L").histogram()[255]


@dataclass
class Disagreement:
    ours_px: int
    theirs_px: int
    xor_px: int
    total_px: int

    @property
    def intersection_px(self) -> int:
        return (self.ours_px + self.theirs_px - self.xor_px) // 2

    @property
    def union_px(self) -> int:
        return self.ours_px + self.theirs_px - self.intersection_px

    @property
    def fraction_of_frame(self) -> float:
        return self.xor_px / self.total_px if self.total_px else 0.0

    @property
    def fraction_of_union(self) -> float:
        return self.xor_px / self.union_px if self.union_px else 0.0

    def summary(self) -> str:
        return (f"ours={self.ours_px} px  reference={self.theirs_px} px  "
                f"xor={self.xor_px} px  "
                f"{self.fraction_of_frame * 100:.4f}% of frame  "
                f"{self.fraction_of_union * 100:.4f}% of union")


def compare(ours: Image.Image, reference: Image.Image,
            reference_is_dark_on_white: bool = True
            ) -> Tuple[Disagreement, Image.Image]:
    """XOR two renders of the same window.

    Returns the disagreement and a diff image coloured by which side has
    copper the other does not — the direction matters, because copper only we
    draw and copper only they draw fail for different reasons.
    """
    if ours.size != reference.size:
        reference = reference.resize(ours.size, Image.NEAREST)
    a = _mask_ours(ours)
    b = _mask_reference(reference, reference_is_dark_on_white)

    xor = ImageChops.logical_xor(a, b)
    only_ours = ImageChops.logical_and(a, xor)
    only_ref = ImageChops.logical_and(b, xor)
    both = ImageChops.logical_and(a, b)

    diff = Image.new("RGB", ours.size, (16, 16, 18))
    diff.paste((70, 70, 76), mask=both)
    diff.paste((225, 120, 70), mask=only_ours)
    diff.paste((60, 170, 230), mask=only_ref)

    stats = Disagreement(_count(a), _count(b), _count(xor),
                         ours.size[0] * ours.size[1])
    return stats, diff


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pcbshield.crosscheck")
    ap.add_argument("job")
    ap.add_argument("--step", default=None)
    ap.add_argument("--layer", required=True)
    ap.add_argument("--ref-svg", required=True,
                    help="reference SVG — read only for its viewBox")
    ap.add_argument("--ref-png", required=True,
                    help="reference raster of the same window")
    ap.add_argument("--unit-scale", type=float, default=1.0,
                    help="viewBox unit -> mm (25.4 if the reference is in inches)")
    ap.add_argument("--arc-tolerance-mm", type=float, default=0.001)
    ap.add_argument("--out", default="crosscheck")
    ap.add_argument("--max-fraction", type=float, default=0.0,
                    help="exit non-zero above this disagreement fraction")
    args = ap.parse_args(argv)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    vbx, vby, vbw, vbh = read_viewbox(Path(args.ref_svg))
    s = args.unit_scale

    with Image.open(args.ref_png) as ref_img:
        ref = ref_img.convert("RGB")
        width_px, height_px = ref.size

    # Derive the window from the reference's own pixel grid rather than from
    # the viewBox height. Rounding the height independently leaves the two
    # frames a pixel apart, and the nearest-neighbour resize that papers over
    # that mismatch injects more disagreement than the thing being measured.
    scale_um_px = (vbw * s) * 1000.0 / width_px
    y_centre = (vby + vbh / 2.0) * s
    half_h = height_px * scale_um_px / 2000.0
    bbox = (vbx * s, y_centre - half_h, (vbx + vbw) * s, y_centre + half_h)
    job = read_job(Path(args.job), args.step)
    params = Params(signal_nets=[], shield_nets=[],
                    arc_tolerance_mm=args.arc_tolerance_mm)
    board = fold_features(job.profile, params.arc_tolerance_mm)
    ours = render_window(job, args.layer, params, bbox, scale_um_px,
                         board if not board.is_empty else None,
                         max_edge_px=max(width_px, height_px))
    if ours.size != (width_px, height_px):
        ours = ours.resize((width_px, height_px), Image.NEAREST)

    stats, diff = compare(ours, ref)
    ours.save(out / f"{args.layer}_ours.png")
    ref.save(out / f"{args.layer}_reference.png")
    diff.save(out / f"{args.layer}_diff.png")

    print(f"layer {args.layer}: window {bbox[0]:.3f},{bbox[1]:.3f} .. "
          f"{bbox[2]:.3f},{bbox[3]:.3f} mm at {scale_um_px:.2f} um/px "
          f"({width_px}x{height_px})")
    print(f"  {stats.summary()}")
    print(f"  orange = only ours, blue = only the reference -> "
          f"{out / (args.layer + '_diff.png')}")
    if stats.fraction_of_frame > args.max_fraction:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
