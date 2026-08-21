import json
from pathlib import Path


def test_frozen_v03_pressure_decomposition_result():
    root = Path(__file__).resolve().parents[1]
    r = json.loads((root / "validation" / "pressure-dominance-decomposition.json").read_text())
    d = r["replicated_diagnostics"]
    assert d["space_capture"]["replicated_expected_direction"] is True
    assert d["attack_opportunity_generation"]["replicated_expected_direction"] is True
    assert d["defensive_response_forcing"]["replicated_expected_direction"] is True
    assert d["damage_conversion"]["replicated_expected_direction"] is False
    assert d["spatial_access_dependency"]["pressure_advantage_reduced_in_all_matchups"] is False
    a_control = next(x for x in r["families"]["A"]["standard_matchups"] if x["opponent"] == "control")
    assert a_control["pressure_decisive_win_rate"] == 0.0
    assert a_control["pressure_minus_opponent"]["net_damage_per_match"] < 0
