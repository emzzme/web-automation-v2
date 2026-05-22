from xz_control_ui.services.ttl_adapter import TtlDigitalIoAdapter


def test_ttl_trigger_and_inputs() -> None:
    ttl = TtlDigitalIoAdapter()
    ttl.pulse_trigger()
    ttl.pulse_trigger()
    assert ttl.trigger_count == 2

    ttl.set_input("x_limit", True)
    data = ttl.read_inputs()
    assert data["x_limit"] is True
