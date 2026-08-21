from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

from .engine import simulate_match
from .model import Rules
from .policies import POLICY_FAMILIES

DEFAULT_MATCHES_PER_ORDER = 400
DEFAULT_SEED = 75001
EXPECTED_V05_POLICY_SHA256 = "93ca6c82abf1d1280334a7c048f4b01f59b7da5765f3d6b780b11cda919f1242"


def _policy_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name("policies.py").read_bytes()).hexdigest()


def _perspective(result, control_idx: int):
    for rec in result.records:
        if control_idx == 0:
            yield rec.action0, rec.action1, rec.hit0, rec.hit1, rec
        else:
            yield rec.action1, rec.action0, rec.hit1, rec.hit0, rec


def _distance(rec) -> int:
    return abs(rec.after_positions[0] - rec.after_positions[1])


def _before_distance(rec) -> int:
    return abs(rec.before_positions[0] - rec.before_positions[1])


def _one_match_metrics(result, control_idx: int, rules: Rules) -> dict:
    rows = list(_perspective(result, control_idx))
    if not rows:
        return {k: 0.0 for k in (
            "pressure_threat_ticks", "pressure_close_threat_ticks", "mean_pressure_threat_run_length",
            "max_pressure_threat_run_length", "control_defense_rate_vs_pressure_attacks",
            "control_defensive_action_rate_during_close_threat", "control_retreat_rate_during_threat",
            "control_distance_gain_rate_during_threat", "control_distance_loss_rate_during_threat",
            "control_post_threat_recovery_rate", "damage_taken_per_close_threat_tick",
            "damage_taken_during_sustained_threat_per_match", "damage_dealt_during_sustained_threat_per_match",
            "control_hit_rate_during_close_threat", "pressure_reengagement_rate_after_control_hit",
            "pressure_reengagement_rate_after_successful_defense", "net_damage_per_match"
        )}

    threat_flags = []
    close_threat_flags = []
    pressure_attacks = defenses = 0
    defensive_close = retreat_threat = 0
    distance_gain = distance_loss = 0
    recovery_windows = recoveries = 0
    close_threat_ticks = 0
    damage_taken_close = 0.0
    damage_taken_sustained = 0.0
    damage_dealt_sustained = 0.0
    close_control_hits = 0
    control_hits = 0
    reengage_after_hit_windows = reengage_after_hit = 0
    successful_defense_windows = reengage_after_defense = 0

    for i, (control_action, pressure_action, control_hit, pressure_hit, rec) in enumerate(rows):
        before_d = _before_distance(rec)
        after_d = _distance(rec)
        threat = pressure_action in ("advance", "attack")
        close_threat = threat and after_d <= rules.attack_range
        threat_flags.append(threat)
        close_threat_flags.append(close_threat)

        if pressure_action == "attack":
            pressure_attacks += 1
            if control_action in ("guard", "evade"):
                defenses += 1
            if control_action in ("guard", "evade") and not pressure_hit and i + 1 < len(rows):
                successful_defense_windows += 1
                next_pressure = rows[i + 1][1]
                if next_pressure in ("advance", "attack"):
                    reengage_after_defense += 1

        if close_threat:
            close_threat_ticks += 1
            if control_action in ("guard", "evade"):
                defensive_close += 1
            if control_hit:
                close_control_hits += 1
            if pressure_hit:
                damage_taken_close += rules.attack_damage

        if threat:
            if control_action == "retreat":
                retreat_threat += 1
            if after_d > before_d:
                distance_gain += 1
            elif after_d < before_d:
                distance_loss += 1

        if control_hit:
            control_hits += 1
            if i + 1 < len(rows):
                reengage_after_hit_windows += 1
                next_pressure = rows[i + 1][1]
                if next_pressure in ("advance", "attack"):
                    reengage_after_hit += 1

    # Consecutive close-threat runs operationalize sustained Pressure exposure.
    runs: list[tuple[int, int]] = []
    start = None
    for i, flag in enumerate(close_threat_flags + [False]):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            runs.append((start, i - 1))
            start = None

    sustained = [(a, b) for a, b in runs if b - a + 1 >= 2]
    for a, b in sustained:
        for i in range(a, b + 1):
            _ca, _pa, ch, ph, _rec = rows[i]
            damage_taken_sustained += rules.attack_damage * int(ph)
            damage_dealt_sustained += rules.attack_damage * int(ch)
        # Recovery = distance increases within two surviving ticks after a sustained run ends.
        if b + 1 < len(rows):
            recovery_windows += 1
            endpoint = _distance(rows[b][4])
            for j in range(b + 1, min(len(rows), b + 3)):
                if _distance(rows[j][4]) > endpoint:
                    recoveries += 1
                    break

    run_lengths = [b - a + 1 for a, b in runs]
    start_hp = rows[0][4].before_health[control_idx]
    opp_start_hp = rows[0][4].before_health[1 - control_idx]
    damage_taken = float(start_hp - result.health[control_idx])
    damage_dealt = float(opp_start_hp - result.health[1 - control_idx])
    threat_ticks = sum(threat_flags)

    return {
        "pressure_threat_ticks": float(threat_ticks),
        "pressure_close_threat_ticks": float(close_threat_ticks),
        "mean_pressure_threat_run_length": mean(run_lengths) if run_lengths else 0.0,
        "max_pressure_threat_run_length": float(max(run_lengths) if run_lengths else 0),
        "control_defense_rate_vs_pressure_attacks": defenses / max(1, pressure_attacks),
        "control_defensive_action_rate_during_close_threat": defensive_close / max(1, close_threat_ticks),
        "control_retreat_rate_during_threat": retreat_threat / max(1, threat_ticks),
        "control_distance_gain_rate_during_threat": distance_gain / max(1, threat_ticks),
        "control_distance_loss_rate_during_threat": distance_loss / max(1, threat_ticks),
        "control_post_threat_recovery_rate": recoveries / max(1, recovery_windows),
        "damage_taken_per_close_threat_tick": damage_taken_close / max(1, close_threat_ticks),
        "damage_taken_during_sustained_threat_per_match": damage_taken_sustained,
        "damage_dealt_during_sustained_threat_per_match": damage_dealt_sustained,
        "control_hit_rate_during_close_threat": close_control_hits / max(1, close_threat_ticks),
        "pressure_reengagement_rate_after_control_hit": reengage_after_hit / max(1, reengage_after_hit_windows),
        "pressure_reengagement_rate_after_successful_defense": reengage_after_defense / max(1, successful_defense_windows),
        "net_damage_per_match": damage_dealt - damage_taken,
    }


def _aggregate(rows: list[dict]) -> dict:
    return {key: mean(row[key] for row in rows) for key in rows[0]}


def run_residual_pressure(matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    policies = POLICY_FAMILIES["B"]
    rules = Rules()
    rows = []
    pressure_wins = control_wins = draws = 0

    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + order * 10000 + k
            if order == 0:
                result = simulate_match(policies["pressure"](), policies["control"](), seed=s, rules=rules)
                control_idx = 1
                winner = result.winner
            else:
                result = simulate_match(policies["control"](), policies["pressure"](), seed=s, rules=rules)
                control_idx = 0
                winner = None if result.winner is None else 1 - result.winner
            rows.append(_one_match_metrics(result, control_idx, rules))
            if winner == 0:
                pressure_wins += 1
            elif winner == 1:
                control_wins += 1
            else:
                draws += 1

    metrics = _aggregate(rows)
    decisive = pressure_wins + control_wins
    policy_hash = _policy_sha256()
    return {
        "residual_pressure_decomposition_confirmed": False,
        "status": "frozen_descriptive_residual_family_b_pressure_decomposition",
        "design": {
            "version": "0.6.0",
            "policy_version": "0.5.0",
            "policies_modified": False,
            "expected_v05_policy_sha256": EXPECTED_V05_POLICY_SHA256,
            "observed_policy_sha256": policy_hash,
            "policy_hash_matches_expected": policy_hash == EXPECTED_V05_POLICY_SHA256,
            "family": "B",
            "matchup": "pressure_vs_control",
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_order_balanced": True,
            "post_result_policy_tuning_allowed": False,
            "sustained_threat_definition": "at least two consecutive ticks where Pressure chooses advance/attack and remains within attack range after resolution",
            "recovery_definition": "distance increases within two surviving ticks after a sustained close-threat run ends",
        },
        "matchup": {
            "pressure_decisive_win_rate": pressure_wins / decisive if decisive else 0.5,
            "wins_pressure": pressure_wins,
            "wins_control": control_wins,
            "draws": draws,
        },
        "metrics": metrics,
        "diagnostic_flags": {
            "control_defends_at_least_half_of_pressure_attacks": metrics["control_defense_rate_vs_pressure_attacks"] >= 0.5,
            "pressure_reengages_after_majority_of_control_hits": metrics["pressure_reengagement_rate_after_control_hit"] >= 0.5,
            "pressure_reengages_after_majority_of_successful_defenses": metrics["pressure_reengagement_rate_after_successful_defense"] >= 0.5,
            "control_recovers_space_after_at_least_half_of_sustained_threats": metrics["control_post_threat_recovery_rate"] >= 0.5,
            "sustained_threat_net_damage_favors_control": metrics["damage_dealt_during_sustained_threat_per_match"] > metrics["damage_taken_during_sustained_threat_per_match"],
        },
        "interpretation": (
            "This frozen v0.6 diagnostic decomposes the residual Family B Pressure advantage after the v0.5 public counter-window intervention. "
            "It measures defense frequency, sustained close-threat persistence, spatial concession/recovery, damage during sustained threat sequences, "
            "and Pressure re-engagement after Control hits or successful defenses. It changes no policy or engine parameter and does not authorize construct recovery."
        ),
    }


def write_residual_pressure(path: str, matches_per_order: int = DEFAULT_MATCHES_PER_ORDER, seed: int = DEFAULT_SEED) -> dict:
    report = run_residual_pressure(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
