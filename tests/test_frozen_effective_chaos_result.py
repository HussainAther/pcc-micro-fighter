import json
from pathlib import Path

from pcc_micro_fighter.chaos_validation import chaos_validation


def test_frozen_effective_chaos_result_reproduces():
    root = Path(__file__).resolve().parents[1]
    frozen = json.loads((root / "validation/effective-chaos-validation-v0.9.0.json").read_text())
    observed = chaos_validation(matches_per_order=400, seed=97001)
    assert observed == frozen


def test_chaos_is_not_randomness_in_frozen_result():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "validation/effective-chaos-validation-v0.9.0.json").read_text())
    random_row = report["results"]["state_random"]["neutral"]
    chaos_row = report["results"]["effective_chaos"]["neutral"]
    assert random_row["conditional_action_entropy"] > chaos_row["conditional_action_entropy"]
    assert chaos_row["mean_health_margin"] > random_row["mean_health_margin"]
    assert chaos_row["decisive_win_rate"] > random_row["decisive_win_rate"]
    assert report["effective_chaos_confirmed"] is True
