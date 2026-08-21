from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

from .engine import simulate_match
from .model import Rules
from .policies import POLICY_FAMILIES

DEFAULT_MATCHES_PER_ORDER = 400
DEFAULT_SEED = 64001


def _policy_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name("policies.py").read_bytes()).hexdigest()


def _perspective(result, player: int):
    for rec in result.records:
        if player == 0:
            yield rec.action0, rec.action1, rec.hit0, rec.hit1, rec
        else:
            yield rec.action1, rec.action0, rec.hit1, rec.hit0, rec


def _distance(rec) -> int:
    return abs(rec.after_positions[0] - rec.after_positions[1])


def _metrics(result, player: int, rules: Rules) -> dict:
    rows = list(_perspective(result, player))
    if not rows:
        return {k: 0.0 for k in (
            "attack_attempts_per_match", "attack_opportunities_per_match", "attack_take_rate",
            "hit_conversion_per_attack", "hit_conversion_per_opportunity", "damage_per_attack_opportunity",
            "opponent_attacks_per_match", "defensive_response_rate", "successful_defenses_per_match",
            "successful_defense_rate_per_opponent_attack", "counter_windows_per_match", "counter_window_creation_rate",
            "counter_attack_take_rate", "counter_hit_rate_per_window", "counter_hit_rate_per_counter_attempt",
            "cooldown_punishment_attack_rate", "cooldown_punishment_hit_rate", "positional_recovery_rate_after_defense",
            "damage_received_per_opponent_threat_tick", "damage_dealt_per_match", "damage_taken_per_match",
            "net_damage_per_match"
        )}

    attack_cd = 0
    attacks = hits = opportunities = 0
    opp_attacks = defensive_responses = successful_defenses = 0
    counter_windows = counter_attacks = counter_hits = 0
    cooldown_windows = cooldown_attacks = cooldown_hits = 0
    positional_recoveries = positional_recovery_windows = 0
    opponent_threat_ticks = 0

    # Reconstruct the focal fighter's attack cooldown exactly from its own public actions.
    # Cooldown is checked before the current action and updated after resolution.
    attack_cd_before: list[int] = []
    cd = 0
    for mine, _opp, _my_hit, _opp_hit, _rec in rows:
        attack_cd_before.append(cd)
        if mine == "attack":
            cd = rules.attack_cooldown
        else:
            cd = max(0, cd - 1)

    for i, (mine, opp, my_hit, opp_hit, rec) in enumerate(rows):
        after_d = _distance(rec)
        if after_d <= rules.attack_range and attack_cd_before[i] == 0:
            opportunities += 1
        if mine == "attack":
            attacks += 1
        hits += int(my_hit)

        if opp in ("advance", "attack"):
            opponent_threat_ticks += 1

        if opp == "attack":
            opp_attacks += 1
            if mine in ("guard", "evade"):
                defensive_responses += 1
            successful = mine in ("guard", "evade") and not opp_hit
            if successful:
                successful_defenses += 1
                if i + 1 < len(rows):
                    positional_recovery_windows += 1
                    next_rec = rows[i + 1][4]
                    if _distance(next_rec) > after_d:
                        positional_recoveries += 1

                    # Because the attacker attacked on this tick, its attack cooldown is active
                    # on the next tick. If range is retained, this is a concrete punish window.
                    if after_d <= rules.attack_range:
                        counter_windows += 1
                        next_mine, _next_opp, next_hit, _next_opp_hit, _ = rows[i + 1]
                        if next_mine == "attack":
                            counter_attacks += 1
                            if next_hit:
                                counter_hits += 1

            # Every surviving next tick after an opponent attack is an attacker-cooldown window;
            # range determines whether an immediate attack punishment is physically available.
            if i + 1 < len(rows):
                cooldown_windows += 1
                next_mine, _next_opp, next_hit, _next_opp_hit, next_rec = rows[i + 1]
                if _distance(rec) <= rules.attack_range and next_mine == "attack":
                    cooldown_attacks += 1
                    if next_hit:
                        cooldown_hits += 1

    start_hp = result.records[0].before_health[player]
    opp_start_hp = result.records[0].before_health[1 - player]
    damage_taken = float(start_hp - result.health[player])
    damage_dealt = float(opp_start_hp - result.health[1 - player])

    return {
        "attack_attempts_per_match": float(attacks),
        "attack_opportunities_per_match": float(opportunities),
        "attack_take_rate": attacks / max(1, opportunities),
        "hit_conversion_per_attack": hits / max(1, attacks),
        "hit_conversion_per_opportunity": hits / max(1, opportunities),
        "damage_per_attack_opportunity": damage_dealt / max(1, opportunities),
        "opponent_attacks_per_match": float(opp_attacks),
        "defensive_response_rate": defensive_responses / max(1, opp_attacks),
        "successful_defenses_per_match": float(successful_defenses),
        "successful_defense_rate_per_opponent_attack": successful_defenses / max(1, opp_attacks),
        "counter_windows_per_match": float(counter_windows),
        "counter_window_creation_rate": counter_windows / max(1, successful_defenses),
        "counter_attack_take_rate": counter_attacks / max(1, counter_windows),
        "counter_hit_rate_per_window": counter_hits / max(1, counter_windows),
        "counter_hit_rate_per_counter_attempt": counter_hits / max(1, counter_attacks),
        "cooldown_punishment_attack_rate": cooldown_attacks / max(1, cooldown_windows),
        "cooldown_punishment_hit_rate": cooldown_hits / max(1, cooldown_windows),
        "positional_recovery_rate_after_defense": positional_recoveries / max(1, positional_recovery_windows),
        "damage_received_per_opponent_threat_tick": damage_taken / max(1, opponent_threat_ticks),
        "damage_dealt_per_match": damage_dealt,
        "damage_taken_per_match": damage_taken,
        "net_damage_per_match": damage_dealt - damage_taken,
    }


def _aggregate(rows: list[dict]) -> dict:
    return {key: mean(r[key] for r in rows) for key in rows[0]}


def _pressure_control_matchup(family: str, matches_per_order: int, seed: int) -> dict:
    policies = POLICY_FAMILIES[family]
    rules = Rules()
    pressure_rows: list[dict] = []
    control_rows: list[dict] = []
    pressure_wins = control_wins = draws = 0
    family_offset = 100000 if family == "B" else 0

    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + family_offset + order * 10000 + k
            if order == 0:
                result = simulate_match(policies["pressure"](), policies["control"](), seed=s, rules=rules)
                p_idx, c_idx = 0, 1
                winner = result.winner
            else:
                result = simulate_match(policies["control"](), policies["pressure"](), seed=s, rules=rules)
                p_idx, c_idx = 1, 0
                winner = None if result.winner is None else 1 - result.winner

            pressure_rows.append(_metrics(result, p_idx, rules))
            control_rows.append(_metrics(result, c_idx, rules))
            if winner == 0:
                pressure_wins += 1
            elif winner == 1:
                control_wins += 1
            else:
                draws += 1

    p = _aggregate(pressure_rows)
    c = _aggregate(control_rows)
    decisive = pressure_wins + control_wins
    return {
        "pressure_decisive_win_rate": pressure_wins / decisive if decisive else 0.5,
        "wins_pressure": pressure_wins,
        "wins_control": control_wins,
        "draws": draws,
        "pressure": p,
        "control": c,
        "control_minus_pressure": {k: c[k] - p[k] for k in p},
    }


def run_threat_conversion(matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    policy_hash = _policy_sha256()
    families = {
        family: _pressure_control_matchup(family, matches_per_order, seed)
        for family in ("A", "B")
    }

    # These are descriptive contrasts selected before examining the v0.4 run.
    # They explain exchange conversion; they are not a construct-validity gate.
    control_keys = (
        "successful_defense_rate_per_opponent_attack",
        "counter_window_creation_rate",
        "counter_attack_take_rate",
        "counter_hit_rate_per_window",
        "cooldown_punishment_hit_rate",
        "damage_per_attack_opportunity",
        "damage_received_per_opponent_threat_tick",
        "positional_recovery_rate_after_defense",
        "net_damage_per_match",
    )
    family_contrast = {
        key: families["A"]["control"][key] - families["B"]["control"][key]
        for key in control_keys
    }

    return {
        "threat_conversion_decomposition_confirmed": False,
        "status": "descriptive_threat_conversion_and_counter_value_decomposition",
        "design": {
            "policy_version": "0.2.0",
            "policies_modified": False,
            "observed_policy_sha256": policy_hash,
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_order_balanced": True,
            "primary_matchup": "pressure_vs_control",
            "post_result_policy_tuning_allowed": False,
            "counter_window_definition": (
                "successful guard/evade against an incoming attack, still in attack range after resolution, "
                "with a surviving next tick while the attacker is on attack cooldown"
            ),
        },
        "families": families,
        "family_A_control_minus_family_B_control": family_contrast,
        "interpretation": (
            "This frozen diagnostic asks why Family A Control converts Pressure exposure into winning exchanges while "
            "Family B Control does not. It separates defense success, counter-window creation, counter-window use, "
            "landed punishment, attack-opportunity conversion, positional recovery, cooldown punishment, and damage "
            "received per opponent threat tick. It does not rebalance policies or authorize construct recovery."
        ),
    }


def write_threat_conversion(path: str, matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    report = run_threat_conversion(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
