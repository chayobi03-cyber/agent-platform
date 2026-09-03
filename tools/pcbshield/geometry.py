"""ODB++ features -> shapely geometry, in millimetres.

Three properties of this module are deliberate and load-bearing:

* **Arc flattening tolerance is an explicit argument, never a default.** A
  chord lies inside its arc, so flattening shrinks convex copper and enlarges
  voids: the error is signed and biases every gap measurement the same way. A
  13 um tolerance — a common CAD default — leaves an 11 um edge error on a
  0.15 mm radius, the same order as the defects being hunted. `circumscribe`
  flips the bias so copper can be bracketed from both sides.

* **Features are folded in file order, not unioned.** A negative feature
  subtracts from copper already painted, so order is semantic. Treating the
  feature list as a set is the difference between finding a void and inventing
  one.

* **A negative matrix polarity inverts the whole layer.** Plane layers are
  commonly stored that way, with the features being the voids. Getting this
  wrong does not degrade a shielding check, it inverts it.
"""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Sequence, Tuple

from shapely import affinity
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .odb import Contour, Feature, Job, Layer, Symbol

EMPTY: BaseGeometry = Polygon()


def segments_for(radius_mm: float, tolerance_mm: float) -> int:
    """Segments per full circle to hold sagitta within `tolerance_mm`."""
    if radius_mm <= 0:
        return 3
    ratio = min(1.0, tolerance_mm / radius_mm)
    if ratio >= 1.0:
        return 3
    return max(3, math.ceil(math.pi / math.acos(1.0 - ratio)))


def _quad_resolution(radius_mm: float, tolerance_mm: float) -> int:
    return max(1, math.ceil(segments_for(radius_mm, tolerance_mm) / 4))


def _radial_scale(n_segments: int, circumscribe: bool) -> float:
    """Push a flattened circle out to circumscribe the true one."""
    if not circumscribe:
        return 1.0
    return 1.0 / math.cos(math.pi / max(3, n_segments))


def symbol_polygon(sym: Symbol, tolerance_mm: float,
                   circumscribe: bool = False) -> BaseGeometry:
    """The symbol's shape, centred on the origin, unrotated."""
    if not sym.resolved:
        return EMPTY
    if sym.kind == "round":
        r = sym.dims[0] / 2.0
        n = segments_for(r, tolerance_mm)
        return Point(0, 0).buffer(r * _radial_scale(n, circumscribe),
                                  quad_segs=max(1, math.ceil(n / 4)))
    if sym.kind == "square":
        h = sym.dims[0] / 2.0
        return Polygon([(-h, -h), (h, -h), (h, h), (-h, h)])
    if sym.kind == "rect":
        w, h, corner = sym.dims[0] / 2.0, sym.dims[1] / 2.0, sym.dims[2]
        base = Polygon([(-w, -h), (w, -h), (w, h), (-w, h)])
        if corner > 0:
            res = _quad_resolution(corner, tolerance_mm)
            base = base.buffer(-corner, quad_segs=res).buffer(
                corner, quad_segs=res)
        return base
    if sym.kind == "oval":
        w, h = sym.dims[0], sym.dims[1]
        r = min(w, h) / 2.0
        res = _quad_resolution(r, tolerance_mm)
        if w >= h:
            spine = LineString([(-(w / 2.0 - r), 0), ((w / 2.0 - r), 0)])
        else:
            spine = LineString([(0, -(h / 2.0 - r)), (0, (h / 2.0 - r))])
        return spine.buffer(r, quad_segs=res, cap_style=1)
    return EMPTY


def flatten_arc(start: Tuple[float, float], end: Tuple[float, float],
                center: Tuple[float, float], clockwise: bool,
                tolerance_mm: float) -> List[Tuple[float, float]]:
    """Sample an ODB++ circular arc into points, endpoints included."""
    cx, cy = center
    r = math.hypot(start[0] - cx, start[1] - cy)
    if r <= 0:
        return [start, end]
    a0 = math.atan2(start[1] - cy, start[0] - cx)
    a1 = math.atan2(end[1] - cy, end[0] - cx)
    sweep = a1 - a0
    if clockwise:
        while sweep > 0:
            sweep -= 2 * math.pi
        if abs(sweep) < 1e-12:
            sweep = -2 * math.pi
    else:
        while sweep < 0:
            sweep += 2 * math.pi
        if abs(sweep) < 1e-12:
            sweep = 2 * math.pi

    n_full = segments_for(r, tolerance_mm)
    steps = max(2, math.ceil(abs(sweep) / (2 * math.pi) * n_full))
    pts = []
    for i in range(steps + 1):
        a = a0 + sweep * i / steps
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts[0], pts[-1] = start, end
    return pts


def _contour_ring(contour: Contour, tolerance_mm: float
                  ) -> List[Tuple[float, float]]:
    pts = [contour.start]
    for step in contour.steps:
        if step[0] == "seg":
            pts.append((step[1], step[2]))
        else:
            _, xe, ye, xc, yc, cw = step
            pts.extend(flatten_arc(pts[-1], (xe, ye), (xc, yc), cw,
                                   tolerance_mm)[1:])
    return pts


def _stroke(path: Sequence[Tuple[float, float]], sym: Symbol,
            tolerance_mm: float) -> BaseGeometry:
    """Paint a symbol along a path, the way a viewer draws a trace."""
    if not sym.resolved:
        return EMPTY
    if sym.kind == "round":
        r = sym.dims[0] / 2.0
        return LineString(path).buffer(
            r, quad_segs=_quad_resolution(r, tolerance_mm), cap_style=1,
            join_style=1)
    if sym.kind == "square":
        return LineString(path).buffer(sym.dims[0] / 2.0, cap_style=3,
                                       join_style=2)
    # Any other symbol used as a brush: stamp it along the path. Correct for
    # symmetric symbols and conservative for the rest.
    stamp = symbol_polygon(sym, tolerance_mm)
    if stamp.is_empty:
        return EMPTY
    pieces = [affinity.translate(stamp, x, y) for x, y in path]
    hull = [LineString(path).buffer(0.0)] if len(path) > 1 else []
    return unary_union(pieces + hull)


def feature_geometry(feat: Feature, tolerance_mm: float) -> BaseGeometry:
    """One feature as area. Empty geometry means unresolved, not absent."""
    if feat.kind == "L" and feat.start and feat.end:
        return _stroke([feat.start, feat.end], feat.symbol, tolerance_mm)
    if feat.kind == "A" and feat.start and feat.end and feat.center:
        path = flatten_arc(feat.start, feat.end, feat.center, feat.clockwise,
                           tolerance_mm)
        return _stroke(path, feat.symbol, tolerance_mm)
    if feat.kind == "P" and feat.start:
        geom = symbol_polygon(feat.symbol, tolerance_mm)
        if geom.is_empty:
            return EMPTY
        if feat.mirror:
            geom = affinity.scale(geom, xfact=-1.0, origin=(0, 0))
        if feat.angle_deg:
            geom = affinity.rotate(geom, feat.angle_deg, origin=(0, 0))
        return affinity.translate(geom, feat.start[0], feat.start[1])
    if feat.kind == "S":
        shell: Optional[List[Tuple[float, float]]] = None
        holes: List[List[Tuple[float, float]]] = []
        islands: List[Polygon] = []
        for contour in feat.contours:
            ring = _contour_ring(contour, tolerance_mm)
            if len(ring) < 3:
                continue
            if contour.kind == "I":
                if shell is None:
                    shell = ring
                else:
                    islands.append(Polygon(ring))
            else:
                holes.append(ring)
        if shell is None:
            return EMPTY
        poly = Polygon(shell, holes)
        if not poly.is_valid:
            poly = poly.buffer(0)          # F7: deterministic SIP repair
        if islands:
            poly = unary_union([poly] + [i.buffer(0) for i in islands])
        return poly
    return EMPTY


def fold_features(features: Iterable[Feature], tolerance_mm: float
                  ) -> BaseGeometry:
    """Paint features in file order: positive adds, negative subtracts."""
    positives: List[BaseGeometry] = []
    acc: BaseGeometry = EMPTY
    for feat in features:
        geom = feature_geometry(feat, tolerance_mm)
        if geom.is_empty:
            continue
        if feat.polarity == "N":
            if positives:
                acc = unary_union([acc] + positives)
                positives = []
            acc = acc.difference(geom)
        else:
            positives.append(geom)
    if positives:
        acc = unary_union([acc] + positives)
    return acc


def layer_copper(layer: Layer, tolerance_mm: float,
                 board: Optional[BaseGeometry] = None) -> BaseGeometry:
    """Copper on a layer, honouring both feature and matrix polarity."""
    painted = fold_features(layer.features, tolerance_mm)
    if not layer.negative:
        return painted
    if board is None:
        raise ValueError(
            f"layer {layer.name!r} is NEGATIVE: its features are voids, so the "
            f"board outline is required to invert them")
    return board.difference(painted)


def net_copper(job: Job, layer_name: str, net: str, tolerance_mm: float,
               board: Optional[BaseGeometry] = None) -> BaseGeometry:
    """Copper on `layer_name` belonging to `net`.

    Positive features claimed by the net are intersected with the layer's
    folded copper, so voids cut by later negative features are respected
    rather than re-filled by the per-net union.
    """
    layer = job.layers[layer_name]
    claimed = [feature_geometry(f, tolerance_mm) for f in layer.features
               if f.polarity == "P"
               and job.net_of(layer_name, f.index) == net]
    claimed = [g for g in claimed if not g.is_empty]
    if not claimed:
        return EMPTY
    return unary_union(claimed).intersection(
        layer_copper(layer, tolerance_mm, board))


def as_polygons(geom: BaseGeometry) -> List[Polygon]:
    if geom.is_empty:
        return []
    if isinstance(geom, Polygon):
        return [geom]
    if isinstance(geom, MultiPolygon):
        return list(geom.geoms)
    return [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon)]
