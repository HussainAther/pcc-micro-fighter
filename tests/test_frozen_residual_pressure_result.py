import json
from pathlib import Path


def test_frozen_residual_pressure_result_is_retained():
    frozen = json.loads(Path("validation/residual-pressure-decomposition.json").read_text())
    assert frozen["matchup"]["pressure_decisive_win_rate"] > 0.70
    assert frozen["metrics"]["control_defense_rate_vs_pressure_attacks"] < 0.50
    assert frozen["metrics"]["control_post_threat_recovery_rate"] < 0.10
    assert frozen["metrics"]["pressure_reengagement_rate_after_successful_defense"] < 0.50
    assert frozen["design"]["policy_hash_matches_expected"] is True
