from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


class Action(str, Enum):
    ADVANCE = "advance"
    RETREAT = "retreat"
    ATTACK = "attack"
    GUARD = "guard"
    EVADE = "evade"


@dataclass(frozen=True)
class Rules:
    arena_min: int = 0
    arena_max: int = 6
    starting_health: int = 5
    attack_range: int = 1
    attack_damage: int = 1
    attack_cooldown: int = 1
    evade_cooldown: int = 1
    max_ticks: int = 80


@dataclass
class FighterState:
    position: int
    health: int
    attack_cd: int = 0
    evade_cd: int = 0


@dataclass
class FighterView:
    self_position: int
    opponent_position: int
    self_health: int
    opponent_health: int
    self_attack_cd: int
    self_evade_cd: int
    distance: int
    tick: int
    public_history: Tuple[Tuple[str, str], ...]


@dataclass
class TickRecord:
    tick: int
    action0: str
    action1: str
    before_positions: Tuple[int, int]
    after_positions: Tuple[int, int]
    before_health: Tuple[int, int]
    after_health: Tuple[int, int]
    hit0: bool
    hit1: bool


@dataclass
class MatchResult:
    winner: int | None
    ticks: int
    health: Tuple[int, int]
    records: List[TickRecord] = field(default_factory=list)
