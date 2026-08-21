from pcc_micro_fighter.retreat_backfire import run_retreat_backfire_decomposition


def test_retreat_backfire_design_is_read_only_and_balanced():
    report = run_retreat_backfire_decomposition(matches_per_order=8, seed=86001)
    assert report["design"]["policies_modified"] is False
    assert report["design"]["seat_balanced"] is True
    assert len(report["design"]["prespecified_mechanisms"]) == 4


def test_retreat_backfire_has_v05_and_v07_comparison():
    report = run_retreat_backfire_decomposition(matches_per_order=8, seed=86001)
    assert "pressure_decisive_win_rate" in report["v0.5"]
    assert "retreat_backfire" in report["v0.7"]
    assert "two_tick_displacement_persistence_rate_given_gain" in report["v0.7"]["retreat_backfire"]
