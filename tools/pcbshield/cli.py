"""Run the shielding checks over an ODB++ job and write findings + evidence.

    python3 -m pcbshield.cli JOB_DIR --signal SIG --shield GND \
        --signal-layer top --plane-layer l2 --out report/

`--demo` writes a synthetic job with injected defects instead of reading one,
so the pipeline can be exercised without a real design file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .checks import Params, run_all
from .geometry import fold_features
from .odb import read_job
from .render import render_findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pcbshield")
    ap.add_argument("job", nargs="?", help="ODB++ job root (has steps/)")
    ap.add_argument("--step", default=None)
    ap.add_argument("--signal", action="append", default=[])
    ap.add_argument("--shield", action="append", default=[])
    ap.add_argument("--signal-layer", default=None)
    ap.add_argument("--plane-layer", action="append", default=[])
    ap.add_argument("--window-mm", type=float, default=1.0)
    ap.add_argument("--max-gap-mm", type=float, default=1.0)
    ap.add_argument("--clearance-mm", type=float, default=0.15)
    ap.add_argument("--max-via-pitch-mm", type=float, default=7.31)
    ap.add_argument("--arc-tolerance-mm", type=float, default=0.001)
    ap.add_argument("--out", default="pcbshield-report")
    ap.add_argument("--no-images", action="store_true")
    ap.add_argument("--demo", action="store_true",
                    help="generate a synthetic job with injected defects")
    args = ap.parse_args(argv)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.demo:
        from .synth import Defects, build_job
        job_dir = out / "demo-job"
        injected = build_job(job_dir, Defects(
            guard_gap=(8.0, 11.0), plane_void=(3.0, 1.0),
            shield_short=True, floating_island=True))
        args.job = str(job_dir)
        args.signal = args.signal or ["SIG"]
        args.shield = args.shield or ["GND"]
        args.signal_layer = args.signal_layer or "top"
        args.plane_layer = args.plane_layer or ["l2"]
        print(f"demo job at {job_dir} with {len(injected)} injected defects")
    elif not args.job:
        ap.error("a job directory is required unless --demo is given")

    if not args.signal or not args.shield:
        ap.error("--signal and --shield name design intent and are required")

    job = read_job(Path(args.job), args.step)
    signal_layer = args.signal_layer or job.layer_order[0]
    params = Params(signal_nets=args.signal, shield_nets=args.shield,
                    window_mm=args.window_mm, max_gap_mm=args.max_gap_mm,
                    clearance_mm=args.clearance_mm,
                    max_via_pitch_mm=args.max_via_pitch_mm,
                    arc_tolerance_mm=args.arc_tolerance_mm)

    board = fold_features(job.profile, params.arc_tolerance_mm) or None
    if board is not None and board.is_empty:
        board = None

    findings = run_all(job, params, signal_layer, args.plane_layer, board)
    (out / "findings.json").write_text(
        json.dumps([f.as_dict() for f in findings], indent=2), encoding="utf-8")

    images = []
    if not args.no_images:
        images = render_findings(job, findings, params, out / "evidence", board)

    errors = sum(1 for f in findings if f.severity == "error")
    for f in findings:
        print(f"[{f.severity}] {f.check} @({f.x_mm:.3f},{f.y_mm:.3f}) "
              f"{f.message}")
    print(f"\n{len(findings)} findings ({errors} error) -> "
          f"{out / 'findings.json'}; {len(images)} evidence images")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
