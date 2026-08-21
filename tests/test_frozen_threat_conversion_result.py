import json
from pathlib import Path


def test_frozen_v04_result_preserves_family_split():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "validation" / "threat-conversion-decomposition.json").read_text())
    a = report["families"]["A"]
    b = report["families"]["B"]
    assert a["pressure_decisive_win_rate"] == 0.0
    assert b["pressure_decisive_win_rate"] > 0.9
    assert a["control"]["successful_defense_rate_per_opponent_attack"] > b["control"]["successful_defense_rate_per_opponent_attack"]
    assert a["control"]["counter_hit_rate_per_window"] > 0.20
    assert b["control"]["counter_hit_rate_per_window"] < 0.02
    # Opportunity efficiency itself is not the key family separator.
    assert abs(a["control"]["damage_per_attack_opportunity"] - b["control"]["damage_per_attack_opportunity"]) < 0.02
