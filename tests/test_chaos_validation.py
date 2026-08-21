from pcc_micro_fighter.chaos_policies import (
    AdaptiveExploiterPolicy, EffectiveChaosPolicy, PredictableCompetentPolicy, StateRandomPolicy,
)
from pcc_micro_fighter.chaos_validation import chaos_validation
from pcc_micro_fighter.engine import simulate_match


def test_chaos_policies_run():
    policies = [PredictableCompetentPolicy, StateRandomPolicy, EffectiveChaosPolicy, AdaptiveExploiterPolicy]
    for i, p in enumerate(policies):
        r = simulate_match(p(), PredictableCompetentPolicy(), 9000 + i)
        assert r.ticks > 0


def test_chaos_validation_schema_small():
    report = chaos_validation(matches_per_order=8, seed=12345)
    assert set(report["results"]) == {"predictable_competent", "state_random", "effective_chaos"}
    assert len(report["prespecified_checks"]) == 4
    assert isinstance(report["effective_chaos_confirmed"], bool)


def test_entropy_is_bounded_small():
    report = chaos_validation(matches_per_order=8, seed=23456)
    for row in report["results"].values():
        assert 0.0 <= row["neutral"]["conditional_action_entropy"] <= 1.0
        assert 0.0 <= row["adaptive_exploiter"]["conditional_action_entropy"] <= 1.0
