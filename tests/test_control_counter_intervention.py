import json
from pathlib import Path


def test_v05_intervention_frozen_artifact_uses_original_competitiveness_protocol():
    report = json.loads(Path("validation/control-counter-intervention-v0.5.0.json").read_text())
    assert report["design"]["competitiveness_protocol_unchanged"] is True
    assert report["design"]["decisive_win_rate_window"] == [0.30, 0.70]
    assert report["design"]["cycle_required"] is False
    assert report["design"]["only_family_b_control_intentionally_modified"] is True
    assert report["design"]["policy_hash_matches_expected"] is True
