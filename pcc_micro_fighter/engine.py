from __future__ import annotations
from typing import Protocol
import random

from .model import Action, FighterState, FighterView, MatchResult, Rules, TickRecord


class Policy(Protocol):
    def choose(self, view: FighterView, rng: random.Random) -> Action: ...


def _view(me: FighterState, opp: FighterState, tick: int, history, rules: Rules) -> FighterView:
    return FighterView(
        self_position=me.position,
        opponent_position=opp.position,
        self_health=me.health,
        opponent_health=opp.health,
        self_attack_cd=me.attack_cd,
        self_evade_cd=me.evade_cd,
        distance=abs(me.position - opp.position),
        tick=tick,
        public_history=tuple(history),
    )


def _move_toward(pos: int, opp: int) -> int:
    if pos < opp:
        return pos + 1
    if pos > opp:
        return pos - 1
    return pos


def _move_away(pos: int, opp: int, rules: Rules) -> int:
    if pos < opp:
        return max(rules.arena_min, pos - 1)
    if pos > opp:
        return min(rules.arena_max, pos + 1)
    return pos


def simulate_match(policy0: Policy, policy1: Policy, seed: int = 1, rules: Rules | None = None) -> MatchResult:
    rules = rules or Rules()
    rng0 = random.Random(seed * 2 + 1)
    rng1 = random.Random(seed * 2 + 2)
    s0 = FighterState(rules.arena_min + 1, rules.starting_health)
    s1 = FighterState(rules.arena_max - 1, rules.starting_health)
    history: list[tuple[str, str]] = []
    records: list[TickRecord] = []

    for tick in range(rules.max_ticks):
        a0 = policy0.choose(_view(s0, s1, tick, history, rules), rng0)
        a1 = policy1.choose(_view(s1, s0, tick, [(b, a) for a, b in history], rules), rng1)
        before_pos = (s0.position, s1.position)
        before_hp = (s0.health, s1.health)

        # simultaneous movement resolution
        n0, n1 = s0.position, s1.position
        if a0 == Action.ADVANCE:
            n0 = _move_toward(s0.position, s1.position)
        elif a0 == Action.RETREAT:
            n0 = _move_away(s0.position, s1.position, rules)
        if a1 == Action.ADVANCE:
            n1 = _move_toward(s1.position, s0.position)
        elif a1 == Action.RETREAT:
            n1 = _move_away(s1.position, s0.position, rules)

        # fighters may share a cell; distance zero means clinch range
        s0.position, s1.position = n0, n1
        distance = abs(s0.position - s1.position)

        can_hit0 = a0 == Action.ATTACK and s0.attack_cd == 0 and distance <= rules.attack_range
        can_hit1 = a1 == Action.ATTACK and s1.attack_cd == 0 and distance <= rules.attack_range

        def defended(opp_action: Action) -> bool:
            return opp_action in (Action.GUARD, Action.EVADE)

        hit0 = bool(can_hit0 and not defended(a1))
        hit1 = bool(can_hit1 and not defended(a0))

        if hit0:
            s1.health -= rules.attack_damage
        if hit1:
            s0.health -= rules.attack_damage

        # cooldown bookkeeping
        s0.attack_cd = rules.attack_cooldown if a0 == Action.ATTACK else max(0, s0.attack_cd - 1)
        s1.attack_cd = rules.attack_cooldown if a1 == Action.ATTACK else max(0, s1.attack_cd - 1)
        s0.evade_cd = rules.evade_cooldown if a0 == Action.EVADE else max(0, s0.evade_cd - 1)
        s1.evade_cd = rules.evade_cooldown if a1 == Action.EVADE else max(0, s1.evade_cd - 1)

        records.append(TickRecord(
            tick=tick,
            action0=a0.value,
            action1=a1.value,
            before_positions=before_pos,
            after_positions=(s0.position, s1.position),
            before_health=before_hp,
            after_health=(s0.health, s1.health),
            hit0=hit0,
            hit1=hit1,
        ))
        history.append((a0.value, a1.value))

        if s0.health <= 0 or s1.health <= 0:
            break

    winner = None
    if s0.health > s1.health:
        winner = 0
    elif s1.health > s0.health:
        winner = 1
    return MatchResult(winner=winner, ticks=len(records), health=(s0.health, s1.health), records=records)
