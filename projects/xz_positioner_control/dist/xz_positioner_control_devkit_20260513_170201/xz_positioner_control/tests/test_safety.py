from xz_control_ui.core.safety import SafetyController, SafetyInputs, SafetyState


def test_estop_latch_requires_manual_reset() -> None:
    s = SafetyController()
    s.update(SafetyInputs(estop_pressed=True))
    assert s.state == SafetyState.ESTOP_LATCHED
    assert not s.can_motion_start()

    ok = s.manual_reset(SafetyInputs(estop_pressed=False))
    assert ok
    assert s.state == SafetyState.READY


def test_limit_trips_and_recovers() -> None:
    s = SafetyController()
    s.update(SafetyInputs(x_limit=True))
    assert s.state == SafetyState.LIMIT_ACTIVE
    s.update(SafetyInputs(x_limit=False, z_limit=False))
    assert s.state == SafetyState.READY
