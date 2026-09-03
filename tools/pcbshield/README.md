# pcbshield — ODB++ signal-shielding checks

A working vertical slice of the method proposed in
`docs/research/PCB_ODB_SHIELDING_INSPECTION_METHODOLOGY.md`: verdicts computed
in exact geometry, evidence rendered from the verdicts.

```bash
pip install -r tools/pcbshield/requirements.txt

# exercise the whole pipeline on a generated job with injected defects
cd tools && python3 -m pcbshield.cli --demo --out /tmp/report

# a real job
cd tools && python3 -m pcbshield.cli /path/to/odb_job \
    --signal DDR_CLK --shield GND \
    --signal-layer top --plane-layer l2 \
    --window-mm 1.0 --max-gap-mm 1.0 --max-via-pitch-mm 7.31 \
    --out /tmp/report
```

Output is `findings.json` — every finding carries board coordinates — and one
PNG per finding under `evidence/`, rendered at a pixel pitch chosen so the
defect spans at least 120 px, with a scale bar and the coordinates burnt in.

## Checks

| id | defect | notes |
|---|---|---|
| S1 | coplanar guard break | 1-D coverage along the trace, per side; quantized by `station_pitch_mm`, which every finding reports |
| S2 | stitching via pitch | λ_g/20; the bound comes from `tools/research/pcb_shield_budget.py`, not from a constant |
| S3 | reference-plane void under the signal | anti-pads classified out; voids merged with an anti-pad are reported, not swallowed |
| S4 | shield touching or crowding another net | intersection area, then clearance |
| S6 | shield island with no via path | the defect no image-based method can find |
| Q1–Q3 | data quality | no net attribution, unresolved symbol, reader warning |

`Params` carries design intent — which nets are shields, how far a guard may
sit, what pitch is allowed. None of it is derivable from the job file, so none
of it is guessed: the CLI requires `--signal` and `--shield`.

## What it does not do

- **Text, barcode, and user-defined symbols** are not built. Unresolved symbols
  become `Q2` findings rather than missing copper, because missing copper reads
  as a shield break.
- **Blind and buried vias** are not distinguished; every drill is treated as
  through-hole, so S6 can call two layers connected that a real stackup does
  not connect.
- **Step-and-repeat** is not expanded. The step must be named when a job has
  more than one; the reader refuses instead of defaulting.
- **Negative matrix polarity** is handled only when a board outline is
  available, and raises otherwise rather than guessing.
- **No renderer XOR cross-check yet.** `mcix/odbpp` (Java, AGPL) renders ODB++
  independently and is the obvious second implementation to difference against;
  until that runs, the geometry model is unvalidated against anything but
  itself.

## Validating it

`tools/tests/test_pcbshield.py` builds jobs with defects injected at known
coordinates and sizes, and asserts both halves: that each defect is found and
located, and that a clean board produces nothing. The null control is the half
that matters — a checker that flags everything scores perfect recall.

The honest limit: the fixture's writer and the reader share assumptions, so a
passing run validates the checks, not the reader's fidelity to real CAM output.
Record syntax was taken from KiCad's ODB++ writer and cross-checked against
`ulikoehler/ODBPy`, but only a real job settles it.
