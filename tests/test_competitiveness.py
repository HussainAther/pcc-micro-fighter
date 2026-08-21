from pcc_micro_fighter.competitiveness import MIN_WIN_RATE, MAX_WIN_RATE, run_competitiveness
from pcc_micro_fighter.policies import POLICY_FAMILIES, PressurePolicy, PressurePolicyB


def test_two_policy_families_are_registered_and_distinct():
    assert set(POLICY_FAMILIES) == {"A", "B"}
    assert POLICY_FAMILIES["A"]["pressure"] is PressurePolicy
    assert POLICY_FAMILIES["B"]["pressure"] is PressurePolicyB
    for mode in ("pressure", "control", "chaos"):
        assert POLICY_FAMILIES["A"][mode] is not POLICY_FAMILIES["B"][mode]


def test_competitiveness_protocol_does_not_require_cycle():
    report = run_competitiveness(matches_per_order=5, seed=901)
    assert report["design"]["cycle_required"] is False
    assert report["design"]["decisive_win_rate_window"] == [MIN_WIN_RATE, MAX_WIN_RATE]


def test_competitiveness_report_has_all_pairwise_rows():
    report = run_competitiveness(matches_per_order=5, seed=902)
    for family in ("A", "B"):
        rows = report["families"][family]["matchups"]
        assert {(r["a"], r["b"]) for r in rows} == {
            ("pressure", "control"),
            ("pressure", "chaos"),
            ("control", "chaos"),
        }
        for row in rows:
            assert 0.0 <= row["a_decisive_win_rate"] <= 1.0
