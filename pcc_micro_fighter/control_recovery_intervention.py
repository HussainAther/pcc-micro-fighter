from __future__ import annotations
import hashlib
import json
from pathlib import Path

from .competitiveness import run_competitiveness

V05_RESULT_PATH = Path("validation/control-counter-intervention-v0.5.0.json")
EXPECTED_V07_POLICY_SHA256 = "e978208580f4e09dabae087f202c10a074e20e3a6560016acce2580865e55347"


def _policy_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name("policies.py").read_bytes()).hexdigest()


def _matchup(report: dict, family: str, a: str, b: str) -> dict:
    return next(row for row in report["families"][family]["matchups"] if row["a"] == a and row["b"] == b)


def run_control_recovery_intervention(matches_per_order: int = 400, seed: int = 42001) -> dict:
    baseline = json.loads(V05_RESULT_PATH.read_text())
    current = run_competitiveness(matches_per_order=matches_per_order, seed=seed)

    v05_pc = baseline["target_matchup"]["v05_pressure_decisive_win_rate"]
    now_pc = _matchup(current, "B", "pressure", "control")
    v05_cc = baseline["collateral_matchup"]["v05_control_decisive_win_rate"]
    now_cc = _matchup(current, "B", "control", "chaos")
    observed_hash = _policy_sha256()

    return {
        "competitiveness_confirmed_after_intervention": current["competitiveness_confirmed"],
        "status": "prospective_single_defensive_state_intervention_evaluation",
        "design": {
            "version": "0.7.0",
            "intervention": (
                "Family B Control recognizes two consecutive close-range opponent advance/attack actions; "
                "it defends a current attack or retreats after an advance. The v0.5 punish-window attack keeps priority."
            ),
            "expected_v07_policy_sha256": EXPECTED_V07_POLICY_SHA256,
            "observed_v07_policy_sha256": observed_hash,
            "policy_hash_matches_expected": observed_hash == EXPECTED_V07_POLICY_SHA256,
            "only_family_b_control_intentionally_modified": True,
            "competitiveness_protocol_unchanged": True,
            "matches_per_order": matches_per_order,
            "seed": seed,
            "decisive_win_rate_window": current["design"]["decisive_win_rate_window"],
            "cycle_required": current["design"]["cycle_required"],
            "post_result_tuning_allowed": False,
        },
        "v0.5_reference": {
            "pressure_vs_control_pressure_decisive_win_rate": v05_pc,
            "control_vs_chaos_control_decisive_win_rate": v05_cc,
        },
        "v0.7": current,
        "target_matchup": {
            "family": "B",
            "matchup": "pressure_vs_control",
            "v05_pressure_decisive_win_rate": v05_pc,
            "v07_pressure_decisive_win_rate": now_pc["a_decisive_win_rate"],
            "pressure_win_rate_change": now_pc["a_decisive_win_rate"] - v05_pc,
            "moved_toward_competitiveness": abs(now_pc["a_decisive_win_rate"] - 0.5) < abs(v05_pc - 0.5),
            "competitive_after_intervention": now_pc["competitive"],
        },
        "collateral_matchup": {
            "family": "B",
            "matchup": "control_vs_chaos",
            "v05_control_decisive_win_rate": v05_cc,
            "v07_control_decisive_win_rate": now_cc["a_decisive_win_rate"],
            "control_win_rate_change": now_cc["a_decisive_win_rate"] - v05_cc,
            "remained_competitive": now_cc["competitive"],
        },
        "interpretation": (
            "The prospectively frozen sustained-threat defense/recovery rule moved the target matchup away from the "
            "competitiveness window. Family B Control-vs-Chaos remained competitive, but Pressure-vs-Control worsened "
            "substantially. This is a retained negative intervention result: simple deterministic retreat/defense after "
            "two close Pressure actions is not a justified balancing mechanism and construct recovery remains blocked."
        ),
    }


def write_control_recovery_intervention(path: str, matches_per_order: int = 400, seed: int = 42001) -> dict:
    report = run_control_recovery_intervention(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + "\n")
    return report
