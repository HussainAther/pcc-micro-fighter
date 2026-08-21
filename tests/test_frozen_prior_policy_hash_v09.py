import hashlib
from pathlib import Path


def test_prior_pcc_policy_file_unchanged_for_v09_chaos_experiment():
    root = Path(__file__).resolve().parents[1]
    observed = hashlib.sha256((root / "pcc_micro_fighter/policies.py").read_bytes()).hexdigest()
    assert observed == "e978208580f4e09dabae087f202c10a074e20e3a6560016acce2580865e55347"
