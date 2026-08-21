from __future__ import annotations

import json
import random
from pathlib import Path
from statistics import mean

from .engine import simulate_match
from .model import Action, FighterView
from .policies import PressurePolicyB, _softmax_choice


class ControlPolicyBV05:
    """Frozen v0.5 Family B Control reconstructed without the rejected v0.7 recovery rule."""

    def choose(self, view: FighterView, rng: random.Random) -> Action:
        scores = {
            Action.ADVANCE: 0.2,
            Action.RETREAT: 0.0,
            Action.ATTACK: 0.0,
            Action.GUARD: 0.25,
            Action.EVADE: 0.0,
        }
        last = view.public_history[-1][1] if view.public_history else None
        previous = view.public_history[-2][1] if len(view.public_history) >= 2 else None
        own_last = view.public_history[-1][0] if view.public_history else None

        # v0.5 punish-window rule only.
        if (
            view.distance <= 1
            and view.self_attack_cd == 0
            and last == Action.ATTACK.value
            and own_last in (Action.GUARD.value, Action.EVADE.value)
        ):
            return Action.ATTACK

        if view.distance > 1:
            scores[Action.ADVANCE] += 1.0
            scores[Action.GUARD] += 0.3
            if last == Action.RETREAT.value:
                scores[Action.ADVANCE] += 1.3
            if last == Action.ADVANCE.value:
                scores[Action.GUARD] += 0.5
        else:
            if last == Action.ATTACK.value:
                scores[Action.EVADE] += 1.9
                scores[Action.GUARD] += 1.1
            elif last in (Action.GUARD.value, Action.EVADE.value):
                scores[Action.ATTACK] += 1.25
                scores[Action.ADVANCE] += 0.35
            elif last == Action.RETREAT.value:
                scores[Action.ADVANCE] += 1.5
                scores[Action.ATTACK] += 0.35
            else:
                scores[Action.ATTACK] += 0.7
                scores[Action.GUARD] += 0.5

            if last is not None and last == previous:
                if last == Action.ATTACK.value:
                    scores[Action.EVADE] += 0.6
                elif last in (Action.GUARD.value, Action.EVADE.value):
                    scores[Action.ATTACK] += 0.55
                elif last == Action.RETREAT.value:
                    scores[Action.ADVANCE] += 0.6

        if view.self_attack_cd:
            scores[Action.ATTACK] = -3.0
        if view.self_evade_cd:
            scores[Action.EVADE] = -3.0
        return _softmax_choice(scores, rng, temperature=0.55)


def _distance(rec, before: bool) -> int:
    positions = rec.before_positions if before else rec.after_positions
    return abs(positions[0] - positions[1])


def _control_action(rec, control_index: int) -> str:
    return rec.action0 if control_index == 0 else rec.action1


def _pressure_action(rec, control_index: int) -> str:
    return rec.action1 if control_index == 0 else rec.action0


def _control_hit(rec, control_index: int) -> bool:
    return rec.hit0 if control_index == 0 else rec.hit1


def _control_health(rec, control_index: int, before: bool) -> int:
    hp = rec.before_health if before else rec.after_health
    return hp[control_index]


def _analyze_v07_match(result, control_index: int) -> dict:
    records = result.records
    retreat_triggers = 0
    attack_available_proxy = 0
    distance_gain = 0
    ineffective_retreat = 0
    immediate_free_reentry = 0
    persistent_two_ticks = 0
    damage_next_two = []

    for i, rec in enumerate(records):
        if i < 2:
            continue
        if _control_action(rec, control_index) != Action.RETREAT.value:
            continue
        if _distance(rec, True) > 1:
            continue
        prev_opp = [_pressure_action(records[i - 2], control_index), _pressure_action(records[i - 1], control_index)]
        if not all(a in (Action.ADVANCE.value, Action.ATTACK.value) for a in prev_opp):
            continue
        if prev_opp[-1] != Action.ADVANCE.value:
            continue

        retreat_triggers += 1
        # At close range an ATTACK is a potentially valuable initiative action whenever not on cooldown.
        # Tick records do not store cooldown, so this is a conservative proxy: previous own action was not ATTACK.
        if _control_action(records[i - 1], control_index) != Action.ATTACK.value:
            attack_available_proxy += 1

        before_d = _distance(rec, True)
        after_d = _distance(rec, False)
        gained = after_d > before_d
        if gained:
            distance_gain += 1
        else:
            ineffective_retreat += 1

        if gained and i + 1 < len(records):
            nxt = records[i + 1]
            if _pressure_action(nxt, control_index) == Action.ADVANCE.value and _distance(nxt, False) <= 1:
                immediate_free_reentry += 1

        if gained:
            end = min(len(records), i + 3)
            future = records[i + 1:end]
            if future and all(_distance(r, False) > 1 for r in future):
                persistent_two_ticks += 1

        end = min(len(records), i + 3)
        if i + 1 < end:
            hp0 = _control_health(rec, control_index, False)
            hp1 = _control_health(records[end - 1], control_index, False)
            damage_next_two.append(max(0, hp0 - hp1))

    return {
        "retreat_trigger_events": retreat_triggers,
        "attack_available_proxy_events": attack_available_proxy,
        "distance_gain_events": distance_gain,
        "ineffective_retreat_events": ineffective_retreat,
        "immediate_free_reentry_events": immediate_free_reentry,
        "persistent_two_tick_displacement_events": persistent_two_ticks,
        "mean_damage_received_next_two_ticks": mean(damage_next_two) if damage_next_two else 0.0,
    }


def _run_policy(policy_cls, matches_per_order: int, seed: int, analyze_retreat: bool) -> dict:
    wins_p = wins_c = draws = 0
    control_net_damage = []
    event_rows = []
    for order in (0, 1):
        for k in range(matches_per_order):
            s = seed + order * 10000 + k
            pressure = PressurePolicyB()
            control = policy_cls()
            if order == 0:
                result = simulate_match(pressure, control, s)
                control_index = 1
                winner = result.winner
                p_win = winner == 0
                c_win = winner == 1
            else:
                result = simulate_match(control, pressure, s)
                control_index = 0
                winner = result.winner
                p_win = winner == 1
                c_win = winner == 0
            if p_win:
                wins_p += 1
            elif c_win:
                wins_c += 1
            else:
                draws += 1
            final_hp_c = result.health[control_index]
            final_hp_p = result.health[1 - control_index]
            control_net_damage.append(final_hp_c - final_hp_p)
            if analyze_retreat:
                event_rows.append(_analyze_v07_match(result, control_index))

    decisive = wins_p + wins_c
    summary = {
        "pressure_wins": wins_p,
        "control_wins": wins_c,
        "draws": draws,
        "pressure_decisive_win_rate": wins_p / decisive if decisive else 0.0,
        "control_mean_health_margin": mean(control_net_damage),
    }
    if analyze_retreat:
        totals = {k: sum(row[k] for row in event_rows) for k in event_rows[0] if k != "mean_damage_received_next_two_ticks"} if event_rows else {}
        trigger = totals.get("retreat_trigger_events", 0)
        gain = totals.get("distance_gain_events", 0)
        summary["retreat_backfire"] = {
            **totals,
            "initiative_forfeiture_proxy_rate": totals.get("attack_available_proxy_events", 0) / trigger if trigger else 0.0,
            "retreat_ineffectiveness_rate": totals.get("ineffective_retreat_events", 0) / trigger if trigger else 0.0,
            "distance_gain_rate": gain / trigger if trigger else 0.0,
            "immediate_free_reentry_rate_given_gain": totals.get("immediate_free_reentry_events", 0) / gain if gain else 0.0,
            "two_tick_displacement_persistence_rate_given_gain": totals.get("persistent_two_tick_displacement_events", 0) / gain if gain else 0.0,
            "mean_damage_received_next_two_ticks": mean(row["mean_damage_received_next_two_ticks"] for row in event_rows) if event_rows else 0.0,
        }
    return summary


def run_retreat_backfire_decomposition(matches_per_order: int = 400, seed: int = 86001) -> dict:
    # Import current v0.7 policy lazily so this module preserves the explicit v0.5 comparator.
    from .policies import ControlPolicyB

    v05 = _run_policy(ControlPolicyBV05, matches_per_order, seed, analyze_retreat=False)
    v07 = _run_policy(ControlPolicyB, matches_per_order, seed, analyze_retreat=True)
    b = v07["retreat_backfire"]

    interpretation_checks = {
        "v07_worse_than_v05": v07["pressure_decisive_win_rate"] > v05["pressure_decisive_win_rate"],
        "initiative_forfeiture_proxy_at_least_0_50": b["initiative_forfeiture_proxy_rate"] >= 0.50,
        "free_reentry_given_gain_at_least_0_25": b["immediate_free_reentry_rate_given_gain"] >= 0.25,
        "boundary_or_resolution_failure_at_least_0_20": b["retreat_ineffectiveness_rate"] >= 0.20,
        "two_tick_displacement_persistence_below_0_50": b["two_tick_displacement_persistence_rate_given_gain"] < 0.50,
    }

    return {
        "status": "frozen_v05_vs_v07_retreat_backfire_decomposition",
        "design": {
            "version": "0.8.0",
            "matches_per_order": matches_per_order,
            "seed": seed,
            "seat_balanced": True,
            "policies_modified": False,
            "v05_comparator": "Family B Control with v0.5 punish-window rule but without v0.7 sustained-threat recovery rule",
            "v07_target": "Current Family B Control including rejected sustained-threat recovery rule",
            "prespecified_mechanisms": [
                "initiative_forfeiture",
                "free_reentry",
                "boundary_or_resolution_saturation",
                "defensive_displacement_persistence",
            ],
            "post_result_tuning_allowed": False,
        },
        "v0.5": v05,
        "v0.7": v07,
        "prespecified_checks": interpretation_checks,
        "primary_explanation": (
            "Retreat backfire is attributed to the mechanisms that meet their prespecified descriptive thresholds; "
            "no single mechanism is required to explain the full win-rate regression."
        ),
    }


def write_retreat_backfire_decomposition(path: str, matches_per_order: int = 400, seed: int = 86001) -> dict:
    report = run_retreat_backfire_decomposition(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
