from xz_control_ui.core.models import ScanRecipe
from xz_control_ui.services.demo_system import DemoSystem


def test_manual_jog_and_tick_moves_axis() -> None:
    s = DemoSystem()
    x0 = s.x.position_mm
    s.jog("x", 100.0)
    for _ in range(8):
        s.tick(0.25)
    assert s.x.position_mm > x0


def test_home_and_park_queue_paths() -> None:
    s = DemoSystem()
    s.home()
    for _ in range(20):
        s.tick(0.25)
    assert s.x.target_mm == 0.0
    assert s.z.target_mm == 0.0

    s.park()
    for _ in range(20):
        s.tick(0.25)
    assert s.x.target_mm == 100.0
    assert s.z.target_mm == 100.0


def test_recipe_and_scan_progress() -> None:
    s = DemoSystem()
    r = ScanRecipe(x_start_mm=0.0, x_stop_mm=200.0, x_step_mm=100.0, z_start_mm=0.0, z_stop_mm=100.0, z_step_mm=100.0)
    s.apply_recipe(r)
    s.start_scan()
    for _ in range(120):
        t = s.tick(0.25)
    assert t.progress.total_points >= 1
    assert t.progress.completed_points > 0


def test_estop_blocks_motion_until_reset() -> None:
    s = DemoSystem()
    s.estop_press()
    s.jog("x", 50.0)
    s.tick(0.25)
    assert s.mode in {"ESTOP_LATCHED", "STOPPED", "SAFE_LOCK"}

    s.estop_reset()
    s.jog("x", 50.0)
    for _ in range(4):
        s.tick(0.25)
    assert s.x.target_mm >= s.x.position_mm


def test_limit_sets_mode_and_alarm() -> None:
    s = DemoSystem()
    s.set_limit_state(True, False)
    s.tick(0.25)
    assert s.mode in {"LIMIT_ACTIVE", "STOPPED"}
    assert any("limit" in a.lower() for a in s.alarms)


def test_watchdog_fault_alarm() -> None:
    s = DemoSystem()
    s.watchdog.timeout_s = 0.05
    s.watchdog._last_beat -= 1.0
    s.tick(0.25)
    assert s.mode == "FAULT"
    assert any("heartbeat timeout" in a.lower() for a in s.alarms)
