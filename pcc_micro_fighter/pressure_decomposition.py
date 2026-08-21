from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from .engine import simulate_match
from .model import Rules
from .policies import POLICY_FAMILIES

MODES = ("control", "chaos")
DEFAULT_MATCHES_PER_ORDER = 300
DEFAULT_SEED = 53001


def _perspective_records(result, player: int):
    for rec in result.records:
        if player == 0:
            yield rec.action0, rec.action1, rec.hit0, rec.hit1, rec
        else:
            yield rec.action1, rec.action0, rec.hit1, rec.hit0, rec


def _match_metrics(result, player: int) -> dict:
    rows = list(_perspective_records(result, player))
    n = max(1, len(rows))
    compression = 0.0
    attacks_in_range = 0
    attacks = 0
    threat_ticks = 0
    next_defense_after_threat = 0
    next_available_after_threat = 0
    hits = 0

    for i, (mine, opp, my_hit, _opp_hit, rec) in enumerate(rows):
        before_d = abs(rec.before_positions[0] - rec.before_positions[1])
        after_d = abs(rec.after_positions[0] - rec.after_positions[1])
        if mine == "advance":
            compression += max(0, before_d - after_d)
        if mine == "attack":
            attacks += 1
            if after_d <= 1:
                attacks_in_range += 1
        if mine in ("advance", "attack"):
            threat_ticks += 1
            if i + 1 < len(rows):
                next_available_after_threat += 1
                next_opp = rows[i + 1][1]
                if next_opp in ("guard", "evade", "retreat"):
                    next_defense_after_threat += 1
        hits += int(my_hit)

    damage_dealt = result.records[0].before_health[1-player] - result.health[1-player] if result.records else 0
    damage_taken = result.records[0].before_health[player] - result.health[player] if result.records else 0
    return {
        "spatial_compression_per_tick": compression / n,
        "attack_rate": attacks / n,
        "in_range_attack_rate": attacks_in_range / n,
        "hit_rate_per_attack": hits / max(1, attacks),
        "threat_rate": threat_ticks / n,
        "next_tick_defensive_response_rate": next_defense_after_threat / max(1, next_available_after_threat),
        "damage_dealt_per_match": float(damage_dealt),
        "damage_taken_per_match": float(damage_taken),
        "net_damage_per_match": float(damage_dealt - damage_taken),
        "damage_per_threat_tick": float(damage_dealt) / max(1, threat_ticks),
    }


def _aggregate(rows: list[dict]) -> dict:
    keys = rows[0].keys()
    return {k: mean(r[k] for r in rows) for k in keys}


def _matchup(family: str, opponent: str, matches_per_order: int, seed: int, rules: Rules) -> dict:
    policies = POLICY_FAMILIES[family]
    pressure_rows: list[dict] = []
    opponent_rows: list[dict] = []
    pressure_wins = opponent_wins = draws = 0

    family_offset = 100000 if family == "B" else 0
    opp_offset = 20000 if opponent == "chaos" else 0
    arena_offset = 500000 if rules.arena_max <= 3 else 0

    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + family_offset + opp_offset + arena_offset + order * 1000 + k
            if order == 0:
                result = simulate_match(policies["pressure"](), policies[opponent](), seed=s, rules=rules)
                p_idx, o_idx = 0, 1
                winner = result.winner
            else:
                result = simulate_match(policies[opponent](), policies["pressure"](), seed=s, rules=rules)
                p_idx, o_idx = 1, 0
                winner = None if result.winner is None else 1 - result.winner

            pressure_rows.append(_match_metrics(result, p_idx))
            opponent_rows.append(_match_metrics(result, o_idx))
            if winner == 0:
                pressure_wins += 1
            elif winner == 1:
                opponent_wins += 1
            else:
                draws += 1

    p = _aggregate(pressure_rows)
    o = _aggregate(opponent_rows)
    decisive = pressure_wins + opponent_wins
    deltas = {k: p[k] - o[k] for k in p}
    return {
        "opponent": opponent,
        "pressure_decisive_win_rate": pressure_wins / decisive if decisive else 0.5,
        "wins_pressure": pressure_wins,
        "wins_opponent": opponent_wins,
        "draws": draws,
        "pressure": p,
        "opponent_metrics": o,
        "pressure_minus_opponent": deltas,
    }


def run_pressure_decomposition(matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    standard = Rules()
    compact = Rules(arena_min=0, arena_max=3)
    families = {}

    for family in ("A", "B"):
        standard_rows = [_matchup(family, opp, matches_per_order, seed, standard) for opp in MODES]
        compact_rows = [_matchup(family, opp, matches_per_order, seed, compact) for opp in MODES]
        compact_by_opp = {r["opponent"]: r for r in compact_rows}
        for row in standard_rows:
            compact_row = compact_by_opp[row["opponent"]]
            row["compact_arena_pressure_win_rate"] = compact_row["pressure_decisive_win_rate"]
            row["pressure_win_rate_change_when_starting_in_range"] = (
                compact_row["pressure_decisive_win_rate"] - row["pressure_decisive_win_rate"]
            )
        families[family] = {
            "standard_matchups": standard_rows,
            "compact_arena_matchups": compact_rows,
        }

    # Candidate explanations are intentionally diagnostics, not confirmation gates.
    # A factor is called replicated only if its Pressure-minus-opponent delta has
    # the expected sign against both opponents in both independent families.
    replicated = {}
    metric_expectations = {
        "space_capture": ("spatial_compression_per_tick", 1),
        "attack_opportunity_generation": ("in_range_attack_rate", 1),
        "defensive_response_forcing": ("next_tick_defensive_response_rate", 1),
        "damage_conversion": ("net_damage_per_match", 1),
    }
    for label, (metric, sign) in metric_expectations.items():
        vals = [
            sign * row["pressure_minus_opponent"][metric]
            for family in families.values()
            for row in family["standard_matchups"]
        ]
        replicated[label] = {
            "replicated_expected_direction": all(v > 0 for v in vals),
            "minimum_directional_delta": min(vals),
            "mean_directional_delta": mean(vals),
        }

    compact_changes = [
        row["pressure_win_rate_change_when_starting_in_range"]
        for family in families.values()
        for row in family["standard_matchups"]
    ]
    replicated["spatial_access_dependency"] = {
        "pressure_advantage_reduced_in_all_matchups": all(v < 0 for v in compact_changes),
        "mean_pressure_win_rate_change": mean(compact_changes),
        "minimum_change": min(compact_changes),
        "maximum_change": max(compact_changes),
    }

    return {
        "pressure_dominance_decomposition_confirmed": False,
        "status": "descriptive_mechanism_decomposition",
        "design": {
            "policy_version": "0.2.0",
            "policies_modified": False,
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_order_balanced": True,
            "standard_arena": [standard.arena_min, standard.arena_max],
            "compact_arena": [compact.arena_min, compact.arena_max],
            "candidate_mechanisms": list(metric_expectations),
            "post_result_policy_tuning_allowed": False,
        },
        "families": families,
        "replicated_diagnostics": replicated,
        "interpretation": (
            "This frozen diagnostic decomposes the v0.2 Pressure advantage without changing policies. "
            "It distinguishes attributable spatial compression, in-range attack opportunity use, delayed defensive forcing, "
            "and damage conversion. The compact-arena replay removes most initial approach distance as a diagnostic of spatial-access dependence."
        ),
    }


def write_pressure_decomposition(path: str, matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    report = run_pressure_decomposition(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
