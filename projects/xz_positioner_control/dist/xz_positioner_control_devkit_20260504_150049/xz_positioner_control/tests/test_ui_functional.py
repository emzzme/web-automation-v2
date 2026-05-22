from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from xz_control_ui.main import MainWindow


def _find_button(window: MainWindow, text: str) -> QPushButton:
    for b in window.findChildren(QPushButton):
        if b.text() == text:
            return b
    raise AssertionError(f"Button not found: {text}")


def test_ui_manual_buttons_and_log(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()

    # Speed apply path
    w.x_speed.setText("180")
    w.z_speed.setText("170")
    qtbot.mouseClick(_find_button(w, "Hiz Uygula"), Qt.MouseButton.LeftButton)

    # Jog path
    qtbot.mouseClick(_find_button(w, "X Jog +"), Qt.MouseButton.LeftButton)
    for _ in range(5):
        w._tick()
    assert "X Konum" in w.x_label.text()

    # E-stop path
    qtbot.mouseClick(_find_button(w, "E-STOP"), Qt.MouseButton.LeftButton)
    w._tick()
    assert "Safety" in w.safety_label.text()


def test_ui_runtime_mode_and_dry_run(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()

    w.runtime_mode.setCurrentText("HARDWARE")
    qtbot.mouseClick(_find_button(w, "Dry-Run"), Qt.MouseButton.LeftButton)

    assert w.log_table.rowCount() >= 1


def test_ui_self_check_updates_log_and_led(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()

    before = w.log_table.rowCount()
    qtbot.mouseClick(_find_button(w, "Self-Check"), Qt.MouseButton.LeftButton)
    after = w.log_table.rowCount()
    assert after > before


def test_ui_gain_and_scan_overview_updates(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()

    qtbot.mouseClick(_find_button(w, "Receteyi Uygula"), Qt.MouseButton.LeftButton)
    qtbot.mouseClick(_find_button(w, "Baslat"), Qt.MouseButton.LeftButton)
    for _ in range(8):
        w._tick()

    assert "Gain (Peak):" in w.gain_label.text()
    assert len(w.scan_overview_unscanned.points()) >= 0
    assert len(w.scan_overview_current.points()) >= 1
