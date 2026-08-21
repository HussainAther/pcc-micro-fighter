import json
from pathlib import Path

from pcc_micro_fighter.retreat_backfire import run_retreat_backfire_decomposition


def test_frozen_v08_retreat_backfire_result_reproduces():
    frozen = json.loads(Path('validation/retreat-backfire-decomposition.json').read_text())
    observed = run_retreat_backfire_decomposition(matches_per_order=400, seed=86001)
    assert observed == frozen
    assert observed['prespecified_checks']['v07_worse_than_v05'] is True
    assert observed['prespecified_checks']['initiative_forfeiture_proxy_at_least_0_50'] is True
    assert observed['prespecified_checks']['free_reentry_given_gain_at_least_0_25'] is True
    assert observed['prespecified_checks']['boundary_or_resolution_failure_at_least_0_20'] is True
    assert observed['prespecified_checks']['two_tick_displacement_persistence_below_0_50'] is True
