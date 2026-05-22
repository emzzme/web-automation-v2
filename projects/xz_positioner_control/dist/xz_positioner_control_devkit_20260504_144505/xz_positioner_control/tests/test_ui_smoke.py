from xz_control_ui.main import MainWindow


def test_main_window_smoke(qtbot) -> None:
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()
    assert w.windowTitle() != ""
    assert w.progress.maximum() == 100
