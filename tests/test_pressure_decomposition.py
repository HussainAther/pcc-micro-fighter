from pcc_micro_fighter.pressure_decomposition import run_pressure_decomposition


def test_pressure_decomposition_is_balanced_and_read_only():
    r = run_pressure_decomposition(matches_per_order=8, seed=99)
    assert r["design"]["policies_modified"] is False
    assert r["design"]["seat_order_balanced"] is True
    assert set(r["families"]) == {"A", "B"}
    for family in r["families"].values():
        assert {x["opponent"] for x in family["standard_matchups"]} == {"control", "chaos"}
        for row in family["standard_matchups"]:
            assert "spatial_compression_per_tick" in row["pressure_minus_opponent"]
            assert "next_tick_defensive_response_rate" in row["pressure_minus_opponent"]
            assert "pressure_win_rate_change_when_starting_in_range" in row


def test_pressure_decomposition_deterministic():
    a = run_pressure_decomposition(matches_per_order=5, seed=1234)
    b = run_pressure_decomposition(matches_per_order=5, seed=1234)
    assert a == b
