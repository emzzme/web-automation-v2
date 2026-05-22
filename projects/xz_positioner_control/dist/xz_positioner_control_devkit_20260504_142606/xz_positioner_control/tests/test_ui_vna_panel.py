from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from xz_control_ui.main import MainWindow


def _find_button(window: MainWindow, text: str) -> QPushButton:
    for b in window.findChildren(QPushButton):
        if b.text() == text:
            return b
    raise AssertionError(f"Button not found: {text}")


def test_ui_apply_vna_settings_button(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()
    qtbot.mouseClick(_find_button(w, "VNA Ayarlari Uygula"), Qt.MouseButton.LeftButton)
    assert w.log_table.rowCount() >= 1
