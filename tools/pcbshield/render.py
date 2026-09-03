"""Deterministic rendering — evidence images, generated from findings.

A viewer screenshot cannot anchor a finding: it depends on zoom, layer colour
and blend order, and nothing in it maps back to board coordinates. Everything
here is pinned instead:

    px_x = round((x_mm - x0_mm) * 1000 / scale_um_px)
    px_y = round((y1_mm - y_mm) * 1000 / scale_um_px)

so every pixel inverts to a board coordinate, and the scale is chosen from the
defect's own size rather than from a window. Colour carries net semantics —
signal, shield, other copper — which is the part a raster capture of a viewer
throws away.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw
from shapely.geometry.base import BaseGeometry

from .checks import Finding, Params
from .geometry import as_polygons, layer_copper, net_copper
from .odb import Job

BACKGROUND = (18, 18, 20)
OTHER_COPPER = (110, 110, 116)
SHIELD = (60, 170, 110)
SIGNAL = (225, 120, 70)
MARKER = (240, 70, 170)
TEXT = (235, 235, 240)

# A defect narrower than this many pixels cannot be judged by eye.
MIN_DEFECT_PX = 120
MAX_EDGE_PX = 2400


@dataclass
class Transform:
    x0_mm: float
    y1_mm: float
    scale_um_px: float

    def to_px(self, x_mm: float, y_mm: float) -> Tuple[float, float]:
        return ((x_mm - self.x0_mm) * 1000.0 / self.scale_um_px,
                (self.y1_mm - y_mm) * 1000.0 / self.scale_um_px)

    def to_mm(self, px: float, py: float) -> Tuple[float, float]:
        return (self.x0_mm + px * self.scale_um_px / 1000.0,
                self.y1_mm - py * self.scale_um_px / 1000.0)


def _draw(geom: BaseGeometry, drw: ImageDraw.ImageDraw, tr: Transform,
          colour: Tuple[int, int, int]) -> None:
    for poly in as_polygons(geom):
        ring = [tr.to_px(x, y) for x, y in poly.exterior.coords]
        if len(ring) >= 3:
            drw.polygon(ring, fill=colour)
        for hole in poly.interiors:
            hring = [tr.to_px(x, y) for x, y in hole.coords]
            if len(hring) >= 3:
                drw.polygon(hring, fill=BACKGROUND)


def render_window(job: Job, layer: str, params: Params,
                  bbox_mm: Tuple[float, float, float, float],
                  scale_um_px: float,
                  board: Optional[BaseGeometry] = None) -> Image.Image:
    """One layer over a board-coordinate window, at a stated pixel pitch."""
    x0, y0, x1, y1 = bbox_mm
    w = max(1, min(MAX_EDGE_PX, math.ceil((x1 - x0) * 1000.0 / scale_um_px)))
    h = max(1, min(MAX_EDGE_PX, math.ceil((y1 - y0) * 1000.0 / scale_um_px)))
    img = Image.new("RGB", (w, h), BACKGROUND)
    drw = ImageDraw.Draw(img)
    tr = Transform(x0, y1, scale_um_px)

    _draw(layer_copper(job.layers[layer], params.arc_tolerance_mm, board),
          drw, tr, OTHER_COPPER)
    for net in params.shield_nets:
        _draw(net_copper(job, layer, net, params.arc_tolerance_mm, board),
              drw, tr, SHIELD)
    for net in params.signal_nets:
        _draw(net_copper(job, layer, net, params.arc_tolerance_mm, board),
              drw, tr, SIGNAL)
    return img


def _scale_bar(drw: ImageDraw.ImageDraw, tr: Transform, size: Tuple[int, int],
               label: str) -> None:
    w, h = size
    # A round number of millimetres that fits in about a fifth of the width.
    target_mm = (w * tr.scale_um_px / 1000.0) / 5.0
    step = 10.0 ** math.floor(math.log10(max(target_mm, 1e-6)))
    for mult in (1.0, 2.0, 5.0, 10.0):
        if step * mult >= target_mm:
            step *= mult
            break
    bar_px = step * 1000.0 / tr.scale_um_px
    x, y = 12, h - 18
    drw.line([(x, y), (x + bar_px, y)], fill=TEXT, width=2)
    drw.line([(x, y - 4), (x, y + 4)], fill=TEXT, width=2)
    drw.line([(x + bar_px, y - 4), (x + bar_px, y + 4)], fill=TEXT, width=2)
    drw.text((x, y - 16), f"{step:g} mm", fill=TEXT)
    drw.text((12, 10), label, fill=TEXT)


def evidence_image(job: Job, finding: Finding, params: Params, out: Path,
                   board: Optional[BaseGeometry] = None,
                   scale_um_px: Optional[float] = None) -> Path:
    """Render one finding at a scale where the defect is actually judgeable."""
    layer = finding.layer or job.layer_order[0]
    extent = max(finding.extent_mm, 0.2)
    if scale_um_px is None:
        scale_um_px = max(1.0, extent * 1000.0 / MIN_DEFECT_PX)

    half = max(extent * 1.8, 1.0)
    bbox = (finding.x_mm - half, finding.y_mm - half,
            finding.x_mm + half, finding.y_mm + half)
    img = render_window(job, layer, params, bbox, scale_um_px, board)
    drw = ImageDraw.Draw(img)
    tr = Transform(bbox[0], bbox[3], scale_um_px)

    cx, cy = tr.to_px(finding.x_mm, finding.y_mm)
    r = max(6.0, extent * 1000.0 / scale_um_px / 2.0)
    drw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=MARKER, width=3)
    _scale_bar(drw, tr, img.size,
               f"{finding.check}  {finding.net or '-'}@{layer}  "
               f"({finding.x_mm:.3f}, {finding.y_mm:.3f}) mm  "
               f"{scale_um_px:g} um/px")

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def render_findings(job: Job, findings: Sequence[Finding], params: Params,
                    out_dir: Path,
                    board: Optional[BaseGeometry] = None) -> List[Path]:
    """One image per finding that has a location. Data-quality findings have
    no coordinates and are deliberately skipped rather than rendered at the
    origin, which would be a picture of the wrong place."""
    paths: List[Path] = []
    for i, finding in enumerate(findings):
        if not finding.layer or finding.check.startswith("Q"):
            continue
        name = f"{i:03d}_{finding.check}_{finding.net or 'na'}.png"
        paths.append(evidence_image(job, finding, params,
                                    Path(out_dir) / name, board))
    return paths
