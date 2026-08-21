from __future__ import annotations
import argparse, json
from .engine import simulate_match
from .experiment import write_sweep
from .competitiveness import write_competitiveness
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
    args = p.parse_args()
    if args.cmd == "simulate":
        r = simulate_match(POLICIES[args.p0](), POLICIES[args.p1](), args.seed)
        print(json.dumps({"winner": r.winner, "ticks": r.ticks, "health": r.health, "p0": summarize(r,0), "p1": summarize(r,1)}, indent=2))
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
