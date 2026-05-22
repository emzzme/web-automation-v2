from xz_control_ui.services.demo_system import DemoSystem


def test_vna_settings_model_limits() -> None:
    s = DemoSystem()
    s.set_vna_settings("R&S ZNL14", start_ghz=0.001, stop_ghz=20.0, points=9, ifbw_hz=1_000_000.0, power_dbm=15.0)
    assert 0.005 <= s.vna_start_ghz <= 14.0
    assert s.vna_stop_ghz <= 14.0
    assert s.vna_points >= 11
    assert s.vna_ifbw_hz <= 500000.0
    assert s.vna_power_dbm <= 10.0

    s.set_vna_settings("Keysight N9917B", start_ghz=0.001, stop_ghz=50.0, points=5000, ifbw_hz=0.1, power_dbm=20.0)
    assert 0.03 <= s.vna_start_ghz <= 18.0
    assert s.vna_stop_ghz <= 18.0
    assert s.vna_points <= 4001
    assert s.vna_ifbw_hz >= 10.0
    assert s.vna_power_dbm <= 8.0
