"""Synthetic ODB++ jobs with defects injected at known coordinates.

Ground truth is exact because it is constructed: the generator returns what it
injected, so detection rate, localisation error and measured-size error are all
measurable without an oracle.

The honest limit of this fixture, stated up front: the writer and the reader
share assumptions, so a passing run validates the *checks*, not the reader's
fidelity to real CAM output. Only a real job, or a second independent renderer,
tests that. What the fixture does test — and what a real job cannot, because
its defects are unknown — is whether a check finds a defect of known size at a
known place, and whether it stays silent when there is none.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

BOARD_W, BOARD_H = 20.0, 10.0
TRACE_Y = 5.0
GUARD_OFFSET = 0.8
TRACE_X0, TRACE_X1 = 2.0, 18.0
GUARD_CHUNK = 0.25
VIA_PITCH = 1.0
VIA_DIA = 0.6


@dataclass
class Injected:
    """One deliberately created defect, with the truth about it."""

    kind: str
    x_mm: float
    y_mm: float
    size_mm: float
    note: str = ""


@dataclass
class Defects:
    guard_gap: Optional[Tuple[float, float]] = None     # (x_start, x_end), left guard
    plane_void: Optional[Tuple[float, float]] = None    # (x_center, width)
    shield_short: bool = False
    floating_island: bool = False
    via_fence_gap: Optional[Tuple[float, float]] = None  # (x_start, x_end)


class _FeatureFile:
    def __init__(self) -> None:
        self.symbols: List[str] = []
        self.lines: List[str] = []
        self.nets: List[Optional[str]] = []

    def symbol(self, name: str) -> int:
        if name not in self.symbols:
            self.symbols.append(name)
        return self.symbols.index(name)

    def _add(self, text: str, net: Optional[str]) -> int:
        self.lines.append(text)
        self.nets.append(net)
        return len(self.lines) - 1

    # Coordinates are in the file unit (mm here); standard-symbol dimensions
    # are in thousandths of it. Writing both with the same number is the
    # 1000x error an independent renderer caught in the reader.
    def line(self, x0, y0, x1, y1, width_mm, net, polarity="P") -> int:
        s = self.symbol(f"r{width_mm * 1000:g}")
        return self._add(f"L {x0:g} {y0:g} {x1:g} {y1:g} {s} {polarity} 0", net)

    def pad(self, x, y, dia_mm, net, polarity="P") -> int:
        s = self.symbol(f"r{dia_mm * 1000:g}")
        return self._add(f"P {x:g} {y:g} {s} {polarity} 0 8 0", net)

    def rect_surface(self, x0, y0, x1, y1, net, polarity="P",
                     holes: Sequence[Tuple[float, float, float, float]] = ()
                     ) -> int:
        body = [f"S {polarity} 0",
                f"OB {x0:g} {y0:g} I", f"OS {x1:g} {y0:g}",
                f"OS {x1:g} {y1:g}", f"OS {x0:g} {y1:g}",
                f"OS {x0:g} {y0:g}", "OE"]
        for hx0, hy0, hx1, hy1 in holes:
            body += [f"OB {hx0:g} {hy0:g} H", f"OS {hx1:g} {hy0:g}",
                     f"OS {hx1:g} {hy1:g}", f"OS {hx0:g} {hy1:g}",
                     f"OS {hx0:g} {hy0:g}", "OE"]
        body.append("SE")
        return self._add("\n".join(body), net)

    def render(self) -> str:
        out = ["UNITS=MM", "#", "#Num Features", "#", f"F {len(self.lines)}",
               "", "#", "#Feature symbol names", "#"]
        out += [f"${i} {name}" for i, name in enumerate(self.symbols)]
        out += ["", "#", "#Layer features", "#"]
        out += self.lines
        return "\n".join(out) + "\n"


MATRIX = """STEP {{
   COL=1
   NAME=PCB
}}
LAYER {{
   ROW=1
   CONTEXT=BOARD
   TYPE=SIGNAL
   NAME=TOP
   POLARITY=POSITIVE
}}
LAYER {{
   ROW=2
   CONTEXT=BOARD
   TYPE=POWER_GROUND
   NAME=L2
   POLARITY=POSITIVE
}}
LAYER {{
   ROW=3
   CONTEXT=BOARD
   TYPE=DRILL
   NAME=DRILL
   POLARITY=POSITIVE
}}
"""


def _via_positions(defects: Defects) -> List[Tuple[float, float]]:
    """GND stitching vias. A guard break takes its vias with it — a break with
    the fence still standing is not an unshielded run, and pretending otherwise
    would build a fixture that tests nothing."""
    vias: List[Tuple[float, float]] = []
    x = TRACE_X0 + VIA_PITCH / 2
    while x <= TRACE_X1:
        fence_gone = (defects.via_fence_gap is not None
                      and defects.via_fence_gap[0] <= x <= defects.via_fence_gap[1])
        guard_gone = (defects.guard_gap is not None
                      and defects.guard_gap[0] <= x <= defects.guard_gap[1])
        if not fence_gone:
            if not guard_gone:
                vias.append((x, TRACE_Y + GUARD_OFFSET))
            vias.append((x, TRACE_Y - GUARD_OFFSET))
        x += VIA_PITCH
    return vias


# Signal through-holes. These are the features that legitimately produce
# anti-pads in the ground plane, and they are in the fixture so that the S3
# void classifier has something real to classify rather than a plane with no
# expected voids at all.
SIG_HOLES: Tuple[Tuple[float, float], ...] = ((4.5, 5.0), (15.0, 5.0))
SIG_HOLE_ANTIPAD = 0.9


def build_job(root: Path, defects: Optional[Defects] = None
              ) -> List[Injected]:
    """Write a job under `root`; return the defects actually injected."""
    defects = defects or Defects()
    root = Path(root)
    injected: List[Injected] = []

    top = _FeatureFile()
    top.line(TRACE_X0, TRACE_Y, TRACE_X1, TRACE_Y, 0.2, "SIG")

    for side, y in (("left", TRACE_Y + GUARD_OFFSET),
                    ("right", TRACE_Y - GUARD_OFFSET)):
        x = TRACE_X0
        while x < TRACE_X1 - 1e-9:
            x_next = min(x + GUARD_CHUNK, TRACE_X1)
            removed = (side == "left" and defects.guard_gap is not None
                       and defects.guard_gap[0] <= x < defects.guard_gap[1])
            if not removed:
                top.line(x, y, x_next, y, 0.3, "GND")
            x = x_next

    if defects.guard_gap is not None:
        gx0, gx1 = defects.guard_gap
        injected.append(Injected("guard_gap", (gx0 + gx1) / 2,
                                 TRACE_Y + GUARD_OFFSET, gx1 - gx0,
                                 "left guard removed"))

    vias = _via_positions(defects)
    for vx, vy in vias:
        top.pad(vx, vy, VIA_DIA, "GND")
    if defects.via_fence_gap is not None:
        vx0, vx1 = defects.via_fence_gap
        injected.append(Injected("via_fence_gap", (vx0 + vx1) / 2,
                                 TRACE_Y + GUARD_OFFSET, vx1 - vx0,
                                 "stitching vias removed"))

    if defects.shield_short:
        top.line(10.0, TRACE_Y + GUARD_OFFSET, 10.0, TRACE_Y, 0.3, "GND")
        injected.append(Injected("shield_short", 10.0, TRACE_Y + 0.4, 0.3,
                                 "guard stub touching the signal"))

    if defects.floating_island:
        top.rect_surface(1.0, 8.5, 3.0, 9.5, "GND")
        injected.append(Injected("floating_island", 2.0, 9.0, 2.0,
                                 "GND pour with no via"))

    for hx, hy in SIG_HOLES:
        top.pad(hx, hy, 0.6, "SIG")

    plane = _FeatureFile()
    # GND stitching vias land in GND copper, so they connect directly and get
    # no anti-pad. Only the signal through-holes clear the plane.
    r = SIG_HOLE_ANTIPAD
    antipads = [(hx - r, hy - r, hx + r, hy + r) for hx, hy in SIG_HOLES]
    void = []
    if defects.plane_void is not None:
        cx, w = defects.plane_void
        void = [(cx - w / 2, TRACE_Y - w / 2, cx + w / 2, TRACE_Y + w / 2)]
        injected.append(Injected("plane_void", cx, TRACE_Y, w,
                                 "reference plane cut under the signal"))
    plane.rect_surface(0.5, 0.5, BOARD_W - 0.5, BOARD_H - 0.5, "GND",
                       holes=antipads + void)

    drill = _FeatureFile()
    for vx, vy in vias:
        drill.pad(vx, vy, 0.3, "GND")
    for hx, hy in SIG_HOLES:
        drill.pad(hx, hy, 0.4, "SIG")

    layers = {"top": top, "l2": plane, "drill": drill}
    step = root / "steps" / "pcb"
    for name, ff in layers.items():
        d = step / "layers" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "features").write_text(ff.render(), encoding="utf-8")

    (root / "matrix").mkdir(parents=True, exist_ok=True)
    (root / "matrix" / "matrix").write_text(MATRIX.format(), encoding="utf-8")

    # misc/info carries the job-level UNITS directive. It is required, and
    # omitting it made an independent renderer fall back to inches.
    (root / "misc").mkdir(parents=True, exist_ok=True)
    (root / "misc" / "info").write_text(
        "JOB_NAME=pcbshield-synth\nUNITS=MM\nODB_VERSION_MAJOR=8\n"
        "ODB_VERSION_MINOR=1\nODB_SOURCE=pcbshield.synth\n", encoding="utf-8")

    order = ["top", "l2", "drill"]
    eda = ["# synthetic", "HDR pcbshield synth", "UNITS=MM",
           "LYR " + " ".join(order)]
    by_net: Dict[str, List[Tuple[int, int]]] = {}
    for li, name in enumerate(order):
        for fi, net in enumerate(layers[name].nets):
            if net:
                by_net.setdefault(net, []).append((li, fi))
    for net in sorted(by_net):
        eda.append(f"NET {net}")
        eda.append("SNT TRC")
        for li, fi in by_net[net]:
            eda.append(f"FID C {li} {fi}")
    (step / "eda").mkdir(parents=True, exist_ok=True)
    (step / "eda" / "data").write_text("\n".join(eda) + "\n", encoding="utf-8")

    profile = _FeatureFile()
    profile.rect_surface(0.0, 0.0, BOARD_W, BOARD_H, None)
    (step / "profile").write_text(profile.render(), encoding="utf-8")

    return injected
