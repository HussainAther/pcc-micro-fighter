import random
from pcc_micro_fighter.model import FighterView, Action
from pcc_micro_fighter.policies import PressurePolicy, ControlPolicy, ChaosPolicy


def v(distance=4, history=()):
    return FighterView(1, 1+distance, 5, 5, 0, 0, distance, 10, tuple(history))


def test_pressure_tends_to_advance_at_range():
    rng = random.Random(1)
    xs = [PressurePolicy().choose(v(4), rng) for _ in range(200)]
    assert xs.count(Action.ADVANCE) > xs.count(Action.GUARD)


def test_control_responds_to_attack_history():
    h = (("guard","attack"),)*6
    a = ControlPolicy().choose(v(1,h), random.Random(1))
    assert a in (Action.EVADE, Action.GUARD)


def test_chaos_policy_uses_multiple_actions():
    rng = random.Random(2)
    xs = {ChaosPolicy().choose(v(1), rng) for _ in range(100)}
    assert len(xs) >= 3


def test_family_b_control_takes_public_counter_window():
    from pcc_micro_fighter.policies import ControlPolicyB
    history = (("guard", "attack"),)
    view = FighterView(2, 3, 5, 5, 0, 0, 1, 11, history)
    assert ControlPolicyB().choose(view, random.Random(7)) == Action.ATTACK


def test_family_b_control_counter_rule_requires_in_range_and_clear_attack_cd():
    from pcc_micro_fighter.policies import ControlPolicyB
    history = (("guard", "attack"),)
    far = FighterView(1, 4, 5, 5, 0, 0, 3, 11, history)
    cooling = FighterView(2, 3, 5, 5, 1, 0, 1, 11, history)
    assert ControlPolicyB().choose(far, random.Random(7)) != Action.ATTACK
    assert ControlPolicyB().choose(cooling, random.Random(7)) != Action.ATTACK
