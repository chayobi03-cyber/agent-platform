"""Minimal ODB++ reader — the subset a shielding inspection needs.

Scope is deliberate. This reads `matrix/matrix`, one step's layer `features`
files, and `eda/data`; it does not attempt the whole format. Everything it does
read is normalised to millimetres at parse time, so no downstream code has to
know what unit the job was written in.

Record syntax is taken from KiCad's ODB++ writer
(`pcbnew/pcb_io/odbpp/odb_feature.cpp`, `odb_eda_data.cpp`), cross-checked
against the regexes in `ulikoehler/ODBPy`:

    UNITS=MM | UNITS=INCH
    $<n> <symbol name>                     symbol table, scoped to THIS file
    L <xs> <ys> <xe> <ye> <sym> <P|N> <dcode> [;attrs]
    A <xs> <ys> <xe> <ye> <xc> <yc> <sym> <P|N> <dcode> <Y|N> [;attrs]
    P <x> <y> <sym> <P|N> <dcode> <orient> [<angle>] [;attrs]
    S <P|N> <dcode> [;attrs]
      OB <x> <y> <I|H> / OS <x> <y> / OC <xe> <ye> <xc> <yc> <Y|N> / OE
    SE

and for `eda/data`:

    LYR <layer> <layer> ...
    NET <name>
    SNT TRC|VIA|PLN ...|TOP ...
    FID <type> <layer index> <feature id>

Two things this reader refuses to do quietly, because both are silent-wrong
failure modes rather than crashes:

* an unknown symbol does not become empty geometry — it is recorded, and the
  feature is marked unresolved so a caller can report the data-quality gap
  instead of reading missing copper as a shield break;
* a missing or unparseable `eda/data` does not fall back to guessing which
  copper is the shield — net attribution simply comes back empty and the
  checks refuse to run.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

MM_PER_INCH = 25.4

# Standard-symbol dimensions are written in thousandths of the file unit:
# microns in an MM file, mils in an INCH file. Verified against two independent
# implementations — KiCad's ODB++ writer scales symbol values by
# 1/PL_IU_PER_MM (1e3) out of nanometre internal units, and delta-odbpp reads
# them with `symbolToMm = features.isMillimeters() ? 0.001 : 0.0254`.
SYMBOL_TO_MM = {"MM": 0.001, "INCH": 0.0254, "IN": 0.0254}

# A standard-symbol dimension below this is almost certainly the other
# convention (a decimal in file units) rather than a real feature: it would be
# a thousandth of its intended size. See Job.warnings.
IMPLAUSIBLE_SYMBOL_MM = 0.005


@dataclass(frozen=True)
class Symbol:
    """A standard ODB++ symbol, dimensions already in mm."""

    name: str
    kind: str                      # round | square | rect | oval | unknown
    dims: Tuple[float, ...] = ()

    @property
    def resolved(self) -> bool:
        return self.kind != "unknown"


@dataclass
class Contour:
    """One polygon of a surface: an island or a hole."""

    kind: str                      # I | H
    start: Tuple[float, float]
    # ("seg", x, y) or ("arc", xe, ye, xc, yc, clockwise)
    steps: List[tuple] = field(default_factory=list)


@dataclass
class Feature:
    index: int
    kind: str                      # L | A | P | S
    polarity: str                  # P | N
    symbol: Optional[Symbol] = None
    start: Optional[Tuple[float, float]] = None
    end: Optional[Tuple[float, float]] = None
    center: Optional[Tuple[float, float]] = None
    clockwise: bool = False
    angle_deg: float = 0.0
    mirror: bool = False
    contours: List[Contour] = field(default_factory=list)

    @property
    def unresolved(self) -> bool:
        return self.symbol is not None and not self.symbol.resolved


@dataclass
class Layer:
    name: str
    layer_type: str = "SIGNAL"
    polarity: str = "POSITIVE"
    row: int = 0
    features: List[Feature] = field(default_factory=list)

    @property
    def negative(self) -> bool:
        return self.polarity.upper().startswith("NEG")


@dataclass
class Job:
    root: Path
    step: str
    profile: List[Feature] = field(default_factory=list)
    layers: Dict[str, Layer] = field(default_factory=dict)
    layer_order: List[str] = field(default_factory=list)
    # (layer name, feature index) -> net name
    feature_net: Dict[Tuple[str, int], str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    @property
    def has_net_attribution(self) -> bool:
        return bool(self.feature_net)

    def net_of(self, layer: str, index: int) -> Optional[str]:
        return self.feature_net.get((layer, index))

    def nets(self) -> List[str]:
        return sorted(set(self.feature_net.values()))


# --- symbols ---------------------------------------------------------------

_ROUND_RE = re.compile(r"^r([\d.]+)$", re.I)
_SQUARE_RE = re.compile(r"^s([\d.]+)$", re.I)
_RECT_RE = re.compile(r"^rect([\d.]+)x([\d.]+)(?:x[rc]?([\d.]+))?$", re.I)
_OVAL_RE = re.compile(r"^oval([\d.]+)x([\d.]+)$", re.I)


def parse_symbol(name: str, to_mm: float) -> Symbol:
    """Parse a standard symbol name. `to_mm` scales the symbol number to mm.

    Pass `SYMBOL_TO_MM[unit]`, not the coordinate scale: symbol dimensions are
    in thousandths of the file unit while coordinates are in the unit itself,
    so `r200` in an MM file is a 0.2 mm round, not a 200 mm one. Reading the
    two with the same factor is a silent 1000x error on every trace width and
    pad, which is exactly what a cross-check against an independent renderer
    caught here.
    """
    n = name.strip()
    m = _ROUND_RE.match(n)
    if m:
        return Symbol(n, "round", (float(m.group(1)) * to_mm,))
    m = _SQUARE_RE.match(n)
    if m:
        return Symbol(n, "square", (float(m.group(1)) * to_mm,))
    m = _RECT_RE.match(n)
    if m:
        corner = float(m.group(3)) * to_mm if m.group(3) else 0.0
        return Symbol(n, "rect", (float(m.group(1)) * to_mm,
                                  float(m.group(2)) * to_mm, corner))
    m = _OVAL_RE.match(n)
    if m:
        return Symbol(n, "oval", (float(m.group(1)) * to_mm,
                                  float(m.group(2)) * to_mm))
    return Symbol(n, "unknown")


# --- feature files ---------------------------------------------------------

def _strip_attrs(line: str) -> str:
    return line.split(";", 1)[0].strip()


def read_features(path: Path, warnings: List[str]) -> List[Feature]:
    """Parse one layer's `features` file into mm-normalised features."""
    to_mm = 1.0
    symbol_to_mm = SYMBOL_TO_MM["MM"]
    symbols: Dict[int, Symbol] = {}
    raw_symbol_names: Dict[int, str] = {}
    features: List[Feature] = []
    surface: Optional[Feature] = None
    contour: Optional[Contour] = None

    def sym(idx_text: str) -> Symbol:
        idx = int(idx_text)
        if idx not in symbols:
            symbols[idx] = Symbol(f"<undefined #{idx}>", "unknown")
            warnings.append(f"{path.name}: feature references undefined symbol {idx}")
        return symbols[idx]

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.upper().startswith("UNITS="):
            unit = line.split("=", 1)[1].strip().upper()
            to_mm = MM_PER_INCH if unit in ("INCH", "IN") else 1.0
            symbol_to_mm = SYMBOL_TO_MM.get(unit, SYMBOL_TO_MM["MM"])
            continue

        if line.startswith("$"):
            head, _, name = line[1:].partition(" ")
            if head.isdigit():
                idx = int(head)
                raw_symbol_names[idx] = name.strip()
                symbols[idx] = parse_symbol(name, symbol_to_mm)
                if not symbols[idx].resolved:
                    warnings.append(
                        f"{path.name}: unsupported symbol '{name.strip()}' "
                        f"(#{idx}) — features using it are unresolved")
                elif 0 < max(symbols[idx].dims or (0.0,)) < IMPLAUSIBLE_SYMBOL_MM:
                    warnings.append(
                        f"{path.name}: symbol '{name.strip()}' resolves to "
                        f"{max(symbols[idx].dims) * 1000:.3f} um — implausibly "
                        f"small; this job may write symbol sizes as decimals in "
                        f"the file unit rather than in thousandths of it")
            continue

        body = _strip_attrs(line)
        if not body:
            continue
        tag = body.split()[0].upper()
        parts = body.split()

        if tag == "L" and len(parts) >= 8:
            features.append(Feature(
                index=len(features), kind="L", polarity=parts[6].upper(),
                symbol=sym(parts[5]),
                start=(float(parts[1]) * to_mm, float(parts[2]) * to_mm),
                end=(float(parts[3]) * to_mm, float(parts[4]) * to_mm)))
        elif tag == "A" and len(parts) >= 11:
            features.append(Feature(
                index=len(features), kind="A", polarity=parts[8].upper(),
                symbol=sym(parts[7]),
                start=(float(parts[1]) * to_mm, float(parts[2]) * to_mm),
                end=(float(parts[3]) * to_mm, float(parts[4]) * to_mm),
                center=(float(parts[5]) * to_mm, float(parts[6]) * to_mm),
                clockwise=parts[10].upper() == "Y"))
        elif tag == "P" and len(parts) >= 6:
            angle, mirror = 0.0, False
            if len(parts) >= 7:
                orient = parts[6]
                if orient in ("8", "9") and len(parts) >= 8:
                    angle = float(parts[7])
                    mirror = orient == "9"
                elif orient.isdigit():
                    angle = 90.0 * (int(orient) % 4)
                    mirror = int(orient) >= 4
            features.append(Feature(
                index=len(features), kind="P", polarity=parts[4].upper(),
                symbol=sym(parts[3]),
                start=(float(parts[1]) * to_mm, float(parts[2]) * to_mm),
                angle_deg=angle, mirror=mirror))
        elif tag == "S" and len(parts) >= 2:
            surface = Feature(index=len(features), kind="S",
                              polarity=parts[1].upper())
        elif tag == "OB" and surface is not None and len(parts) >= 4:
            contour = Contour(kind=parts[3].upper(),
                              start=(float(parts[1]) * to_mm,
                                     float(parts[2]) * to_mm))
        elif tag == "OS" and contour is not None and len(parts) >= 3:
            contour.steps.append(("seg", float(parts[1]) * to_mm,
                                  float(parts[2]) * to_mm))
        elif tag == "OC" and contour is not None and len(parts) >= 6:
            contour.steps.append(("arc", float(parts[1]) * to_mm,
                                  float(parts[2]) * to_mm,
                                  float(parts[3]) * to_mm,
                                  float(parts[4]) * to_mm,
                                  parts[5].upper() == "Y"))
        elif tag == "OE" and contour is not None and surface is not None:
            surface.contours.append(contour)
            contour = None
        elif tag == "SE" and surface is not None:
            features.append(surface)
            surface = None

    if surface is not None:
        warnings.append(f"{path.name}: surface not closed by SE; discarded")
    return features


# --- matrix ----------------------------------------------------------------

def read_matrix(path: Path) -> List[Layer]:
    """Parse `matrix/matrix` LAYER blocks. Order follows the ROW field."""
    layers: List[Layer] = []
    block: Optional[Dict[str, str]] = None
    kind = ""
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("{"):
            kind = line.split("{")[0].strip().upper()
            block = {}
            continue
        if line == "}":
            if kind == "LAYER" and block and "NAME" in block:
                layers.append(Layer(
                    name=block["NAME"],
                    layer_type=block.get("TYPE", "SIGNAL").upper(),
                    polarity=block.get("POLARITY", "POSITIVE").upper(),
                    row=int(block.get("ROW", len(layers) + 1))))
            block, kind = None, ""
            continue
        if block is not None and "=" in line:
            k, _, v = line.partition("=")
            block[k.strip().upper()] = v.strip()
    layers.sort(key=lambda lay: lay.row)
    return layers


# --- eda/data --------------------------------------------------------------

def read_eda_nets(path: Path, warnings: List[str]
                  ) -> Dict[Tuple[str, int], str]:
    """Map (layer name, feature index) -> net name from `eda/data`.

    Returns an empty mapping if the file is missing or carries no FID records.
    An empty mapping is a refusal signal, not a default: without it nothing
    downstream can tell shield copper from any other copper.
    """
    if not path.is_file():
        warnings.append("eda/data missing — no net attribution available")
        return {}

    layer_names: List[str] = []
    mapping: Dict[Tuple[str, int], str] = {}
    net = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        tag = parts[0].upper()
        if tag == "LYR":
            layer_names = parts[1:]
        elif tag == "NET" and len(parts) >= 2:
            net = parts[1]
        elif tag == "FID" and len(parts) >= 4 and net is not None:
            try:
                layer_idx, feature_id = int(parts[2]), int(parts[3])
            except ValueError:
                continue
            if 0 <= layer_idx < len(layer_names):
                mapping[(layer_names[layer_idx], feature_id)] = net
            else:
                warnings.append(
                    f"eda/data: FID names layer index {layer_idx}, "
                    f"outside the {len(layer_names)} layers in LYR")
    if not mapping:
        warnings.append("eda/data carries no FID records — no net attribution")
    return mapping


# --- job -------------------------------------------------------------------

def read_job(root: Path, step: Optional[str] = None,
             layers: Optional[Sequence[str]] = None) -> Job:
    """Read one step of an ODB++ job.

    `step` must be named explicitly unless the job has exactly one: silently
    defaulting is how a panel gets analysed in place of a board.
    """
    root = Path(root)
    steps_dir = root / "steps"
    if not steps_dir.is_dir():
        raise FileNotFoundError(f"not an ODB++ job root (no steps/): {root}")

    available = sorted(p.name for p in steps_dir.iterdir() if p.is_dir())
    if step is None:
        if len(available) != 1:
            raise ValueError(
                f"job has {len(available)} steps {available}; name one explicitly")
        step = available[0]
    elif step not in available:
        raise ValueError(f"step {step!r} not in {available}")

    job = Job(root=root, step=step)
    matrix_path = root / "matrix" / "matrix"
    matrix_layers = read_matrix(matrix_path) if matrix_path.is_file() else []
    if not matrix_layers:
        job.warnings.append(
            "matrix/matrix missing or empty — layer type and polarity unknown")

    step_dir = steps_dir / step
    layers_dir = step_dir / "layers"
    on_disk = sorted(p.name for p in layers_dir.iterdir()
                     if p.is_dir()) if layers_dir.is_dir() else []

    known = {lay.name.lower(): lay for lay in matrix_layers}
    wanted = [n for n in on_disk
              if layers is None or n.lower() in {w.lower() for w in layers}]

    for name in wanted:
        lay = known.get(name.lower()) or Layer(name=name, row=len(job.layers) + 1)
        lay = Layer(name=name, layer_type=lay.layer_type, polarity=lay.polarity,
                    row=lay.row)
        features_path = layers_dir / name / "features"
        if features_path.is_file():
            lay.features = read_features(features_path, job.warnings)
        job.layers[name] = lay
        job.layer_order.append(name)

    job.layer_order.sort(key=lambda n: job.layers[n].row)
    profile_path = step_dir / "profile"
    if profile_path.is_file():
        job.profile = read_features(profile_path, job.warnings)
    else:
        job.warnings.append("steps/<step>/profile missing — no board outline")

    job.feature_net = read_eda_nets(step_dir / "eda" / "data", job.warnings)
    return job


def unresolved_features(job: Job) -> List[Tuple[str, int, str]]:
    """Every feature whose symbol could not be resolved. Non-empty means the
    copper model is incomplete, and missing copper reads as a shield break."""
    out = []
    for name in job.layer_order:
        for feat in job.layers[name].features:
            if feat.unresolved:
                out.append((name, feat.index, feat.symbol.name))
    return out
