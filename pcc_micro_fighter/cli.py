from __future__ import annotations
import argparse, json
from .engine import simulate_match
from .experiment import write_sweep
from .competitiveness import write_competitiveness
from .pressure_decomposition import write_pressure_decomposition
from .threat_conversion import write_threat_conversion
from .control_counter_intervention import write_control_counter_intervention
from .residual_pressure import write_residual_pressure
from .control_recovery_intervention import write_control_recovery_intervention
from .observables import summarize
from .policies import POLICIES


def main() -> int:
    p = argparse.ArgumentParser(prog="pcc-micro-fighter")
    sub = p.add_subparsers(dest="cmd", required=True)
    sim = sub.add_parser("simulate")
    sim.add_argument("--p0", choices=POLICIES, default="pressure")
    sim.add_argument("--p1", choices=POLICIES, default="control")
    sim.add_argument("--seed", type=int, default=1)
    sweep = sub.add_parser("sweep")
    sweep.add_argument("--matches-per-order", type=int, default=100)
    sweep.add_argument("--seed", type=int, default=1000)
    sweep.add_argument("--output", default="validation/pairwise-sweep.json")
    balance = sub.add_parser("competitiveness")
    balance.add_argument("--matches-per-order", type=int, default=400)
    balance.add_argument("--seed", type=int, default=42001)
    balance.add_argument("--output", default="validation/competitiveness.json")
    decomp = sub.add_parser("pressure-decomposition")
    decomp.add_argument("--matches-per-order", type=int, default=300)
    decomp.add_argument("--seed", type=int, default=53001)
    decomp.add_argument("--output", default="validation/pressure-dominance-decomposition.json")
    conversion = sub.add_parser("threat-conversion")
    conversion.add_argument("--matches-per-order", type=int, default=400)
    conversion.add_argument("--seed", type=int, default=64001)
    conversion.add_argument("--output", default="validation/threat-conversion-decomposition.json")
    intervention = sub.add_parser("control-counter-intervention")
    intervention.add_argument("--matches-per-order", type=int, default=400)
    intervention.add_argument("--seed", type=int, default=42001)
    intervention.add_argument("--output", default="validation/control-counter-intervention-v0.5.0.json")
    recovery = sub.add_parser("control-recovery-intervention")
    recovery.add_argument("--matches-per-order", type=int, default=400)
    recovery.add_argument("--seed", type=int, default=42001)
    recovery.add_argument("--output", default="validation/control-recovery-intervention-v0.7.0.json")
    residual = sub.add_parser("residual-pressure")
    residual.add_argument("--matches-per-order", type=int, default=400)
    residual.add_argument("--seed", type=int, default=75001)
    residual.add_argument("--output", default="validation/residual-pressure-decomposition.json")
    args = p.parse_args()
    if args.cmd == "simulate":
        r = simulate_match(POLICIES[args.p0](), POLICIES[args.p1](), args.seed)
        print(json.dumps({"winner": r.winner, "ticks": r.ticks, "health": r.health, "p0": summarize(r,0), "p1": summarize(r,1)}, indent=2))
        return 0
    if args.cmd == "control-recovery-intervention":
        report = write_control_recovery_intervention(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    if args.cmd == "residual-pressure":
        report = write_residual_pressure(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    if args.cmd == "control-counter-intervention":
        report = write_control_counter_intervention(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    if args.cmd == "threat-conversion":
        report = write_threat_conversion(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    if args.cmd == "pressure-decomposition":
        report = write_pressure_decomposition(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    if args.cmd == "competitiveness":
        report = write_competitiveness(args.output, args.matches_per_order, args.seed)
        print(json.dumps(report, indent=2))
        return 0
    report = write_sweep(args.output, args.matches_per_order, args.seed)
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
