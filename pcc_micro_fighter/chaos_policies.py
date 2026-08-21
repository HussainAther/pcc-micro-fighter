from __future__ import annotations
from collections import Counter, defaultdict
import random

from .model import Action, FighterView


class PredictableCompetentPolicy:
    """Low-entropy state-competent baseline for the v0.9 Chaos experiment."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        last_opp = view.public_history[-1][1] if view.public_history else None
        if view.distance > 1:
            return Action.ADVANCE
        if last_opp == Action.ATTACK.value:
            return Action.EVADE if view.self_evade_cd == 0 else Action.GUARD
        if view.self_attack_cd == 0:
            return Action.ATTACK
        return Action.GUARD


class StateRandomPolicy:
    """State-aware random baseline; unpredictability without an adequacy claim."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            return rng.choice([Action.ADVANCE, Action.RETREAT, Action.GUARD])
        actions = [Action.ADVANCE, Action.RETREAT, Action.GUARD]
        if view.self_attack_cd == 0:
            actions.append(Action.ATTACK)
        if view.self_evade_cd == 0:
            actions.append(Action.EVADE)
        return rng.choice(actions)


class EffectiveChaosPolicy:
    """Value-bounded diversified candidate; not equivalent to uniform randomness."""
    def choose(self, view: FighterView, rng: random.Random) -> Action:
        if view.distance > 1:
            actions = [Action.ADVANCE, Action.GUARD, Action.RETREAT]
            weights = [0.62, 0.28, 0.10]
        else:
            actions = [Action.ADVANCE, Action.RETREAT, Action.GUARD]
            weights = [0.08, 0.10, 0.27]
            if view.self_attack_cd == 0:
                actions.append(Action.ATTACK)
                weights.append(0.34)
            if view.self_evade_cd == 0:
                actions.append(Action.EVADE)
                weights.append(0.21)
        if view.public_history:
            own_last = view.public_history[-1][0]
            for i, action in enumerate(actions):
                if action.value == own_last:
                    weights[i] *= 0.42
        return rng.choices(actions, weights=weights, k=1)[0]


class AdaptiveExploiterPolicy:
    """Fixed public-history transition learner for the v0.9 falsification test."""
    def _predict_opponent(self, view: FighterView) -> str | None:
        opp = [b for _, b in view.public_history]
        if not opp:
            return None
        transitions: dict[str, Counter] = defaultdict(Counter)
        for a, b in zip(opp, opp[1:]):
            transitions[a][b] += 1
        last = opp[-1]
        if transitions[last]:
            return transitions[last].most_common(1)[0][0]
        return Counter(opp).most_common(1)[0][0]

    def choose(self, view: FighterView, rng: random.Random) -> Action:
        predicted = self._predict_opponent(view)
        if view.distance > 1:
            if predicted == Action.RETREAT.value:
                return Action.ADVANCE
            return Action.ADVANCE if rng.random() < 0.82 else Action.GUARD
        if predicted == Action.ATTACK.value:
            return Action.EVADE if view.self_evade_cd == 0 else Action.GUARD
        if predicted == Action.RETREAT.value:
            return Action.ADVANCE
        if predicted == Action.ADVANCE.value and view.self_attack_cd == 0:
            return Action.ATTACK
        if predicted in (Action.GUARD.value, Action.EVADE.value):
            return Action.ADVANCE if rng.random() < 0.62 else Action.GUARD
        if view.self_attack_cd == 0:
            return Action.ATTACK
        return Action.GUARD
