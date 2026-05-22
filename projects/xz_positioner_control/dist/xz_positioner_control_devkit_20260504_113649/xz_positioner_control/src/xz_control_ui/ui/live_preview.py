from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import QApplication

# Live preview now uses the full legacy demo UI so all features remain visible.
os.environ["XZ_UI_MODE"] = "legacy"

from xz_control_ui.main import MainWindow


class FullDemoPreview(MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._watcher = QFileSystemWatcher(self)
        self.qss_path = Path(__file__).parent / "theme.qss"
        if self.qss_path.exists():
            self._watcher.addPath(str(self.qss_path))
            self._watcher.fileChanged.connect(self._on_theme_changed)

    def _on_theme_changed(self, path: str) -> None:
        if str(self.qss_path) not in self._watcher.files() and self.qss_path.exists():
            self._watcher.addPath(str(self.qss_path))
        self._load_theme()
        self._apply_responsive_layout()
        self._push_log("INFO", "UI", f"Tema yenilendi: {path}")


def run() -> None:
    app = QApplication(sys.argv)
    w = FullDemoPreview()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
