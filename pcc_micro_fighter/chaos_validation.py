from __future__ import annotations
from collections import Counter, defaultdict
import json
from math import log
from pathlib import Path
from statistics import mean

from .chaos_policies import (
    AdaptiveExploiterPolicy,
    EffectiveChaosPolicy,
    PredictableCompetentPolicy,
    StateRandomPolicy,
)
from .engine import simulate_match
from .policies import NeutralPolicy


FOCAL = {
    "predictable_competent": PredictableCompetentPolicy,
    "state_random": StateRandomPolicy,
    "effective_chaos": EffectiveChaosPolicy,
}


def _conditional_entropy(sequences: list[list[str]]) -> float:
    transitions = defaultdict(Counter)
    totals = Counter()
    for seq in sequences:
        for a, b in zip(seq, seq[1:]):
            transitions[a][b] += 1
            totals[a] += 1
    n = sum(totals.values())
    if n == 0:
        return 0.0
    h = 0.0
    for a, count in totals.items():
        local = 0.0
        for c in transitions[a].values():
            p = c / count
            local -= p * log(p)
        h += (count / n) * local
    return h / log(5)


def _evaluate(focal_cls, opponent_cls, matches_per_order: int, seed: int) -> dict:
    wins = losses = draws = 0
    margins = []
    sequences: list[list[str]] = []
    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + order * 100000 + k
            if order == 0:
                result = simulate_match(focal_cls(), opponent_cls(), s)
                focal_player = 0
                winner = result.winner
                seq = [r.action0 for r in result.records]
                margin = result.health[0] - result.health[1]
            else:
                result = simulate_match(opponent_cls(), focal_cls(), s)
                focal_player = 1
                winner = None if result.winner is None else 1 - result.winner
                seq = [r.action1 for r in result.records]
                margin = result.health[1] - result.health[0]
            sequences.append(seq)
            margins.append(margin)
            if winner == 0:
                wins += 1
            elif winner == 1:
                losses += 1
            else:
                draws += 1
    decisive = wins + losses
    return {
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "decisive_win_rate": wins / decisive if decisive else 0.5,
        "mean_health_margin": mean(margins) if margins else 0.0,
        "conditional_action_entropy": _conditional_entropy(sequences),
    }


def chaos_validation(matches_per_order: int = 400, seed: int = 97001) -> dict:
    results = {}
    for i, (name, cls) in enumerate(FOCAL.items()):
        neutral = _evaluate(cls, NeutralPolicy, matches_per_order, seed + i * 1000000)
        exploiter = _evaluate(cls, AdaptiveExploiterPolicy, matches_per_order, seed + i * 1000000 + 500000)
        results[name] = {
            "neutral": neutral,
            "adaptive_exploiter": exploiter,
            "exploitability_health_loss": neutral["mean_health_margin"] - exploiter["mean_health_margin"],
        }

    pred = results["predictable_competent"]
    rnd = results["state_random"]
    chaos = results["effective_chaos"]
    checks = {
        "effective_chaos_entropy_exceeds_predictable_by_0_10": (
            chaos["neutral"]["conditional_action_entropy"] >= pred["neutral"]["conditional_action_entropy"] + 0.10
        ),
        "effective_chaos_preserves_value_over_random": (
            chaos["neutral"]["mean_health_margin"] >= rnd["neutral"]["mean_health_margin"] + 0.50
            or chaos["neutral"]["decisive_win_rate"] >= rnd["neutral"]["decisive_win_rate"] + 0.10
        ),
        "effective_chaos_reduces_exploitability_vs_predictable_by_0_25": (
            chaos["exploitability_health_loss"] <= pred["exploitability_health_loss"] - 0.25
        ),
        "effective_chaos_preserves_value_over_random_under_exploitation": (
            chaos["adaptive_exploiter"]["mean_health_margin"] >= rnd["adaptive_exploiter"]["mean_health_margin"] + 0.50
            or chaos["adaptive_exploiter"]["decisive_win_rate"] >= rnd["adaptive_exploiter"]["decisive_win_rate"] + 0.10
        ),
    }
    return {
        "status": "completed",
        "design": {
            "status": "frozen_effective_chaos_validation",
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_balanced": True,
            "human_data": False,
            "policy_scope": "evaluation-only v0.9 policies; prior P/C/Ch policies unchanged",
        },
        "results": results,
        "prespecified_checks": checks,
        "effective_chaos_confirmed": all(checks.values()),
        "interpretation": (
            "Chaos requires unpredictability plus preserved strategic adequacy and resistance to a fixed adaptive exploiter; "
            "high entropy alone is insufficient."
        ),
    }


def write_chaos_validation(path: str, matches_per_order: int = 400, seed: int = 97001) -> dict:
    report = chaos_validation(matches_per_order, seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
