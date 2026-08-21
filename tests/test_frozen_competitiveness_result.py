import json
from pathlib import Path


def test_frozen_v02_competitiveness_result_is_retained_as_failure():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "validation" / "competitiveness.json").read_text())
    assert report["competitiveness_confirmed"] is False
    assert report["design"]["cycle_required"] is False
    assert report["design"]["post_result_tuning_allowed"] is False
    assert report["families"]["A"]["all_pairwise_matchups_competitive"] is False
    assert report["families"]["B"]["all_pairwise_matchups_competitive"] is False
    assert sum(r["competitive"] for r in report["families"]["B"]["matchups"]) == 1
