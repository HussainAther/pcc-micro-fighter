from __future__ import annotations
from collections import Counter
import random

from .model import Action, FighterView


LEGAL = tuple(Action)


class NeutralPolicy:
    """Simple state-aware baseline; not a PCC policy."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance <= 1 and view.self_attack_cd == 0:
            return rng.choice([Action.ATTACK, Action.GUARD, Action.EVADE])
        return rng.choice([Action.ADVANCE, Action.GUARD, Action.RETREAT])


class PressurePolicy:
    """Closes space and sustains credible attack threat; avoids suicidal attack spam."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            return Action.ADVANCE if rng.random() < 0.82 else Action.GUARD
        if view.self_attack_cd == 0:
            return Action.ATTACK if rng.random() < 0.62 else Action.GUARD
        return Action.ADVANCE if rng.random() < 0.55 else Action.GUARD


class ControlPolicy:
    """Uses public opponent history to predict and punish repeated responses."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        opp_recent = [b for _, b in view.public_history[-6:]]
        common = Counter(opp_recent).most_common(1)[0][0] if opp_recent else None
        if view.distance > 1:
            if common == Action.RETREAT.value:
                return Action.ADVANCE
            return Action.ADVANCE if rng.random() < 0.55 else Action.GUARD
        if common in (Action.GUARD.value, Action.EVADE.value):
            # punish passive/repeated defense with a credible attack, but do not spam it
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
    """State-constrained stochastic policy; randomness is not assumed to equal Chaos."""
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


POLICIES = {
    "neutral": NeutralPolicy,
    "pressure": PressurePolicy,
    "control": ControlPolicy,
    "chaos": ChaosPolicy,
}
