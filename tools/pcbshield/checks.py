"""The shielding checks, computed in exact geometry.

Each check answers one of the defect classes the request conflates. Findings
carry board coordinates, so evidence images are rendered from findings rather
than findings being read off images.

Every check that quantizes says so in its own findings: `station_pitch_mm` on
the continuity checks is the sampling step along the trace, and a reported gap
length is that pitch times a station count. Reporting a bare millimetre figure
without it would imply a precision the sampling does not have.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from shapely.geometry import LineString, MultiLineString, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import linemerge, nearest_points, unary_union

from .geometry import (EMPTY, as_polygons, feature_geometry, flatten_arc,
                       layer_copper, net_copper)
from .odb import Job


@dataclass
class Finding:
    check: str
    severity: str                       # error | warning | info
    layer: str
    net: str
    message: str
    x_mm: float
    y_mm: float
    extent_mm: float = 0.0
    detail: Dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Params:
    """Design intent. None of this can be derived from the job file."""

    signal_nets: Sequence[str]
    shield_nets: Sequence[str]
    window_mm: float = 0.6          # how far to either side a guard may sit
    max_gap_mm: float = 1.0         # longest tolerated unshielded run
    clearance_mm: float = 0.15      # required shield-to-foreign-net spacing
    plane_margin_mm: float = 0.5    # signal footprint widening on a plane
    antipad_max_area_mm2: float = 4.0   # above this, a void is not just an anti-pad
    max_via_pitch_mm: float = 7.31  # lambda_g/20; see pcb_shield_budget.py
    station_pitch_mm: float = 0.1
    arc_tolerance_mm: float = 0.001


# --- helpers ---------------------------------------------------------------

def _net_paths(job: Job, layer: str, net: str,
               tolerance_mm: float) -> List[LineString]:
    """Centrelines of a net's line and arc features on one layer."""
    segs: List[LineString] = []
    for feat in job.layers[layer].features:
        if feat.polarity != "P" or job.net_of(layer, feat.index) != net:
            continue
        if feat.kind == "L" and feat.start and feat.end:
            if feat.start != feat.end:
                segs.append(LineString([feat.start, feat.end]))
        elif feat.kind == "A" and feat.start and feat.end and feat.center:
            pts = flatten_arc(feat.start, feat.end, feat.center,
                              feat.clockwise, tolerance_mm)
            if len(pts) > 1:
                segs.append(LineString(pts))
    if not segs:
        return []
    merged = linemerge(MultiLineString(segs))
    if isinstance(merged, LineString):
        return [merged]
    return [g for g in merged.geoms if isinstance(g, LineString)]


def _shield_geom(job: Job, layer: str, params: Params,
                 board: Optional[BaseGeometry] = None) -> BaseGeometry:
    parts = [net_copper(job, layer, n, params.arc_tolerance_mm, board)
             for n in params.shield_nets]
    parts = [p for p in parts if not p.is_empty]
    return unary_union(parts) if parts else EMPTY


def _drill_points(job: Job) -> List[Point]:
    """Via and hole positions, taken from DRILL-type layers."""
    pts: List[Point] = []
    for name in job.layer_order:
        layer = job.layers[name]
        if "DRILL" not in layer.layer_type.upper():
            continue
        for feat in layer.features:
            if feat.kind == "P" and feat.start:
                pts.append(Point(*feat.start))
    return pts


def _runs(flags: Sequence[bool]) -> List[Tuple[int, int]]:
    """Index ranges of consecutive True values, end exclusive."""
    out, start = [], None
    for i, flag in enumerate(flags):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(flags)))
    return out


# --- S1: coplanar guard continuity ----------------------------------------

def check_guard_continuity(job: Job, layer: str, params: Params,
                           board: Optional[BaseGeometry] = None
                           ) -> List[Finding]:
    shield = _shield_geom(job, layer, params, board)
    findings: List[Finding] = []
    if shield.is_empty:
        return findings

    for net in params.signal_nets:
        for path in _net_paths(job, layer, net, params.arc_tolerance_mm):
            n = max(2, int(path.length / params.station_pitch_mm) + 1)
            pitch = path.length / (n - 1)
            for side, sign in (("left", 1.0), ("right", -1.0)):
                covered: List[bool] = []
                points: List[Point] = []
                for i in range(n):
                    s = pitch * i
                    p = path.interpolate(s)
                    q = path.interpolate(min(path.length, s + pitch * 0.5))
                    dx, dy = q.x - p.x, q.y - p.y
                    norm = math.hypot(dx, dy) or 1.0
                    nx, ny = -dy / norm * sign, dx / norm * sign
                    probe = LineString([(p.x, p.y),
                                        (p.x + nx * params.window_mm,
                                         p.y + ny * params.window_mm)])
                    covered.append(shield.intersects(probe))
                    points.append(p)

                for a, b in _runs([not c for c in covered]):
                    length = (b - a - 1) * pitch
                    if length <= params.max_gap_mm:
                        continue
                    mid = points[(a + b) // 2]
                    findings.append(Finding(
                        check="S1-guard-continuity", severity="error",
                        layer=layer, net=net,
                        message=(f"{side} guard absent for {length:.3f} mm "
                                 f"(limit {params.max_gap_mm:.3f} mm)"),
                        x_mm=round(mid.x, 6), y_mm=round(mid.y, 6),
                        extent_mm=round(length, 6),
                        detail={"station_pitch_mm": round(pitch, 6),
                                "window_mm": params.window_mm,
                                "start_along_mm": round(a * pitch, 6),
                                "end_along_mm": round((b - 1) * pitch, 6)}))
    return findings


# --- S2: via-fence pitch ---------------------------------------------------

def check_via_fence_pitch(job: Job, layer: str, params: Params,
                          board: Optional[BaseGeometry] = None
                          ) -> List[Finding]:
    shield = _shield_geom(job, layer, params, board)
    drills = [p for p in _drill_points(job) if shield.intersects(p)]
    findings: List[Finding] = []
    if not drills:
        return findings

    for net in params.signal_nets:
        for path in _net_paths(job, layer, net, params.arc_tolerance_mm):
            near = [(path.project(p), p) for p in drills
                    if path.distance(p) <= params.window_mm * 2.5]
            near.sort(key=lambda item: item[0])
            if len(near) < 2:
                continue
            for (s0, p0), (s1, p1) in zip(near, near[1:]):
                gap = s1 - s0
                if gap <= params.max_via_pitch_mm:
                    continue
                findings.append(Finding(
                    check="S2-via-fence-pitch", severity="warning",
                    layer=layer, net=net,
                    message=(f"stitching via pitch {gap:.3f} mm exceeds "
                             f"{params.max_via_pitch_mm:.3f} mm"),
                    x_mm=round((p0.x + p1.x) / 2, 6),
                    y_mm=round((p0.y + p1.y) / 2, 6),
                    extent_mm=round(gap, 6),
                    detail={"limit_mm": params.max_via_pitch_mm}))
    return findings


# --- S3: reference-plane continuity ---------------------------------------

def check_plane_continuity(job: Job, signal_layer: str, plane_layer: str,
                           params: Params,
                           board: Optional[BaseGeometry] = None
                           ) -> List[Finding]:
    """Voids under the signal footprint on the adjacent plane.

    Voids that contain a drill are anti-pads — expected geometry, not defects.
    Without that classification this check drowns in false positives, which is
    the failure mode it is most likely to hit in practice.
    """
    plane = _shield_geom(job, plane_layer, params, board)
    findings: List[Finding] = []
    if plane.is_empty:
        return findings
    drills = _drill_points(job)

    # Classify on the plane's own void components, never on the sliver left
    # after clipping to the signal footprint: an anti-pad clipped by the
    # footprint no longer contains its drill, and the check would report the
    # remainder as a break. This is the false-positive source that decides
    # whether S3 is usable at all.
    #
    # Containing a drill is necessary but not sufficient. A real void that
    # touches an anti-pad merges with it into one component, and accepting the
    # whole component would make that void invisible — a silent false negative,
    # which is worse than the false positive the classifier exists to remove.
    # Oversized components are therefore reported, flagged as merged.
    expected, merged = [], []
    for poly in as_polygons(plane):
        for ring in poly.interiors:
            v = Polygon(ring)
            if not any(v.contains(d) for d in drills):
                continue
            (expected if v.area <= params.antipad_max_area_mm2
             else merged).append(v)
    antipads = unary_union(expected) if expected else EMPTY
    merged_union = unary_union(merged) if merged else EMPTY

    for net in params.signal_nets:
        sig = net_copper(job, signal_layer, net, params.arc_tolerance_mm, board)
        if sig.is_empty:
            continue
        footprint = sig.buffer(params.plane_margin_mm,
                               quad_segs=8, join_style=2)
        breach = footprint.difference(plane)
        if not antipads.is_empty:
            breach = breach.difference(antipads)
        for hole in as_polygons(breach):
            width = 2.0 * math.sqrt(hole.area / math.pi)
            if width < params.clearance_mm:
                continue
            c = hole.representative_point()
            note = (" (void merges with an anti-pad; sizes are not separable "
                    "here)" if not merged_union.is_empty
                    and merged_union.intersects(hole) else "")
            findings.append(Finding(
                check="S3-plane-continuity", severity="error",
                layer=plane_layer, net=net,
                message=(f"reference plane absent under {net} over "
                         f"{hole.area:.4f} mm^2{note}"),
                x_mm=round(c.x, 6), y_mm=round(c.y, 6),
                extent_mm=round(width, 6),
                detail={"area_mm2": round(hole.area, 6),
                        "signal_layer_hint": 0.0,
                        "margin_mm": params.plane_margin_mm}))
    return findings


# --- S4: shield / foreign-net overlap and clearance -----------------------

def check_shield_overlap(job: Job, layer: str, params: Params,
                         board: Optional[BaseGeometry] = None
                         ) -> List[Finding]:
    shield = _shield_geom(job, layer, params, board)
    findings: List[Finding] = []
    if shield.is_empty:
        return findings
    shield_set = {n for n in params.shield_nets}

    for net in sorted({job.net_of(layer, f.index)
                       for f in job.layers[layer].features
                       if job.net_of(layer, f.index)} - shield_set):
        other = net_copper(job, layer, net, params.arc_tolerance_mm, board)
        if other.is_empty:
            continue
        hit = shield.intersection(other)
        if not hit.is_empty and hit.area > 0:
            c = hit.representative_point()
            findings.append(Finding(
                check="S4-shield-overlap", severity="error", layer=layer,
                net=net,
                message=(f"shield overlaps net {net} over {hit.area:.5f} mm^2 "
                         f"— short"),
                x_mm=round(c.x, 6), y_mm=round(c.y, 6),
                detail={"area_mm2": round(hit.area, 6)}))
            continue
        gap = shield.distance(other)
        if gap < params.clearance_mm:
            pair, _ = nearest_points(shield, other)
            findings.append(Finding(
                check="S4-shield-clearance", severity="warning", layer=layer,
                net=net,
                message=(f"shield-to-{net} spacing {gap:.4f} mm below "
                         f"{params.clearance_mm:.4f} mm"),
                x_mm=round(pair.x, 6), y_mm=round(pair.y, 6),
                extent_mm=round(gap, 6),
                detail={"limit_mm": params.clearance_mm}))
    return findings


# --- S6: shield electrical connectivity -----------------------------------

def check_shield_connectivity(job: Job, layers: Sequence[str], params: Params,
                              board: Optional[BaseGeometry] = None
                              ) -> List[Finding]:
    """Islanded shield copper — geometrically present, electrically absent.

    This is the defect no capture-based method can find: every pixel is in the
    right place and the shield still does not work.
    """
    drills = _drill_points(job)
    nodes: List[Tuple[str, int, object]] = []
    for layer in layers:
        for i, poly in enumerate(as_polygons(
                _shield_geom(job, layer, params, board))):
            nodes.append((layer, i, poly))
    if len(nodes) <= 1:
        return []

    parent = list(range(len(nodes)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for i, (li, _, gi) in enumerate(nodes):
        for j, (lj, _, gj) in enumerate(nodes[i + 1:], start=i + 1):
            if li == lj:
                continue
            for d in drills:
                if gi.contains(d) and gj.contains(d):
                    union(i, j)
                    break

    groups: Dict[int, List[int]] = {}
    for i in range(len(nodes)):
        groups.setdefault(find(i), []).append(i)
    if len(groups) <= 1:
        return []

    main = max(groups.values(),
               key=lambda idxs: sum(nodes[i][2].area for i in idxs))
    findings: List[Finding] = []
    for idxs in groups.values():
        if idxs is main:
            continue
        for i in idxs:
            layer, _, poly = nodes[i]
            c = poly.representative_point()
            findings.append(Finding(
                check="S6-shield-connectivity", severity="error", layer=layer,
                net=",".join(params.shield_nets),
                message=(f"shield island of {poly.area:.4f} mm^2 has no via "
                         f"path to the main shield"),
                x_mm=round(c.x, 6), y_mm=round(c.y, 6),
                detail={"area_mm2": round(poly.area, 6)}))
    return findings


# --- data quality ----------------------------------------------------------

def check_data_quality(job: Job, params: Params) -> List[Finding]:
    """Parse gaps reported as findings, because missing copper reads as a gap.

    A shielding report that stays silent about the copper it failed to
    understand is worse than one that finds nothing.
    """
    from .odb import unresolved_features

    findings: List[Finding] = []
    if not job.has_net_attribution:
        findings.append(Finding(
            check="Q1-net-attribution", severity="error", layer="", net="",
            message=("no net attribution in eda/data — shield copper cannot be "
                     "identified and every geometric check is refused"),
            x_mm=0.0, y_mm=0.0))
    for layer, index, name in unresolved_features(job):
        findings.append(Finding(
            check="Q2-unresolved-symbol", severity="error", layer=layer,
            net=job.net_of(layer, index) or "",
            message=(f"feature {index} uses unsupported symbol {name!r}; its "
                     f"copper is missing from the model"),
            x_mm=0.0, y_mm=0.0))
    for warning in job.warnings:
        findings.append(Finding(
            check="Q3-reader-warning", severity="warning", layer="", net="",
            message=warning, x_mm=0.0, y_mm=0.0))
    return findings


def run_all(job: Job, params: Params, signal_layer: str,
            plane_layers: Sequence[str] = (),
            board: Optional[BaseGeometry] = None) -> List[Finding]:
    findings = check_data_quality(job, params)
    if not job.has_net_attribution:
        return findings
    findings += check_shield_overlap(job, signal_layer, params, board)
    findings += check_guard_continuity(job, signal_layer, params, board)
    findings += check_via_fence_pitch(job, signal_layer, params, board)
    for plane in plane_layers:
        findings += check_plane_continuity(job, signal_layer, plane, params,
                                           board)
    copper_layers = [n for n in job.layer_order
                     if "DRILL" not in job.layers[n].layer_type.upper()]
    findings += check_shield_connectivity(job, copper_layers, params, board)
    return findings
