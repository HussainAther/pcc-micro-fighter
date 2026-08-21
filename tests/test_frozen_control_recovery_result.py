import json
from pathlib import Path

from pcc_micro_fighter.control_recovery_intervention import run_control_recovery_intervention


def test_frozen_v07_result_retains_negative_intervention_and_reproduces():
    frozen = json.loads(Path("validation/control-recovery-intervention-v0.7.0.json").read_text())
    observed = run_control_recovery_intervention(matches_per_order=400, seed=42001)
    assert observed == frozen
    target = frozen["target_matchup"]
    assert frozen["competitiveness_confirmed_after_intervention"] is False
    assert target["moved_toward_competitiveness"] is False
    assert target["v07_pressure_decisive_win_rate"] > target["v05_pressure_decisive_win_rate"]
    assert frozen["collateral_matchup"]["remained_competitive"] is True
