from __future__ import annotations
import json
from pathlib import Path
from statistics import mean

from .engine import simulate_match
from .observables import summarize
from .policies import POLICIES


def pairwise_sweep(matches_per_order: int = 100, seed: int = 1000) -> dict:
    names = ["neutral", "pressure", "control", "chaos"]
    rows = []
    for i, a in enumerate(names):
        for b in names[i+1:]:
            wins_a = wins_b = draws = 0
            obs_a = []
            obs_b = []
            for order in (0, 1):
                for k in range(matches_per_order):
                    s = seed + i * 100000 + names.index(b) * 10000 + order * 1000 + k
                    pa, pb = POLICIES[a](), POLICIES[b]()
                    result = simulate_match(pa, pb, s) if order == 0 else simulate_match(pb, pa, s)
                    if order == 0:
                        wa = result.winner
                        obs_a.append(summarize(result, 0)); obs_b.append(summarize(result, 1))
                    else:
                        wa = None if result.winner is None else 1 - result.winner
                        obs_a.append(summarize(result, 1)); obs_b.append(summarize(result, 0))
                    if wa == 0: wins_a += 1
                    elif wa == 1: wins_b += 1
                    else: draws += 1
            total = wins_a + wins_b + draws
            rows.append({
                "a": a, "b": b,
                "a_win_rate": wins_a/total,
                "b_win_rate": wins_b/total,
                "draw_rate": draws/total,
                "a_mean_net_damage": mean(x["net_damage"] for x in obs_a),
                "b_mean_net_damage": mean(x["net_damage"] for x in obs_b),
                "a_mean_action_entropy": mean(x["action_entropy"] for x in obs_a),
                "b_mean_action_entropy": mean(x["action_entropy"] for x in obs_b),
                "a_mean_spatial_constriction": mean(x["spatial_constriction"] for x in obs_a),
                "b_mean_spatial_constriction": mean(x["spatial_constriction"] for x in obs_b),
            })
    return {"design": {"matches_per_order": matches_per_order, "seed": seed, "seat_balanced": True}, "matchups": rows}


def write_sweep(path: str, matches_per_order: int = 100, seed: int = 1000) -> dict:
    report = pairwise_sweep(matches_per_order, seed)
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
