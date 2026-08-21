from __future__ import annotations
import json
from pathlib import Path

from .engine import simulate_match
from .policies import POLICY_FAMILIES

MIN_WIN_RATE = 0.30
MAX_WIN_RATE = 0.70
MODES = ("pressure", "control", "chaos")


def _pair_result(family: str, a: str, b: str, matches_per_order: int, seed: int) -> dict:
    policies = POLICY_FAMILIES[family]
    wins_a = wins_b = draws = 0
    pair_index = MODES.index(a) * 10 + MODES.index(b)
    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + (100000 if family == "B" else 0) + pair_index * 10000 + order * 1000 + k
            if order == 0:
                result = simulate_match(policies[a](), policies[b](), seed=s)
                winner_a_view = result.winner
            else:
                result = simulate_match(policies[b](), policies[a](), seed=s)
                winner_a_view = None if result.winner is None else 1 - result.winner
            if winner_a_view == 0:
                wins_a += 1
            elif winner_a_view == 1:
                wins_b += 1
            else:
                draws += 1
    decisive = wins_a + wins_b
    a_decisive_win_rate = wins_a / decisive if decisive else 0.5
    total = decisive + draws
    return {
        "a": a,
        "b": b,
        "wins_a": wins_a,
        "wins_b": wins_b,
        "draws": draws,
        "a_win_rate_all_matches": wins_a / total,
        "b_win_rate_all_matches": wins_b / total,
        "draw_rate": draws / total,
        "a_decisive_win_rate": a_decisive_win_rate,
        "competitive": MIN_WIN_RATE <= a_decisive_win_rate <= MAX_WIN_RATE,
    }


def run_competitiveness(matches_per_order: int = 400, seed: int = 42001) -> dict:
    families = {}
    all_checks = []
    for family in ("A", "B"):
        rows = []
        for i, a in enumerate(MODES):
            for b in MODES[i + 1:]:
                row = _pair_result(family, a, b, matches_per_order, seed)
                rows.append(row)
                all_checks.append(row["competitive"])
        families[family] = {
            "all_pairwise_matchups_competitive": all(r["competitive"] for r in rows),
            "matchups": rows,
        }
    return {
        "competitiveness_confirmed": all(all_checks),
        "design": {
            "policy_families": ["A", "B"],
            "modes": list(MODES),
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_order_balanced": True,
            "decisive_win_rate_window": [MIN_WIN_RATE, MAX_WIN_RATE],
            "cycle_required": False,
            "post_result_tuning_allowed": False,
        },
        "families": families,
        "interpretation": (
            "This gate tests only whether any synthetic mechanism trivially dominates another. "
            "It does not require or reward a Pressure-Chaos-Control dominance cycle."
        ),
    }


def write_competitiveness(path: str, matches_per_order: int = 400, seed: int = 42001) -> dict:
    report = run_competitiveness(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
