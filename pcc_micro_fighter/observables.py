from __future__ import annotations
from collections import Counter
from math import log
from .model import MatchResult


def _entropy(values: list[str]) -> float:
    if not values:
        return 0.0
    counts = Counter(values)
    n = len(values)
    return -sum((c/n) * log(c/n) for c in counts.values())


def summarize(result: MatchResult, player: int) -> dict:
    mine = [r.action0 if player == 0 else r.action1 for r in result.records]
    opp = [r.action1 if player == 0 else r.action0 for r in result.records]
    before_distance = [abs(r.before_positions[0] - r.before_positions[1]) for r in result.records]
    after_distance = [abs(r.after_positions[0] - r.after_positions[1]) for r in result.records]
    attacks = sum(a == "attack" for a in mine)
    advances = sum(a == "advance" for a in mine)
    # Attribute spatial compression only when this fighter chose advance and the
    # public distance actually decreased. This remains descriptive in v0.1.
    constriction = sum(
        max(0, b - a)
        for action, b, a in zip(mine, before_distance, after_distance)
        if action == "advance"
    ) / max(1, len(mine))
    entropy = _entropy(mine)
    opp_entropy = _entropy(opp)
    damage = (result.records[0].before_health[1-player] - result.health[1-player]) if result.records else 0
    taken = (result.records[0].before_health[player] - result.health[player]) if result.records else 0
    return {
        "ticks": len(mine),
        "advance_rate": advances / max(1, len(mine)),
        "attack_rate": attacks / max(1, len(mine)),
        "spatial_constriction": constriction,
        "action_entropy": entropy,
        "opponent_action_entropy": opp_entropy,
        "damage_dealt": damage,
        "damage_taken": taken,
        "net_damage": damage - taken,
    }
