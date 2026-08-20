from pcc_micro_fighter.engine import simulate_match
from pcc_micro_fighter.model import Action, FighterView, Rules


class AlwaysAttack:
    def choose(self, view, rng): return Action.ATTACK
class AlwaysAdvance:
    def choose(self, view, rng): return Action.ADVANCE
class AlwaysGuard:
    def choose(self, view, rng): return Action.GUARD


def test_deterministic_seed():
    a = simulate_match(AlwaysAdvance(), AlwaysGuard(), seed=7)
    b = simulate_match(AlwaysAdvance(), AlwaysGuard(), seed=7)
    assert [(r.action0, r.action1, r.after_positions) for r in a.records] == [(r.action0, r.action1, r.after_positions) for r in b.records]


def test_guard_blocks_attacks():
    rules = Rules(max_ticks=6)
    r = simulate_match(AlwaysAttack(), AlwaysGuard(), seed=2, rules=rules)
    assert r.health[1] == rules.starting_health


def test_match_stays_bounded():
    r = simulate_match(AlwaysAdvance(), AlwaysAdvance(), seed=3)
    assert r.ticks <= Rules().max_ticks
    for rec in r.records:
        assert all(Rules().arena_min <= p <= Rules().arena_max for p in rec.after_positions)
