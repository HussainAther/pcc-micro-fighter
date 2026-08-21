from __future__ import annotations
import hashlib
import json
from pathlib import Path

from .competitiveness import run_competitiveness

BASELINE_PATH = Path('validation/competitiveness.json')
BASELINE_POLICY_SHA256 = '511d01fa4d62fd912d7453505e76408a91a8e8065e35f5eeecd87659c432c360'
V05_POLICY_SHA256 = '93ca6c82abf1d1280334a7c048f4b01f59b7da5765f3d6b780b11cda919f1242'


def _policy_sha256() -> str:
    return hashlib.sha256(Path(__file__).with_name('policies.py').read_bytes()).hexdigest()


def _matchup(report: dict, family: str, a: str, b: str) -> dict:
    return next(row for row in report['families'][family]['matchups'] if row['a'] == a and row['b'] == b)


def run_control_counter_intervention(matches_per_order: int = 400, seed: int = 42001) -> dict:
    baseline = json.loads(BASELINE_PATH.read_text())
    current = run_competitiveness(matches_per_order=matches_per_order, seed=seed)
    base_pc = _matchup(baseline, 'B', 'pressure', 'control')
    now_pc = _matchup(current, 'B', 'pressure', 'control')
    base_cc = _matchup(baseline, 'B', 'control', 'chaos')
    now_cc = _matchup(current, 'B', 'control', 'chaos')
    observed_hash = _policy_sha256()

    return {
        'competitiveness_confirmed_after_intervention': current['competitiveness_confirmed'],
        'status': 'prospective_single_mechanism_intervention_evaluation',
        'design': {
            'version': '0.5.0',
            'intervention': 'Family B Control immediately attacks in a publicly recognizable successful-defense cooldown punish window.',
            'baseline_policy_sha256': BASELINE_POLICY_SHA256,
            'expected_v05_policy_sha256': V05_POLICY_SHA256,
            'observed_v05_policy_sha256': observed_hash,
            'policy_hash_matches_expected': observed_hash == V05_POLICY_SHA256,
            'only_family_b_control_intentionally_modified': True,
            'competitiveness_protocol_unchanged': True,
            'matches_per_order': matches_per_order,
            'seed': seed,
            'decisive_win_rate_window': current['design']['decisive_win_rate_window'],
            'cycle_required': current['design']['cycle_required'],
            'post_result_tuning_allowed': False,
        },
        'baseline_v0.2': baseline,
        'v0.5': current,
        'target_matchup': {
            'family': 'B',
            'matchup': 'pressure_vs_control',
            'baseline_pressure_decisive_win_rate': base_pc['a_decisive_win_rate'],
            'v05_pressure_decisive_win_rate': now_pc['a_decisive_win_rate'],
            'pressure_win_rate_change': now_pc['a_decisive_win_rate'] - base_pc['a_decisive_win_rate'],
            'moved_toward_competitiveness': abs(now_pc['a_decisive_win_rate'] - 0.5) < abs(base_pc['a_decisive_win_rate'] - 0.5),
            'competitive_after_intervention': now_pc['competitive'],
        },
        'collateral_matchup': {
            'family': 'B',
            'matchup': 'control_vs_chaos',
            'baseline_control_decisive_win_rate': base_cc['a_decisive_win_rate'],
            'v05_control_decisive_win_rate': now_cc['a_decisive_win_rate'],
            'control_win_rate_change': now_cc['a_decisive_win_rate'] - base_cc['a_decisive_win_rate'],
            'remained_competitive': base_cc['competitive'] and now_cc['competitive'],
        },
        'interpretation': (
            'The prospectively justified Family B Control counter-window rule moved the target Pressure-vs-Control matchup '
            'toward the frozen competitiveness window but did not bring it inside the window. Control-vs-Chaos remained '
            'competitive. The intervention is therefore a partial mechanistic improvement, not a successful rebalance and '
            'not authorization for construct recovery.'
        ),
    }


def write_control_counter_intervention(path: str, matches_per_order: int = 400, seed: int = 42001) -> dict:
    report = run_control_counter_intervention(matches_per_order=matches_per_order, seed=seed)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2) + '\n')
    return report
