# PCB / ODB++ Shielding Inspection — Methodology Research

**Status:** RAW_FINDING → ASSET_CANDIDATE. Research only.
**Evidence class:** EXTERNAL_EVIDENCE, plus one local reproducible computation.
**Date:** 2026-09-03
**Question investigated:** capture an ODB++ job at real-viewer fidelity in order to
inspect a signal's shielding for breaks and for overlap.

This document proposes a method. It is not an APF rule, not an accepted asset, and
not an implementation authorization. Section 12 lists what a human still has to
decide.

---

## 1. The request, restated precisely

The request as given contains one instruction and two defect classes:

- *capture at real-viewer fidelity* — render the ODB++ job in as much detail as a
  commercial ODB++ viewer shows;
- *find where the shielding is broken* (터진 부분) — the shield is absent where it
  was meant to be continuous;
- *find overlap* (오버랩) — two things occupy the same area.

"Broken" and "overlap" are each ambiguous, and the ambiguity is not cosmetic: it
changes which layers are read, which geometry operation runs, and what counts as a
pass. Before any tooling decision, the terms have to be split.

**Break** resolves into three physically distinct defects:

| # | Break class | Where it lives |
|---|---|---|
| B1 | Coplanar guard discontinuity | shield trace/pour beside the signal, same layer |
| B2 | Via-fence pitch violation | stitching vias along the guard; copper is continuous but the fence is not electrically continuous at frequency |
| B3 | Reference-plane discontinuity | void, split or anti-pad field in the plane above/below the signal |

**Overlap** resolves into four:

| # | Overlap class | Where it lives |
|---|---|---|
| V1 | Shield-to-foreign-net overlap | shield copper intersects another net on the same layer — a short or a clearance violation |
| V2 | Shield-domain overlap | two shield domains (e.g. AGND/DGND) intersect where they were meant to be separate |
| V3 | Inter-layer shield coverage | shield on layer *i* vs shield on layer *j*: how much of the intended enclosure actually overlaps |
| V4 | Signal-over-opening overlap | the signal's footprint overlaps an opening in the shield — the same event as B3, expressed as an area rather than as a gap |

A single "check the shielding" pass that does not distinguish these produces
findings that cannot be triaged. **Recommendation: implement six named checks
(§7), not one.**

---

## 2. Evidence base, and its limits

| Source | Type | Used for | Reachable |
|---|---|---|---|
| ODB++ Design Format Specification (Siemens, rel. 8.1 u4) | primary | record syntax, symbols, surfaces | **No** — `odbplusplus.com` is refused by this session's egress policy (HTTP 403) |
| `ulikoehler/ODBPy` source | independent implementation | surface/polygon/unit record syntax, verified by reading the parsing regexes | Yes |
| `sjgallagher2/ODBplusplus-Parser` documentation | independent implementation | feature model, symbol semantics, EDA-data-to-net mapping, matrix contents | Yes |
| `nam20485/OdbDesign` | independent implementation | evidence that full-archive parsing is a solved problem in C++ (AGPL-3.0) | Yes |
| Vendor material on HyperLynx DRC, Allegro, Valor NPI | secondary | prior art: which checks commercial tools consider necessary | Yes |
| EMI/stitching design guidance | secondary | λ/20 pitch rule — **and one propagated error, see §11** | Yes |
| `tools/research/pcb_shield_budget.py` | local computation | every number in §5 and §8 | n/a |

**Limitation to carry forward:** the normative specification could not be read in
this session. Everything stated about the ODB++ file format below is inferred from
two independent implementations that agree with each other. Agreement between two
implementations is weaker evidence than the specification, and both were written
against ODB++ v7/v8.1 and both document gaps (barcode/text unhandled, blind/buried
vias assumed thru-hole in one of them). **Any adoption decision should re-verify
§3 against the specification from a network where it is reachable.**

---

## 3. The data model the method depends on

An ODB++ job is a directory tree, not an image. The parts that matter here:

```text
<job>/matrix/matrix                              layer list, layer TYPE, layer POLARITY, step list
<job>/misc/info, misc/attrlist                   job-level attributes (.board_thickness)
<job>/steps/<step>/profile                       board outline
<job>/steps/<step>/layers/<layer>/features       the geometry
<job>/steps/<step>/layers/<layer>/attrlist       .copper_weight, .layer_dielectric,
                                                 .dielectric_constant, .z0impedance
<job>/steps/<step>/eda/data                      feature -> net and subnet mapping
<job>/steps/<step>/netlists/cadnet/netlist       netlist points (when present)
```

Five properties of this model decide the whole method:

**3.1 Features are drawing operations, not shapes.** A `feature` is one of line,
arc, pad, surface, text, barcode. Lines and arcs carry a *symbol* used as a
paintbrush along a path — the symbol supplies width, cap and join. Pads are a
symbol placed with position, orientation and a resize factor. Only surfaces are
polygons outright. Copper is therefore *derived*, not stored: it is the result of
stroking and stamping, which is exactly what a viewer does when it draws.

**3.2 The symbol dictionary is per feature file.** There is no job-wide symbol
table; symbol numbers are meaningful only within one layer's `features` file. Any
renderer or extractor that hoists a symbol table above layer scope is wrong.

**3.3 Polarity applies twice, and both are inverting.** The matrix marks a layer
POSITIVE or NEGATIVE; individual features carry `P` or `N`. Surfaces open with
`S <P|N> <dcode>` and close with `SE`; their contours are `OB x y <I|H>` (island
or hole), `OS x y`, `OC xe ye xc yc <Y|N>` (arc, clockwise flag), `OE`. Negative
features subtract from copper already painted, so **feature order is semantic** —
copper is a fold over the feature list in file order, not a set union. Plane
layers are commonly stored negative, i.e. the features *are* the voids. Getting
polarity wrong does not degrade a shielding check; it inverts it, and an inverted
check reports the copper as the gap and passes silently.

**3.4 Nets come from `eda/data`, and this is the load-bearing fact.** Features are
mapped to nets and to a subnet kind: *toeprint*, *trace*, *via*, *plane*. This is
what lets a checker say "this copper is the shield" instead of guessing from
colour or position. A feature absent from `eda/data` is non-physical (drawing,
text); a floating physical feature appears under `$NONE$`. **A pixel capture
discards all of this.** It is the single strongest argument against an image-first
method: an image cannot distinguish a ground pour from an unrelated copper flood,
and the entire question being asked is about *which net's* copper is where.

**3.5 Units are mixed by design.** The `U` record gives the file unit (`MM`,
`IN`); symbol parameters are frequently in mil or µm. Unit normalisation belongs
at the parse boundary, once, or it becomes a silent 25.4× error somewhere
downstream.

---

## 4. Why "capture, then inspect" is the wrong order

The request names capture first. Taken literally — screenshot a viewer, then look
for gaps — the method fails for four independent reasons, any one of which is
sufficient:

1. **It throws away the net attribution** that defines the question (§3.4).
2. **It cannot resolve the defects** at any capture size a viewer produces (§5).
3. **It cannot see electrical islanding.** A shield can be geometrically perfect
   and electrically floating — a pour whose only stitching via was deleted. Every
   pixel is in the right place; the shield does not work. Only connectivity
   analysis finds this, and it is arguably the most dangerous defect in the set
   because visual review actively passes it.
4. **It is not reproducible.** Viewer output depends on zoom, layer colour and
   blend order, and anti-aliasing; a finding cannot be tied back to board
   coordinates.

This does not make capture useless. It relocates it. Capture has two roles the
vector path cannot fill, and both are valuable:

- **Evidence.** A finding is a coordinate; a human needs a picture of it. Render
  the picture *from* the finding.
- **Parser self-validation.** Render the board from your own extracted geometry
  and, independently, from a second renderer; XOR the two rasters. Non-zero XOR
  is a parse gap — an unhandled symbol, a missed negative feature, a mis-scaled
  user symbol. This turns "capture at viewer fidelity" into a falsification test
  for the extraction, which is the most useful thing it can be.

**Finding: capture is necessary, but as validation and as evidence — not as the
measurement substrate.**

---

## 5. The resolution budget that settles it

From `tools/research/pcb_shield_budget.py` (200 × 150 mm board, 8 copper layers).
A pixel grid samples on a lattice of pitch *s* at an arbitrary phase; a gap of
width *w* is guaranteed to contain at least `ceil(w/s) − 1` background samples.
Worst case, not average, is the right figure: the defect does not choose its phase.

| µm/px | pixels/layer | Mpx/layer | MB/layer 1bpp | MB stack 8bpp | guaranteed samples in a 25 µm gap | in a 50 µm gap | in a 100 µm gap |
|---|---|---|---|---|---|---|---|
| 50 | 4000 × 3000 | 12 | 1 | 92 | **0** | **0** | 1 |
| 25 | 8000 × 6000 | 48 | 6 | 366 | **0** | 1 | 3 |
| 10 | 20000 × 15000 | 300 | 36 | 2,289 | 2 | 4 | 9 |
| 5 | 40000 × 30000 | 1,200 | 143 | 9,155 | 4 | 9 | 19 |
| 2 | 100000 × 75000 | 7,500 | 894 | 57,220 | 12 | 24 | 49 |
| 1 | 200000 × 150000 | 30,000 | 3,576 | 228,882 | 24 | 49 | 99 |

Read across the two halves of that table:

- A whole-board capture that is cheap (≤ 25 µm/px, ≤ 366 MB for the stack) is
  **blind to a 25 µm gap and marginal on a 50 µm gap** — one guaranteed pixel is
  not separable from rasterization noise on a diagonal edge.
- A capture that can *measure* a 50 µm gap to ±5 µm costs **9 GB per board for
  the copper stack**, before any per-net or intermediate images.
- Measured width carries ±s quantization error at every scale. Vector geometry
  carries none.

Industry practice agrees with the cost side: commercial photoplot rasterizers
operate at 0.25–5 µm pixels over 500 × 600 mm panels — full-fidelity raster of a
whole panel is an established but heavyweight, purpose-built operation, not
something to do casually per inspection run.

**Consequence:** full-board raster is viable for *screening* and for *pictures*,
not for *verdicts*. Vector geometry gives exact answers at a fraction of the cost
and is where the verdict must be computed.

---

## 6. Three candidate methods

| | A — Capture-first | B — Vector-exact | C — Vector verdict + rendered evidence |
|---|---|---|---|
| Substrate | rasterized layers | polygons from parsed features | polygons; raster derived |
| Net awareness | none | full (`eda/data`) | full |
| Smallest reliable defect | 2–3 × pixel pitch | exact | exact |
| Whole-board cost | 0.4–9 GB (§5) | proportional to feature count | vector cost + a few MB of tiles |
| Finds floating shield | no | yes | yes |
| Human-reviewable output | yes | no | yes |
| Depends on parse completeness | no | **yes** | yes, but measurable (§4, XOR) |
| Effort | low | medium | medium-high |

Method A's one real virtue is that it is representation-agnostic: it still shows
copper that the parser failed to understand. That virtue is preserved in C by
using the raster as a cross-check rather than as the substrate.

**Recommendation (not a decision): method C.**

```text
ODB++ job
  → parse (features, matrix, eda/data, drills, stackup)
  → normalize units, resolve symbols, flatten arcs (bounded, §9)
  → fold features in file order honouring polarity  → copper polygons per layer
  → attach net + subnet from eda/data               → net-resolved geometry
  → build stack adjacency from matrix + attrlist
  ├─ CHECKS S1..S6 (§7), computed in vector space   → findings with coordinates
  ├─ renderer XOR self-validation (§4)              → parse-gap report
  └─ evidence renderer, driven by each finding (§8) → viewer-fidelity crops
```

---

## 7. The check catalogue

Notation: `Cu[L]` copper on layer L; `Net[n]` the geometry of net n; `Shield` the
designated shield net(s), typically GND; `Sig` the signal under inspection;
`⊖`/`⊕` erosion/dilation (negative/positive buffer).

**S1 — coplanar guard continuity (B1).** Build `corridor = Sig ⊕ W` for a window
W (a few line widths, or a stated multiple of dielectric height). Intersect with
`Shield` on the same layer, then project the result onto the signal's arc-length
parameter. The complement of that 1-D coverage is the set of gaps, each with a
start, end and length along the trace. Report runs exceeding `L_max`. Reducing
the problem to 1-D intervals is what keeps it exact and cheap; it also yields the
natural report unit — "unshielded from 12.4 mm to 19.1 mm along net X" — rather
than an area.

**S2 — via-fence pitch (B2).** Select `Shield` vias within W of the trace,
project their centres onto the same arc-length axis, sort, and take consecutive
differences. Flag any Δ above the λ/20 bound. The bound is not a constant: it is
`λ_g/20 = c / (20 · f · √ε_r)` with `f` the knee frequency `0.35/t_r`, and `ε_r`
read from the layer `attrlist` where present. §11 records a propagated error in
the secondary literature on exactly this formula.

**S3 — reference-plane continuity (B3).** From the matrix and stackup, find the
plane layer(s) adjacent to the signal's layer. Compute
`hole = (Sig ⊕ m) − Net[gnd]@plane` with margin `m`. Non-empty components are
return-path discontinuities. **Classify before reporting:** anti-pads that
coincide with a drill and its pad are expected geometry, and an unclassified void
detector drowns in them. This check is the open-source equivalent of Allegro's
"segments over void" and HyperLynx DRC's split-crossing rule; both exist as prior
art, which is evidence the check is worth having and that its false-positive
problem is real.

**S4 — shield/foreign-net overlap and clearance (V1).** `Shield ∩ Net[other]`
must be empty; non-empty area is a short. Clearance is the same test on
`Shield ⊕ c`. Cheap, exact, and the check most likely to catch a genuine error
early.

**S5 — inter-layer shield coverage (V2, V3).** For an intended enclosure across
layers *i*, *j*: `coverage = area(Shield[i] ∩ Shield[j]) / area(Shield[i])`, and
`Shield_domainA ∩ Shield_domainB` for domain separation. Also the broadside case:
signal on *i* against openings in the shield on *j*, which is V4 and reuses S3's
geometry with the area rather than the gap as the reported quantity.

**S6 — shield electrical connectivity.** Build a graph: nodes are connected
components of shield copper per layer, edges are vias joining them. Any component
not connected to the main shield component is a floating shield. This check has no
visual equivalent (§4.3) and should not be deferred; it is cheap once the geometry
exists.

S1–S5 are geometry; S6 is topology. All six consume the same net-resolved model,
which is why the model, not the checks, is the thing to get right first.

---

## 8. The capture specification

Capture is still required — for evidence and for §4's XOR validation. To be
useful it must be *deterministic*, which a viewer screenshot is not.

- **Fixed, invertible transform.** `px = round((x − x₀)/s)` with `s` in µm/px
  recorded in the image sidecar. Every pixel maps back to board coordinates.
- **No anti-aliasing on analysis rasters.** AA makes an edge pixel a fraction, and
  a fractional edge silently changes a morphological gap measurement. Analysis
  rasters are 1-bit per layer per polarity. The human-facing composite is a
  separate, anti-aliased, colour-mapped image — never the same file.
- **Net-driven colouring** on evidence images: signal, shield, other copper, and
  void each get a fixed role colour, so a reviewer sees the *semantic* content the
  capture would otherwise have discarded.
- **Findings drive crops, not the reverse.** Each finding carries (layer, x, y,
  extent); the renderer picks `s` so the defect spans ≥ 100 px, and burns in a
  scale bar, coordinates, net name and finding id. This is what makes a capture
  "viewer-level" in the sense that matters: it shows the defect at a size a human
  can judge, with the evidence of *where* it is.
- **Tiling with overlap** (e.g. 2048² tiles, overlap ≥ the largest structuring
  element) for any whole-board raster, so morphology near tile borders is correct.
  A deep-zoom pyramid over those tiles gives interactive review without ever
  materialising the full image.

---

## 9. Failure modes

| # | Failure mode | Effect | Mitigation |
|---|---|---|---|
| F1 | Layer or feature polarity mishandled (§3.3) | **Findings inverted**; check passes on a broken board | Assert copper area against an independent render; test on a known-negative plane layer |
| F2 | Features unioned instead of folded in order | Negative features lost; voids disappear | Fold in file order; make it a parser invariant |
| F3 | Anti-pads and thermal reliefs reported as plane voids | False positives swamp real findings | Classify voids against drill + pad geometry before reporting (S3) |
| F4 | Arc flattening tolerance inherited from CAD defaults | Systematic bias of the same order as the defect | See below |
| F5 | `eda/data` absent or nets `$NONE$` | Shield cannot be identified; method degrades to guessing | Detect and refuse rather than fall back to heuristics |
| F6 | Wrong step analysed (panel vs board) | Repeated geometry, meaningless coordinates | Resolve step explicitly; never default silently |
| F7 | Self-intersecting polygons (a named case in the spec) | Boolean results undefined | Repair with a recorded, deterministic rule; count repairs as a data-quality metric |
| F8 | Unsupported symbol silently skipped | Missing copper reads as a gap | §4 XOR validation catches exactly this |
| F9 | Plane-sized polygons in naive boolean loops | Runtime blows up | Spatial index; process per tile/region; integer-coordinate clipping |

**On F4, with numbers.** Flattening a full circle within a sagitta tolerance needs
`N = ⌈2π / (2·arccos(1 − ε/R))⌉` segments:

| radius | tolerance | segments | achieved sagitta |
|---|---|---|---|
| 0.15 mm | 13 µm (a common CAD default) | 8 | **11.4 µm** |
| 0.15 mm | 5 µm | 13 | 4.4 µm |
| 0.15 mm | 1 µm | 28 | 0.9 µm |
| 1.00 mm | 1 µm | 71 | 1.0 µm |

An 11 µm edge error is the same order as a 25 µm defect. Worse, the error is
*signed*: a chord lies inside its arc, so flattening shrinks convex copper and
enlarges voids — every gap measurement is biased wide and every overlap biased
small, in the direction that produces false passes on overlap and false alarms on
gaps. **Flattening tolerance must be an explicit analysis parameter (suggest ≤ 1/10
of the smallest reported defect), and the conservative form is to flatten copper
circumscribed and voids inscribed, or to run both and report the bracket.**

**On F9,** integer-coordinate clipping (Clipper2-style, ±1 unit bounded error) is
the better fit for this workload than floating-point predicates, because PCB data
is natively on a fine integer grid and the error stays constant rather than
scaling with coordinate magnitude.

---

## 10. Validating the method itself

A checker that has never been shown to find a defect it did not already know about
is an opinion. The validation plan below is falsifiable and should be predeclared
before it is run.

1. **Injected-defect corpus.** Take a real ODB++ job and programmatically inject
   defects of known class, position and size — a 40 µm guard break at a stated
   coordinate, a via removed from a fence, a plane void widened by a stated
   amount. Ground truth is exact because it was constructed.
   Primary measures, all declared in advance: detection rate per defect class per
   size bucket; localisation error; measured-size error against injected size.
2. **Null control.** The same boards with no injection. A checker that flags
   everything scores 100% recall; the false-positive rate on clean boards is the
   measure that stops that, and F3 predicts this is where the method will fail
   first.
3. **Renderer fidelity.** XOR the pipeline's own raster against an independent
   renderer over the whole board; report disagreeing area as a fraction. This is
   the test that "viewer-level capture" was actually achieved, stated as a number
   instead of an impression.
4. **Cross-tool agreement.** Where a commercial tool is licensed, run its
   equivalent check on the same board and build an agreement matrix. Disagreements
   are the interesting rows, in both directions.
5. **Declared falsifier.** The method should be considered falsified at tested
   scope if detection rate on injected defects at or above the declared minimum
   size is below the predeclared threshold, or if the clean-board false-positive
   rate exceeds the level at which a human would stop reading the report.

Measure 2 and measure 5 are the ones that make this a falsification test rather
than a demonstration.

---

## 11. Contradictions recorded

**C1 — a λ/20 figure in circulation omits the dielectric.** Secondary EMI guidance
quotes, for a 1 GHz signal, a via-fence pitch of "around 15 mm in FR-4". Computing
it: `λ₀ = 299792.458/1000 = 299.79 mm`, so `λ₀/20 = 14.99 mm` — the quoted figure
is the **free-space** value. In FR-4 with `ε_r = 4.2`, `λ_g = 146.3 mm` and
`λ_g/20 = 7.31 mm`. The circulating number is therefore roughly **2× too
permissive**, and a fence built to it fails the rule it claims to satisfy. The
calculator prints both columns side by side so the error cannot be inherited
silently. Note also that `ε_r` is the wrong symbol for a microstrip, where the
effective permittivity is lower than the bulk value and the correct pitch sits
between the two columns — the direction of that correction is toward the free-space
number, but it does not reach it.

**C2 — "the spec is freely available" versus this session.** One source notes that
ODB++, unlike IPC-2581, is freely published. That is true of the format and false
of this session: the egress policy refuses the host (§2). The method's dependence
on unverified format details is therefore a real, current risk, not a hypothetical
one.

**C3 — prior art both supports and limits the plan.** Allegro's "segments over
void" and HyperLynx DRC's split-crossing and reference-plane-change rules show the
checks are worth building. They also show that vendors with far more resources
ship these as *netlist-driven vector* checks, not as image analysis — which
corroborates §4 — and that the checks are valuable enough to be a competitive
feature, which is weak evidence that the false-positive problem (F3) is harder than
it looks.

---

## 12. What is undecided, and belongs to a human

1. **Scope.** Is this a one-off inspection of one board, or a repeatable APF work
   type? The answer changes everything downstream; a one-off justifies method A
   plus manual review, a repeatable one does not.
2. **Which shield definition governs.** Which nets are shields, which are domains
   that must not touch, and what `L_max`, `W`, `m` and `c` are for this design.
   These are design intent and cannot be derived from the ODB++ file.
3. **Licence boundary.** `OdbDesign` is AGPL-3.0. Adopting it as a parser has
   distribution consequences; writing a parser instead has cost consequences.
4. **Whether to depend on an unverified format reading** (§2, C2) or to obtain the
   specification first.
5. **Whether this domain becomes an APF test case.** `docs/handoff/SESSION_STATE.md` records that
   every benchmark so far has run against APF's own governance corpus, and that an
   independent engineering domain is required before generalising. A PCB inspection
   workflow is such a domain — work, opportunity, automation decision, execution,
   evidence, outcome, all present and externally grounded. That makes it a
   candidate probe for the work-centric abstraction claim. It is a candidate only;
   registering it as a benchmark is a governed act and is not performed here.

---

## 13. Recommendation

Not a decision. For human review:

- Adopt **method C** — vector-exact verdicts, rendered evidence, XOR self-validation.
- Implement the model before the checks: parse → unit normalisation → polarity-ordered
  fold → net attribution. Five of the nine failure modes in §9 live in that stage.
- Implement **S4 and S6 first**. They are the cheapest, they are exact, and S6
  finds the defect that no capture-based method can find at all.
- Treat **S3 as the hard one** and do not ship it before the void classifier (F3).
- Fix the arc-flattening tolerance explicitly and record it with every result.
- Predeclare §10 before running it, including the falsifier.

## 14. Asset candidates arising

Registered in `docs/research/ASSET_LEDGER.md`:

- `ASSET-0001` — ODB++ as a net-resolved geometry source
- `ASSET-0002` — vector-verdict / rendered-evidence inspection pattern
- `ASSET-0003` — injected-defect validation pattern for geometric checkers

Each is `ASSET_CANDIDATE`. None is accepted.
