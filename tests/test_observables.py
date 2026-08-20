from pcc_micro_fighter.engine import simulate_match
from pcc_micro_fighter.observables import summarize
from pcc_micro_fighter.policies import PressurePolicy, NeutralPolicy


def test_summary_fields_present():
    r = simulate_match(PressurePolicy(), NeutralPolicy(), seed=11)
    s = summarize(r, 0)
    for key in ["advance_rate","attack_rate","spatial_constriction","action_entropy","net_damage"]:
        assert key in s
