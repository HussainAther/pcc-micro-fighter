import json
from pathlib import Path

from pcc_micro_fighter.residual_pressure import EXPECTED_V05_POLICY_SHA256


def test_residual_pressure_frozen_artifact_uses_v05_policy_hash():
    report = json.loads(Path("validation/residual-pressure-decomposition.json").read_text())
    assert report["design"]["expected_v05_policy_sha256"] == EXPECTED_V05_POLICY_SHA256
    assert report["design"]["observed_policy_sha256"] == EXPECTED_V05_POLICY_SHA256
    assert report["design"]["policy_hash_matches_expected"] is True


def test_residual_pressure_frozen_report_has_design_and_metrics():
    report = json.loads(Path("validation/residual-pressure-decomposition.json").read_text())
    assert report["design"]["policies_modified"] is False
    assert report["design"]["seat_order_balanced"] is True
    for key in (
        "control_defense_rate_vs_pressure_attacks",
        "mean_pressure_threat_run_length",
        "control_post_threat_recovery_rate",
        "damage_taken_during_sustained_threat_per_match",
        "pressure_reengagement_rate_after_control_hit",
    ):
        assert key in report["metrics"]
