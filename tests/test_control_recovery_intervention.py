import hashlib
import random
from pathlib import Path

from pcc_micro_fighter.control_recovery_intervention import EXPECTED_V07_POLICY_SHA256, run_control_recovery_intervention
from pcc_micro_fighter.model import Action, FighterView
from pcc_micro_fighter.policies import ControlPolicyB


def _view(history, distance=1, attack_cd=0, evade_cd=0):
    return FighterView(
        self_position=2,
        opponent_position=3,
        self_health=5,
        opponent_health=5,
        self_attack_cd=attack_cd,
        self_evade_cd=evade_cd,
        distance=distance,
        tick=len(history),
        public_history=tuple(history),
    )


def test_v07_policy_hash_is_frozen():
    observed = hashlib.sha256(Path("pcc_micro_fighter/policies.py").read_bytes()).hexdigest()
    assert observed == EXPECTED_V07_POLICY_SHA256


def test_v07_sustained_attack_prefers_defense():
    policy = ControlPolicyB()
    action = policy.choose(
        _view([("guard", "advance"), ("advance", "attack")], evade_cd=0),
        random.Random(1),
    )
    assert action == Action.EVADE


def test_v07_sustained_advance_prefers_spatial_recovery():
    policy = ControlPolicyB()
    action = policy.choose(
        _view([("guard", "attack"), ("advance", "advance")]),
        random.Random(1),
    )
    assert action == Action.RETREAT


def test_v07_intervention_keeps_original_gate_and_records_negative_result():
    report = run_control_recovery_intervention(matches_per_order=20, seed=42001)
    assert report["design"]["competitiveness_protocol_unchanged"] is True
    assert report["design"]["decisive_win_rate_window"] == [0.30, 0.70]
    assert report["design"]["cycle_required"] is False
    assert report["design"]["policy_hash_matches_expected"] is True
