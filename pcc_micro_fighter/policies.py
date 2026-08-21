from __future__ import annotations
from collections import Counter
from math import exp
import random

from .model import Action, FighterView


LEGAL = tuple(Action)


def _softmax_choice(scores: dict[Action, float], rng: random.Random, temperature: float = 0.7) -> Action:
    """Sample from scored actions without sharing Family A decision rules."""
    if temperature <= 0:
        return max(scores, key=scores.get)
    peak = max(scores.values())
    weights = {a: exp((v - peak) / temperature) for a, v in scores.items()}
    total = sum(weights.values())
    x = rng.random() * total
    acc = 0.0
    for action, weight in weights.items():
        acc += weight
        if x <= acc:
            return action
    return next(reversed(weights))


class NeutralPolicy:
    """Simple state-aware baseline; not a PCC policy."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance <= 1 and view.self_attack_cd == 0:
            return rng.choice([Action.ATTACK, Action.GUARD, Action.EVADE])
        return rng.choice([Action.ADVANCE, Action.GUARD, Action.RETREAT])


# ---------------------------------------------------------------------------
# Family A: compact hand-written conditional policies from v0.1.0.
# ---------------------------------------------------------------------------

class PressurePolicy:
    """Family A Pressure: closes space and sustains credible attack threat."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            return Action.ADVANCE if rng.random() < 0.82 else Action.GUARD
        if view.self_attack_cd == 0:
            return Action.ATTACK if rng.random() < 0.62 else Action.GUARD
        return Action.ADVANCE if rng.random() < 0.55 else Action.GUARD


class ControlPolicy:
    """Family A Control: frequency-based public-history response prediction."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        opp_recent = [b for _, b in view.public_history[-6:]]
        common = Counter(opp_recent).most_common(1)[0][0] if opp_recent else None
        if view.distance > 1:
            if common == Action.RETREAT.value:
                return Action.ADVANCE
            return Action.ADVANCE if rng.random() < 0.55 else Action.GUARD
        if common in (Action.GUARD.value, Action.EVADE.value):
            if view.self_attack_cd == 0 and rng.random() < 0.62:
                return Action.ATTACK
            return Action.GUARD
        if common == Action.ATTACK.value:
            return Action.EVADE if view.self_evade_cd == 0 else Action.GUARD
        if common == Action.RETREAT.value:
            return Action.ADVANCE
        if view.self_attack_cd == 0 and rng.random() < 0.62:
            return Action.ATTACK
        return Action.GUARD if rng.random() < 0.65 else Action.EVADE


class ChaosPolicy:
    """Family A Chaos: state-constrained stochastic policy."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            choices = [Action.ADVANCE, Action.RETREAT, Action.GUARD]
            weights = [0.45, 0.2, 0.35]
        else:
            choices = [Action.ATTACK, Action.GUARD, Action.EVADE, Action.RETREAT, Action.ADVANCE]
            weights = [0.28, 0.24, 0.2, 0.14, 0.14]
            if view.self_attack_cd:
                weights[0] = 0.02
            if view.self_evade_cd:
                weights[2] = 0.02
        return rng.choices(choices, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# Family B: independently structured score/recency policies.
# These do not call or parameterize Family A policies.
# ---------------------------------------------------------------------------

class PressurePolicyB:
    """Family B Pressure: utility-scored space occupation and credible threat."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        scores = {a: -1.0 for a in LEGAL}
        if view.distance > 1:
            scores.update({Action.ADVANCE: 2.4, Action.GUARD: 0.7, Action.RETREAT: -0.2})
        else:
            scores.update({Action.ADVANCE: 0.7, Action.GUARD: 1.0, Action.RETREAT: -0.1})
            scores[Action.ATTACK] = 2.2 if view.self_attack_cd == 0 else -2.0
            scores[Action.EVADE] = 0.35 if view.self_evade_cd == 0 else -2.0
        return _softmax_choice(scores, rng, temperature=0.65)


class ControlPolicyB:
    """Family B Control: recency/transition-sensitive counter selection."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        scores = {Action.ADVANCE: 0.2, Action.RETREAT: 0.0, Action.ATTACK: 0.0,
                  Action.GUARD: 0.25, Action.EVADE: 0.0}
        last = view.public_history[-1][1] if view.public_history else None
        previous = view.public_history[-2][1] if len(view.public_history) >= 2 else None

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

            # Repeated public responses strengthen the corresponding counter.
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


class ChaosPolicyB:
    """Family B Chaos: value-bounded diversification with an anti-repeat penalty."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            scores = {
                Action.ADVANCE: 1.15,
                Action.RETREAT: 0.15,
                Action.GUARD: 0.75,
                Action.ATTACK: -2.0,
                Action.EVADE: -1.0,
            }
        else:
            scores = {
                Action.ADVANCE: 0.25,
                Action.RETREAT: 0.35,
                Action.GUARD: 0.75,
                Action.ATTACK: 1.05 if view.self_attack_cd == 0 else -3.0,
                Action.EVADE: 0.8 if view.self_evade_cd == 0 else -3.0,
            }
        # Suppress the fighter's own most recent action rather than using a fixed mixture.
        if view.public_history:
            own_last = view.public_history[-1][0]
            for action in LEGAL:
                if action.value == own_last:
                    scores[action] -= 0.9
                    break
        return _softmax_choice(scores, rng, temperature=1.05)


POLICY_FAMILIES = {
    "A": {
        "pressure": PressurePolicy,
        "control": ControlPolicy,
        "chaos": ChaosPolicy,
    },
    "B": {
        "pressure": PressurePolicyB,
        "control": ControlPolicyB,
        "chaos": ChaosPolicyB,
    },
}

POLICIES = {
    "neutral": NeutralPolicy,
    "pressure": PressurePolicy,
    "control": ControlPolicy,
    "chaos": ChaosPolicy,
    "pressure_b": PressurePolicyB,
    "control_b": ControlPolicyB,
    "chaos_b": ChaosPolicyB,
}
