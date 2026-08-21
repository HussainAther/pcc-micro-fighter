from pcc_micro_fighter.threat_conversion import run_threat_conversion


def test_threat_conversion_is_balanced_and_read_only():
    r = run_threat_conversion(matches_per_order=8, seed=71)
    assert r["status"] == "descriptive_threat_conversion_and_counter_value_decomposition"
    assert r["design"]["policies_modified"] is False
    assert r["design"]["seat_order_balanced"] is True
    assert set(r["families"]) == {"A", "B"}


def test_threat_conversion_reports_prespecified_exchange_metrics():
    r = run_threat_conversion(matches_per_order=8, seed=73)
    required = {
        "successful_defense_rate_per_opponent_attack",
        "counter_window_creation_rate",
        "counter_attack_take_rate",
        "counter_hit_rate_per_window",
        "cooldown_punishment_hit_rate",
        "damage_per_attack_opportunity",
        "damage_received_per_opponent_threat_tick",
        "positional_recovery_rate_after_defense",
        "net_damage_per_match",
    }
    for family in ("A", "B"):
        assert required <= set(r["families"][family]["control"])
