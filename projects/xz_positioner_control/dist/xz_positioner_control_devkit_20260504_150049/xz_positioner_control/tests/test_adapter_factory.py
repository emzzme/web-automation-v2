from pathlib import Path

from xz_control_ui.services.adapter_factory import build_adapters_from_activation
from xz_control_ui.services.controller_adapters import ControllerSerialAdapter, ControllerTcpAdapter


def test_factory_builds_serial_controller_for_usb() -> None:
    cfg = Path("config/activation.json")
    bundle = build_adapters_from_activation(cfg, use_mock_vna=True)
    assert isinstance(bundle.controller, ControllerSerialAdapter)
    assert bundle.controller.connect()


def test_factory_builds_tcp_controller_for_ethernet() -> None:
    p = Path("state/test_activation_ethernet.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        p.write_text(
            '{"controller_transport":"ETHERNET","controller_target":"10.0.0.2:4000","vna_transport":"LAN","vna_target":"10.0.21.151","trigger_mode":"TTL_STEP"}',
            encoding="utf-8",
        )
        bundle = build_adapters_from_activation(p, use_mock_vna=True)
    finally:
        if p.exists():
            p.unlink()
    assert isinstance(bundle.controller, ControllerTcpAdapter)
