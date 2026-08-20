from pcc_micro_fighter.model import Action


def test_no_legal_action_is_named_after_pcc_axes():
    values = {a.value for a in Action}
    assert values.isdisjoint({"pressure", "control", "chaos"})
