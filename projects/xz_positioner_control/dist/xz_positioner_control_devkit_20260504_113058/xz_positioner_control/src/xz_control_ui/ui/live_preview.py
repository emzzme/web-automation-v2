from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QFile, QFileSystemWatcher, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class UiPreviewWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui_path = Path(__file__).parent / "main_window.ui"
        self.qss_path = Path(__file__).parent / "theme.qss"
        self._watcher = QFileSystemWatcher(self)
        self._watcher.addPath(str(self.ui_path))
        self._watcher.addPath(str(self.qss_path))
        self._watcher.fileChanged.connect(self._reload_ui)
        self._load_ui()

    def _load_ui(self) -> None:
        loader = QUiLoader()
        ui_file = QFile(str(self.ui_path))
        if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"UI acilamadi: {self.ui_path}")
        loaded = loader.load(ui_file, self)
        ui_file.close()
        if loaded is None:
            raise RuntimeError(f"UI yuklenemedi: {ui_file}")

        self.setWindowTitle(loaded.windowTitle())
        self.resize(loaded.size())

        central = loaded.findChild(QWidget, "centralwidget") or loaded.centralWidget()
        if central is None:
            central = QWidget(self)

        host = QWidget(self)
        lay = QVBoxLayout(host)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(central)
        self.setCentralWidget(host)

        if self.qss_path.exists():
            self.setStyleSheet(self.qss_path.read_text(encoding="utf-8"))

    def _reload_ui(self, _path: str) -> None:
        # Watcher on Windows may drop watched file after change; add back.
        if str(self.ui_path) not in self._watcher.files() and self.ui_path.exists():
            self._watcher.addPath(str(self.ui_path))
        if str(self.qss_path) not in self._watcher.files() and self.qss_path.exists():
            self._watcher.addPath(str(self.qss_path))

        old = self.centralWidget()
        self._load_ui()
        if old is not None:
            old.deleteLater()


def run() -> None:
    app = QApplication(sys.argv)
    w = UiPreviewWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
