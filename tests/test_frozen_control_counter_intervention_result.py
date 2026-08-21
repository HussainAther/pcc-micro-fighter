import json
from pathlib import Path


def test_frozen_v05_result_is_partial_improvement_not_rebalance():
    root = Path(__file__).resolve().parents[1]
    r = json.loads((root / 'validation' / 'control-counter-intervention-v0.5.0.json').read_text())
    assert r['competitiveness_confirmed_after_intervention'] is False
    assert r['target_matchup']['moved_toward_competitiveness'] is True
    assert r['target_matchup']['competitive_after_intervention'] is False
    assert abs(r['target_matchup']['baseline_pressure_decisive_win_rate'] - 0.9310344827586207) < 1e-12
    assert abs(r['target_matchup']['v05_pressure_decisive_win_rate'] - 0.8211829436038515) < 1e-12
    assert r['collateral_matchup']['remained_competitive'] is True
