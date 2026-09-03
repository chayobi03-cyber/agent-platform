#!/usr/bin/env python3
"""Reproducible numbers behind the PCB/ODB++ shielding inspection methodology.

This is a *research computation*, not an APF asset and not platform code. It
exists so that the quantities quoted in
`docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md` can be re-derived
instead of trusted, and so that a later edit to those numbers fails a test
rather than passing unnoticed.

Four independent budgets decide whether a capture-first inspection can work at
all:

1. raster cost      — bytes per copper layer at a given pixel pitch
2. detectability    — the smallest gap a raster at that pitch can be relied on
                      to show, and the error on its measured width
3. stitching pitch  — the lambda/20 bound a via fence must satisfy
4. arc flattening   — how far a flattened arc departs from the true copper edge

Standard library only. Deterministic. Run:

    python3 tools/research/pcb_shield_budget.py
"""

from __future__ import annotations

import math
from typing import NamedTuple, Sequence

# Speed of light, mm/s -> convenient form: free-space wavelength in mm for MHz.
C_MM_MHZ = 299792.458


class RasterRow(NamedTuple):
    scale_um: float
    px_w: int
    px_h: int
    megapixels: float
    mb_1bpp: float
    mb_8bpp: float
    mb_8bpp_stack: float


def raster_budget(board_w_mm: float, board_h_mm: float, scale_um: float,
                  copper_layers: int) -> RasterRow:
    """Cost of holding one copper layer as a raster at `scale_um` per pixel.

    `mb_8bpp_stack` is the whole copper stack at one byte per pixel, which is
    what a per-net or per-polarity working image actually costs.
    """
    px_w = math.ceil(board_w_mm * 1000.0 / scale_um)
    px_h = math.ceil(board_h_mm * 1000.0 / scale_um)
    px = px_w * px_h
    mb = 1024.0 * 1024.0
    return RasterRow(
        scale_um=scale_um,
        px_w=px_w,
        px_h=px_h,
        megapixels=px / 1e6,
        mb_1bpp=math.ceil(px / 8) / mb,
        mb_8bpp=px / mb,
        mb_8bpp_stack=px * copper_layers / mb,
    )


def guaranteed_samples(width_um: float, scale_um: float) -> int:
    """Background samples an unlucky gap of `width_um` is guaranteed to produce.

    A pixel grid samples on a lattice of pitch `scale_um` at an arbitrary phase.
    An open interval of length w placed anywhere on a lattice of pitch s
    contains at least ceil(w/s) - 1 lattice points. That worst case, not the
    average, is what a defect check must be sized against: the gap does not get
    to choose its phase.
    """
    return max(0, math.ceil(width_um / scale_um) - 1)


def min_detectable_gap_um(scale_um: float, required_samples: int = 2) -> float:
    """Exclusive lower bound on gap width yielding `required_samples` px.

    Inverting `guaranteed_samples`: ceil(w/s) - 1 >= n holds exactly when
    w > n*s. The bound is open — a gap of width exactly n*s can be placed to
    give only n-1 samples — so this returns the infimum and callers must read
    it as "strictly wider than". One sample is the bare detection floor; two is
    the working rule, because a single isolated background pixel is not
    separable from rasterization noise on a diagonal edge.
    """
    return scale_um * required_samples


class StitchRow(NamedTuple):
    freq_mhz: float
    epsilon_r: float
    lambda0_mm: float
    lambda_g_mm: float
    pitch_free_space_mm: float
    pitch_in_dielectric_mm: float


def stitch_pitch(freq_mhz: float, epsilon_r: float,
                 divisor: float = 20.0) -> StitchRow:
    """lambda/20 via-fence pitch bound, computed both ways on purpose.

    Reporting the free-space value alongside the in-dielectric one is not
    padding: secondary sources quote a lambda/20 figure for FR-4 that equals
    the free-space number, i.e. omits the sqrt(epsilon_r) factor. Keeping both
    columns makes that error visible instead of inheritable.
    """
    lambda0 = C_MM_MHZ / freq_mhz
    lambda_g = lambda0 / math.sqrt(epsilon_r)
    return StitchRow(
        freq_mhz=freq_mhz,
        epsilon_r=epsilon_r,
        lambda0_mm=lambda0,
        lambda_g_mm=lambda_g,
        pitch_free_space_mm=lambda0 / divisor,
        pitch_in_dielectric_mm=lambda_g / divisor,
    )


def knee_frequency_mhz(rise_time_ps: float) -> float:
    """f_knee = 0.35 / t_r. The harmonic content that sets the pitch bound is
    set by edge rate, not by the clock the part is labelled with."""
    return 0.35 / (rise_time_ps * 1e-12) / 1e6


class ArcRow(NamedTuple):
    radius_mm: float
    tolerance_mm: float
    segments: int
    actual_sagitta_um: float


def arc_flattening(radius_mm: float, tolerance_mm: float) -> ArcRow:
    """Segments needed to flatten a full circle within `tolerance_mm` sagitta.

    The chord of an arc lies inside it, so flattening a convex copper edge
    always removes copper and flattening a void always adds it. The error is
    therefore signed, and it biases every gap measurement in the same
    direction rather than averaging out.
    """
    if not 0 < tolerance_mm < radius_mm:
        raise ValueError("tolerance must be positive and below the radius")
    theta_max = 2.0 * math.acos(1.0 - tolerance_mm / radius_mm)
    segments = max(3, math.ceil(2.0 * math.pi / theta_max))
    actual = radius_mm * (1.0 - math.cos(math.pi / segments))
    return ArcRow(radius_mm, tolerance_mm, segments, actual * 1000.0)


# --- reporting -------------------------------------------------------------

BOARD_W_MM = 200.0
BOARD_H_MM = 150.0
COPPER_LAYERS = 8
SCALES_UM: Sequence[float] = (50.0, 25.0, 10.0, 5.0, 2.0, 1.0)
GAPS_UM: Sequence[float] = (25.0, 50.0, 100.0, 200.0)
ARC_CASES = ((0.15, 0.013), (0.15, 0.005), (0.15, 0.001), (1.00, 0.001))


def _table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out.extend("| " + " | ".join(r) + " |" for r in rows)
    return "\n".join(out)


def report() -> str:
    parts = []

    parts.append(
        f"### Raster budget — {BOARD_W_MM:.0f} x {BOARD_H_MM:.0f} mm board, "
        f"{COPPER_LAYERS} copper layers\n")
    rows = []
    for s in SCALES_UM:
        r = raster_budget(BOARD_W_MM, BOARD_H_MM, s, COPPER_LAYERS)
        rows.append([
            f"{r.scale_um:g}", f"{r.px_w} x {r.px_h}", f"{r.megapixels:,.0f}",
            f"{r.mb_1bpp:,.0f}", f"{r.mb_8bpp:,.0f}", f"{r.mb_8bpp_stack:,.0f}",
        ])
    parts.append(_table(
        ["um/px", "pixels", "Mpx/layer", "MB/layer 1bpp", "MB/layer 8bpp",
         "MB stack 8bpp"], rows))

    parts.append("\n### Detectability — worst-case background samples in a gap\n")
    header = ["um/px", "gap for 1 sample (um)", "gap for 2 samples (um)",
              "width error (um)"] + [f"samples in {g:g}um gap" for g in GAPS_UM]
    rows = []
    for s in SCALES_UM:
        rows.append([
            f"{s:g}",
            f">{min_detectable_gap_um(s, 1):g}",
            f">{min_detectable_gap_um(s, 2):g}",
            f"+/-{s:g}",
        ] + [str(guaranteed_samples(g, s)) for g in GAPS_UM])
    parts.append(_table(header, rows))

    parts.append("\n### Via-fence pitch — lambda/20\n")
    rows = []
    for f_mhz, er, label in (
        (1000.0, 4.2, "1 GHz clock"),
        (knee_frequency_mhz(500.0), 4.2, "t_r = 500 ps knee"),
        (knee_frequency_mhz(100.0), 4.2, "t_r = 100 ps knee"),
        (knee_frequency_mhz(35.0), 3.5, "t_r = 35 ps knee, low-loss"),
    ):
        r = stitch_pitch(f_mhz, er)
        rows.append([
            label, f"{r.freq_mhz:,.0f}", f"{r.epsilon_r:g}",
            f"{r.lambda_g_mm:,.1f}", f"{r.pitch_in_dielectric_mm:,.2f}",
            f"{r.pitch_free_space_mm:,.2f}",
        ])
    parts.append(_table(
        ["case", "f (MHz)", "er", "lambda_g (mm)", "pitch lambda_g/20 (mm)",
         "pitch lambda_0/20 (mm) [wrong]"], rows))

    parts.append("\n### Arc flattening — segments per full circle\n")
    rows = []
    for radius, tol in ARC_CASES:
        a = arc_flattening(radius, tol)
        rows.append([
            f"{a.radius_mm:g}", f"{a.tolerance_mm * 1000:g}",
            str(a.segments), f"{a.actual_sagitta_um:.2f}",
        ])
    parts.append(_table(
        ["radius (mm)", "tolerance (um)", "segments", "achieved sagitta (um)"],
        rows))

    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    print(report())
