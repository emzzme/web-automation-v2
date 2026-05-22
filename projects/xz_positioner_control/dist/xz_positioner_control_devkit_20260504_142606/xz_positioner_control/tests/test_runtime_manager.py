from pathlib import Path

from xz_control_ui.services.runtime_manager import RuntimeManager


def test_runtime_manager_demo_mode() -> None:
    rm = RuntimeManager(Path("config/activation.json"))
    st = rm.set_mode("DEMO")
    assert st.connected
    assert st.mode == "DEMO"


def test_runtime_manager_hardware_mock_dry_run() -> None:
    rm = RuntimeManager(Path("config/activation.json"))
    st = rm.set_mode("HARDWARE", use_mock_vna=True)
    assert st.connected
    dr = rm.dry_run()
    assert dr.connected
    comp = rm.component_status()
    assert set(comp.keys()) == {"controller", "vna", "ttl"}
