from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QFile, QTimer, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QMenu,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from xz_control_ui.core.models import ScanRecipe
from xz_control_ui.services.demo_system import DemoSystem
from xz_control_ui.services.runtime_manager import RuntimeManager


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("XZ Pozisyoner Ana Kontrol - Full Demo")
        self.resize(1520, 900)
        self.setMinimumSize(1100, 680)

        self.system = DemoSystem()
        activation = Path(__file__).resolve().parents[2] / "config" / "activation.json"
        self.runtime = RuntimeManager(activation)
        self.layout_edit_mode = False
        self._dock_widgets: list[QDockWidget] = []
        self._scan_completed_popup_shown = False
        self._last_scan_report: dict[str, float | int | str] = {}
        self._last_auto_report_path: Path | None = None

        self._load_theme()
        ui_mode = os.getenv("XZ_UI_MODE", "legacy").strip().lower()
        if ui_mode == "ui":
            self._build_ui_first_layout()
        else:
            self.setMenuWidget(self._build_topbar())
            self.setCentralWidget(QWidget())
            self._build_dock_layout()
            self._install_context_menu_sources()
        self._wire_enter_shortcuts()
        self._wire_timer()
        self._apply_responsive_layout()

    def _load_theme(self) -> None:
        qss = Path(__file__).parent / "ui" / "theme.qss"
        self._base_qss = qss.read_text(encoding="utf-8")
        self.setStyleSheet(self._base_qss)

    def _build_topbar(self) -> QWidget:
        box = QFrame()
        box.setObjectName("topbar")
        row = QHBoxLayout(box)
        self.mode_label = QLabel("Sistem Modu: READY")
        self.ttl_label = QLabel("TTL Sayac: 0")
        self.gain_label = QLabel("Gain (Peak): - dB")
        self.safety_label = QLabel("Safety: READY")
        self.runtime_label = QLabel("Runtime: DEMO")
        self.runtime_mode = QComboBox()
        self.runtime_mode.addItems(["DEMO", "HARDWARE"])
        self.runtime_mode.currentTextChanged.connect(self._set_runtime_mode)
        self.real_vna_check = QCheckBox("Real VNA")
        self.real_vna_check.setChecked(False)
        self.layout_btn = QPushButton("Ayarlar: Kilitli")
        self.layout_btn.clicked.connect(self._toggle_layout_edit_mode)
        self.vna_connect_btn = QPushButton("VNA Baglantisi")
        self.vna_connect_btn.clicked.connect(self._on_vna_connect_clicked)
        self.fullscreen_btn = QPushButton("Tam Ekran")
        self.fullscreen_btn.clicked.connect(self._toggle_fullscreen)
        self.dry_run_btn = QPushButton("Dry-Run")
        self.dry_run_btn.clicked.connect(self._dry_run_runtime)
        row.addWidget(QLabel("Proje: Demo_24GHz_Antenna"))
        row.addWidget(QLabel("Aktif Recete: Plane_XZ_Scan_5mm"))
        row.addStretch(1)
        row.addWidget(self.runtime_label)
        row.addWidget(self.runtime_mode)
        row.addWidget(self.real_vna_check)
        row.addWidget(self.vna_connect_btn)
        row.addWidget(self.layout_btn)
        row.addWidget(self.fullscreen_btn)
        row.addWidget(self.dry_run_btn)
        row.addWidget(self.mode_label)
        row.addWidget(self.gain_label)
        row.addWidget(self.safety_label)
        row.addWidget(self.ttl_label)
        return box

    def _build_ui_first_layout(self) -> None:
        ui_path = Path(__file__).parent / "ui" / "main_window.ui"
        if not ui_path.exists():
            self.setMenuWidget(self._build_topbar())
            self.setCentralWidget(QWidget())
            self._build_dock_layout()
            self._install_context_menu_sources()
            return

        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"UI acilamadi: {ui_path}")
        loaded = loader.load(ui_file)
        ui_file.close()
        if loaded is None:
            raise RuntimeError(f"UI yuklenemedi: {ui_path}")
        self._ui_loaded = loaded

        # Build from loaded UI root, then detach top bar and dockable sections.
        self.setWindowTitle(loaded.windowTitle() or "XZ Pozisyoner Ana Kontrol - UI")
        self._ui_loaded = loaded

        topbar_frame = loaded.findChild(QFrame, "topbarFrame")
        if topbar_frame is not None:
            if topbar_frame.parentWidget() is not None and topbar_frame.parentWidget().layout() is not None:
                topbar_frame.parentWidget().layout().removeWidget(topbar_frame)
            topbar_frame.setParent(None)
            topbar_frame.setMinimumHeight(40)
            topbar_frame.setMaximumHeight(46)
            self.setMenuWidget(topbar_frame)

        # QMainWindow must always have a central widget placeholder.
        self.setCentralWidget(QWidget())

        self.mode_label = loaded.findChild(QLabel, "modeLabel") or QLabel("Sistem Modu: READY")
        self.x_label = loaded.findChild(QLabel, "xPosLabel") or QLabel("X Konum: 0.00 mm")
        self.z_label = loaded.findChild(QLabel, "zPosLabel") or QLabel("Z Konum: 0.00 mm")

        self.ttl_label = loaded.findChild(QLabel, "ttlLabel") or QLabel("TTL Sayac: 0")
        self.gain_label = loaded.findChild(QLabel, "gainLabel") or QLabel("Gain (Peak): - dB")
        self.safety_label = loaded.findChild(QLabel, "safetyLabel") or QLabel("Safety: READY")
        self.runtime_label = loaded.findChild(QLabel, "runtimeLabel") or QLabel("Runtime: DEMO")
        self.runtime_mode = loaded.findChild(QComboBox, "runtimeModeCombo") or QComboBox()
        if self.runtime_mode.count() == 0:
            self.runtime_mode.addItems(["DEMO", "HARDWARE"])
        self.runtime_mode.currentTextChanged.connect(self._set_runtime_mode)
        self.real_vna_check = loaded.findChild(QCheckBox, "realVnaCheckBox") or QCheckBox("Real VNA")
        self.vna_connect_btn = loaded.findChild(QPushButton, "vnaConnectButton") or QPushButton("VNA Baglantisi")
        self.vna_connect_btn.clicked.connect(self._on_vna_connect_clicked)
        self.layout_btn = loaded.findChild(QPushButton, "layoutToggleButton") or QPushButton("Ayarlar")
        self.layout_btn.clicked.connect(self._toggle_layout_edit_mode)
        self.layout_btn.setEnabled(True)
        self.fullscreen_btn = loaded.findChild(QPushButton, "fullscreenButton") or QPushButton("Tam Ekran")
        self.fullscreen_btn.clicked.connect(self._toggle_fullscreen)
        self.dry_run_btn = loaded.findChild(QPushButton, "dryRunButton") or QPushButton("Dry-Run")
        self.dry_run_btn.clicked.connect(self._dry_run_runtime)
        topbar_layout = loaded.findChild(QHBoxLayout, "topbarLayout")
        if topbar_layout is not None:
            for w in [
                self.runtime_mode,
                self.real_vna_check,
                self.vna_connect_btn,
                self.layout_btn,
                self.fullscreen_btn,
                self.dry_run_btn,
            ]:
                if w.parent() is None:
                    topbar_layout.addWidget(w)

        self.r_name = loaded.findChild(QLineEdit, "recipeNameLineEdit") or QLineEdit("Plane_XZ_Scan_5mm")
        self.r_x_start = loaded.findChild(QLineEdit, "xStartLineEdit") or QLineEdit("0")
        self.r_x_stop = loaded.findChild(QLineEdit, "xStopLineEdit") or QLineEdit("1000")
        self.r_x_step = loaded.findChild(QLineEdit, "xStepLineEdit") or QLineEdit("500")
        self.r_z_start = loaded.findChild(QLineEdit, "zStartLineEdit") or QLineEdit("0")
        self.r_z_stop = loaded.findChild(QLineEdit, "zStopLineEdit") or QLineEdit("1000")
        self.r_z_step = loaded.findChild(QLineEdit, "zStepLineEdit") or QLineEdit("500")
        self.r_snaking = loaded.findChild(QCheckBox, "snakingCheckBox") or QCheckBox("Snaking")
        self.apply_recipe_btn = loaded.findChild(QPushButton, "applyRecipeButton")
        if self.apply_recipe_btn is not None:
            self.apply_recipe_btn.clicked.connect(self._apply_recipe)

        self.x_speed = loaded.findChild(QLineEdit, "xSpeedLineEdit") or QLineEdit("150")
        self.z_speed = loaded.findChild(QLineEdit, "zSpeedLineEdit") or QLineEdit("150")
        self.x_limit_check = loaded.findChild(QCheckBox, "xLimitCheckBox") or QCheckBox("X Limit")
        self.z_limit_check = loaded.findChild(QCheckBox, "zLimitCheckBox") or QCheckBox("Z Limit")
        self.x_limit_check.stateChanged.connect(self._apply_limits)
        self.z_limit_check.stateChanged.connect(self._apply_limits)
        if (btn := loaded.findChild(QPushButton, "applySpeedButton")) is not None:
            btn.clicked.connect(self._apply_speed)
        if (btn := loaded.findChild(QPushButton, "jogXmButton")) is not None:
            btn.clicked.connect(lambda: self.system.jog("x", -50.0))
        if (btn := loaded.findChild(QPushButton, "jogXpButton")) is not None:
            btn.clicked.connect(lambda: self.system.jog("x", 50.0))
        if (btn := loaded.findChild(QPushButton, "jogZmButton")) is not None:
            btn.clicked.connect(lambda: self.system.jog("z", -50.0))
        if (btn := loaded.findChild(QPushButton, "jogZpButton")) is not None:
            btn.clicked.connect(lambda: self.system.jog("z", 50.0))
        if (btn := loaded.findChild(QPushButton, "homeButton")) is not None:
            btn.clicked.connect(self.system.home)
        if (btn := loaded.findChild(QPushButton, "parkButton")) is not None:
            btn.clicked.connect(self.system.park)
        if (btn := loaded.findChild(QPushButton, "stopButton")) is not None:
            btn.clicked.connect(self.system.stop)
        if (btn := loaded.findChild(QPushButton, "estopButton")) is not None:
            btn.clicked.connect(self.system.estop_press)
        if (btn := loaded.findChild(QPushButton, "estopResetButton")) is not None:
            btn.clicked.connect(self.system.estop_reset)

        self.vna_model_combo = loaded.findChild(QComboBox, "vnaModelCombo") or QComboBox()
        self.vna_start = loaded.findChild(QDoubleSpinBox, "vnaStartSpin") or QDoubleSpinBox()
        self.vna_stop = loaded.findChild(QDoubleSpinBox, "vnaStopSpin") or QDoubleSpinBox()
        self.vna_points = loaded.findChild(QSpinBox, "vnaPointsSpin") or QSpinBox()
        self.vna_ifbw = loaded.findChild(QDoubleSpinBox, "vnaIfbwSpin") or QDoubleSpinBox()
        self.vna_power = loaded.findChild(QDoubleSpinBox, "vnaPowerSpin") or QDoubleSpinBox()
        if (btn := loaded.findChild(QPushButton, "applyVnaButton")) is not None:
            btn.clicked.connect(self._apply_vna_settings)

        self.progress = loaded.findChild(QProgressBar, "scanProgressBar") or QProgressBar()
        self.progress_label = loaded.findChild(QLabel, "progressLabel") or QLabel("Ilerleme: 0/0")
        self.gain_side_label = loaded.findChild(QLabel, "gainSideLabel") or QLabel("Gain (Peak): - dB")
        self.report_btn = loaded.findChild(QPushButton, "downloadReportButton") or QPushButton("Raporu Indir")
        self.report_btn.clicked.connect(self._download_scan_report)
        self._set_report_ready(False)
        if (btn := loaded.findChild(QPushButton, "startScanButton")) is not None:
            btn.clicked.connect(self._start_scan)
        if (btn := loaded.findChild(QPushButton, "pauseScanButton")) is not None:
            btn.clicked.connect(self._pause_scan)
        if (btn := loaded.findChild(QPushButton, "resumeScanButton")) is not None:
            btn.clicked.connect(self._resume_scan)
        if (btn := loaded.findChild(QPushButton, "abortScanButton")) is not None:
            btn.clicked.connect(self._abort_scan)
        self.self_check_btn = loaded.findChild(QPushButton, "selfCheckButton") or QPushButton("Self-Check")
        self.self_check_btn.clicked.connect(self._run_self_check)
        self.function_test_btn = loaded.findChild(QPushButton, "functionTestButton") or QPushButton("Fonksiyon Testi")
        self.function_test_btn.clicked.connect(self._run_function_demo_checks)
        self.icd_load_btn = loaded.findChild(QPushButton, "loadIcdButton") or QPushButton("ICD Yukle")
        self.icd_load_btn.clicked.connect(self._load_icd_placeholder)
        self.icd_path_label = loaded.findChild(QLabel, "icdPathLabel") or QLabel("ICD: yuklenmedi")
        self.icd_map_label = loaded.findChild(QLabel, "icdMapLabel") or QLabel("Map: beklemede")

        self.log_table = loaded.findChild(QTableWidget, "logTable") or QTableWidget(0, 3)
        if (btn := loaded.findChild(QPushButton, "clearLogButton")) is not None:
            btn.clicked.connect(lambda: self.log_table.setRowCount(0))

        trace_host = loaded.findChild(QFrame, "tracePlaceholderFrame")
        trace_layout = trace_host.layout() if trace_host is not None else QVBoxLayout()
        self.trace_plot = pg.PlotWidget()
        self.trace_plot.showGrid(x=True, y=True, alpha=0.2)
        self.trace_plot.setLabel("left", "S21", units="dB")
        self.trace_plot.setLabel("bottom", "Frekans", units="GHz")
        self.trace_curve = self.trace_plot.plot(pen=pg.mkPen("#203040", width=2))
        trace_layout.addWidget(self.trace_plot)

        heat_host = loaded.findChild(QFrame, "heatmapPlaceholderFrame")
        heat_layout = heat_host.layout() if heat_host is not None else QVBoxLayout()
        self.heatmap = pg.ImageView(view=pg.PlotItem())
        self.heatmap.ui.histogram.hide()
        self.heatmap.ui.roiBtn.hide()
        self.heatmap.ui.menuBtn.hide()
        heat_layout.addWidget(self.heatmap)

        time_host = loaded.findChild(QFrame, "timePlaceholderFrame")
        time_layout = time_host.layout() if time_host is not None else QVBoxLayout()
        self.time_plot = pg.PlotWidget()
        self.time_plot.showGrid(x=True, y=True, alpha=0.2)
        self.time_plot.setLabel("left", "S21", units="dB")
        self.time_plot.setLabel("bottom", "Zaman", units="s")
        self.time_curve = self.time_plot.plot(pen=pg.mkPen("#1e90ff", width=2))
        time_layout.addWidget(self.time_plot)

        plan_host = loaded.findChild(QFrame, "scanPlanPlaceholderFrame")
        plan_layout = plan_host.layout() if plan_host is not None else QVBoxLayout()
        self.scan_overview_plot = pg.PlotWidget()
        self.scan_overview_plot.showGrid(x=True, y=True, alpha=0.2)
        self.scan_overview_plot.setLabel("left", "Z", units="mm")
        self.scan_overview_plot.setLabel("bottom", "X", units="mm")
        self.scan_overview_scanned = pg.ScatterPlotItem(pen=pg.mkPen("#16a34a"), brush=pg.mkBrush("#22c55e"), size=8)
        self.scan_overview_unscanned = pg.ScatterPlotItem(pen=pg.mkPen("#dc2626"), brush=pg.mkBrush("#ef4444"), size=7)
        self.scan_overview_current = pg.ScatterPlotItem(pen=pg.mkPen("#1d4ed8"), brush=pg.mkBrush("#3b82f6"), size=12)
        self.scan_overview_plot.addItem(self.scan_overview_unscanned)
        self.scan_overview_plot.addItem(self.scan_overview_scanned)
        self.scan_overview_plot.addItem(self.scan_overview_current)
        plan_layout.addWidget(self.scan_overview_plot)

        self.setDockNestingEnabled(True)
        self._dock_widgets.clear()

        def _dock_from_group(group_name: str, title: str, area: Qt.DockWidgetArea, visible: bool = True):
            grp = loaded.findChild(QWidget, group_name)
            if grp is None:
                return None
            parent = grp.parentWidget()
            if parent is not None and parent.layout() is not None:
                parent.layout().removeWidget(grp)
            grp.setParent(None)
            dock = QDockWidget(title, self)
            dock.setObjectName(f"dock_ui_{group_name}")
            dock.setAllowedAreas(
                Qt.DockWidgetArea.LeftDockWidgetArea
                | Qt.DockWidgetArea.RightDockWidgetArea
                | Qt.DockWidgetArea.TopDockWidgetArea
                | Qt.DockWidgetArea.BottomDockWidgetArea
            )
            dock.setWidget(grp)
            self.addDockWidget(area, dock)
            self._dock_widgets.append(dock)
            if not visible:
                dock.hide()
            return dock

        manual = _dock_from_group("manualGroup", "Manuel Kontrol", Qt.DockWidgetArea.LeftDockWidgetArea)
        recipe = _dock_from_group("recipeGroup", "Tarama Recetesi", Qt.DockWidgetArea.LeftDockWidgetArea)
        scan = _dock_from_group("scanControlGroup", "Otomatik Tarama", Qt.DockWidgetArea.LeftDockWidgetArea)
        self.vna_settings_dock = _dock_from_group(
            "vnaSettingsGroup", "VNA Ayarlari", Qt.DockWidgetArea.LeftDockWidgetArea, visible=False
        )
        trace = _dock_from_group("traceGroup", "Canli S21 Trace", Qt.DockWidgetArea.RightDockWidgetArea)
        heatmap = _dock_from_group("heatmapGroup", "XZ Tarama Haritasi", Qt.DockWidgetArea.RightDockWidgetArea)
        time_series = _dock_from_group("timeSeriesGroup", "S21 Zaman Akisi", Qt.DockWidgetArea.RightDockWidgetArea)
        scan_plan = _dock_from_group("scanPlanGroup", "Tarama Nokta Plani", Qt.DockWidgetArea.BottomDockWidgetArea)
        log = _dock_from_group("alarmLogGroup", "Alarm / Log", Qt.DockWidgetArea.BottomDockWidgetArea)

        if manual and recipe:
            self.splitDockWidget(manual, recipe, Qt.Orientation.Vertical)
        if recipe and scan:
            self.splitDockWidget(recipe, scan, Qt.Orientation.Vertical)
        if scan and self.vna_settings_dock:
            self.splitDockWidget(scan, self.vna_settings_dock, Qt.Orientation.Vertical)
        if trace and heatmap:
            self.splitDockWidget(trace, heatmap, Qt.Orientation.Vertical)
        if heatmap and time_series:
            self.splitDockWidget(heatmap, time_series, Qt.Orientation.Vertical)
        if time_series and log:
            self.splitDockWidget(time_series, log, Qt.Orientation.Vertical)
        if log and scan_plan:
            self.splitDockWidget(log, scan_plan, Qt.Orientation.Horizontal)

        if manual and trace:
            self.resizeDocks([manual, trace], [420, 1080], Qt.Orientation.Horizontal)
        if manual and recipe and scan:
            self.resizeDocks([manual, recipe, scan], [220, 220, 260], Qt.Orientation.Vertical)
        if trace and heatmap and time_series:
            self.resizeDocks([trace, heatmap, time_series], [290, 290, 220], Qt.Orientation.Vertical)
        if log and scan_plan:
            self.resizeDocks([log, scan_plan], [210, 210], Qt.Orientation.Horizontal)

        self._install_context_menu_sources()
        self._set_layout_edit_mode(False)

    def _build_manual_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        layout = QVBoxLayout(box)
        layout.addWidget(QLabel("Manuel Kontrol - X/Z"))

        self.x_label = QLabel("X Konum: 0.00 mm")
        self.z_label = QLabel("Z Konum: 0.00 mm")
        self.x_label.setObjectName("value")
        self.z_label.setObjectName("value")
        layout.addWidget(self.x_label)
        layout.addWidget(self.z_label)

        speed_row = QHBoxLayout()
        self.x_speed = QLineEdit("150")
        self.z_speed = QLineEdit("150")
        speed_row.addWidget(QLabel("X hiz mm/s"))
        speed_row.addWidget(self.x_speed)
        speed_row.addWidget(QLabel("Z hiz mm/s"))
        speed_row.addWidget(self.z_speed)
        set_speed_btn = QPushButton("Hiz Uygula")
        set_speed_btn.clicked.connect(self._apply_speed)
        speed_row.addWidget(set_speed_btn)
        layout.addLayout(speed_row)

        move_row1 = QHBoxLayout()
        for title, fn in [
            ("X Jog -", lambda: self.system.jog("x", -50.0)),
            ("X Jog +", lambda: self.system.jog("x", 50.0)),
            ("Z Jog -", lambda: self.system.jog("z", -50.0)),
            ("Z Jog +", lambda: self.system.jog("z", 50.0)),
        ]:
            b = QPushButton(title)
            b.clicked.connect(fn)
            move_row1.addWidget(b)
        layout.addLayout(move_row1)

        move_row2 = QHBoxLayout()
        for title, fn in [
            ("Home", self.system.home),
            ("Park", self.system.park),
            ("STOP", self.system.stop),
            ("E-STOP", self.system.estop_press),
            ("E-STOP Reset", self.system.estop_reset),
        ]:
            b = QPushButton(title)
            b.clicked.connect(fn)
            move_row2.addWidget(b)
        layout.addLayout(move_row2)

        limit_row = QHBoxLayout()
        self.x_limit_check = QCheckBox("X Limit")
        self.z_limit_check = QCheckBox("Z Limit")
        self.x_limit_check.stateChanged.connect(self._apply_limits)
        self.z_limit_check.stateChanged.connect(self._apply_limits)
        limit_row.addWidget(self.x_limit_check)
        limit_row.addWidget(self.z_limit_check)
        layout.addLayout(limit_row)
        return box

    def _build_recipe_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        form = QFormLayout(box)

        self.r_name = QLineEdit("Plane_XZ_Scan_5mm")
        self.r_x_start = QLineEdit("0")
        self.r_x_stop = QLineEdit("1000")
        self.r_x_step = QLineEdit("500")
        self.r_z_start = QLineEdit("0")
        self.r_z_stop = QLineEdit("1000")
        self.r_z_step = QLineEdit("500")
        self.r_snaking = QCheckBox("Snaking")
        self.r_snaking.setChecked(True)

        form.addRow("Recete Adi", self.r_name)
        form.addRow("X Baslangic (mm)", self.r_x_start)
        form.addRow("X Bitis (mm)", self.r_x_stop)
        form.addRow("X Adim (mm)", self.r_x_step)
        form.addRow("Z Baslangic (mm)", self.r_z_start)
        form.addRow("Z Bitis (mm)", self.r_z_stop)
        form.addRow("Z Adim (mm)", self.r_z_step)
        form.addRow(self.r_snaking)

        btn = QPushButton("Receteyi Uygula")
        btn.clicked.connect(self._apply_recipe)
        form.addRow(btn)
        return box

    def _build_vna_settings_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        form = QFormLayout(box)
        form.addRow(QLabel("Network Analizor Ayarlari"))

        self.vna_model_combo = QComboBox()
        self.vna_model_combo.addItems(["R&S ZNL14", "Keysight N9917B"])
        form.addRow("Model", self.vna_model_combo)

        self.vna_start = QDoubleSpinBox()
        self.vna_start.setDecimals(3)
        self.vna_start.setRange(0.001, 50.0)
        self.vna_start.setValue(1.0)
        form.addRow("Start (GHz)", self.vna_start)

        self.vna_stop = QDoubleSpinBox()
        self.vna_stop.setDecimals(3)
        self.vna_stop.setRange(0.001, 50.0)
        self.vna_stop.setValue(14.0)
        form.addRow("Stop (GHz)", self.vna_stop)

        self.vna_points = QSpinBox()
        self.vna_points.setRange(11, 4001)
        self.vna_points.setValue(101)
        form.addRow("Points", self.vna_points)

        self.vna_ifbw = QDoubleSpinBox()
        self.vna_ifbw.setDecimals(1)
        self.vna_ifbw.setRange(1.0, 1_000_000.0)
        self.vna_ifbw.setValue(1000.0)
        form.addRow("IFBW (Hz)", self.vna_ifbw)

        self.vna_power = QDoubleSpinBox()
        self.vna_power.setDecimals(1)
        self.vna_power.setRange(-60.0, 20.0)
        self.vna_power.setValue(-10.0)
        form.addRow("Power (dBm)", self.vna_power)

        apply_btn = QPushButton("VNA Ayarlari Uygula")
        apply_btn.clicked.connect(self._apply_vna_settings)
        form.addRow(apply_btn)
        return box

    def _build_scan_control_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        layout = QVBoxLayout(box)
        layout.addWidget(QLabel("Otomatik Tarama / ICD / Gain"))

        row = QHBoxLayout()
        for t, fn in [
            ("Baslat", self._start_scan),
            ("Duraklat", self._pause_scan),
            ("Devam", self._resume_scan),
            ("Iptal", self._abort_scan),
        ]:
            b = QPushButton(t)
            b.clicked.connect(fn)
            row.addWidget(b)
        self.report_btn = QPushButton("Raporu Indir")
        self._set_report_ready(False)
        self.report_btn.clicked.connect(self._download_scan_report)
        row.addWidget(self.report_btn)
        layout.addLayout(row)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)
        self.progress_label = QLabel("Ilerleme: 0/0")
        layout.addWidget(self.progress_label)

        self.gain_side_label = QLabel("Gain (Peak): - dB")
        layout.addWidget(self.gain_side_label)

        led_row = QHBoxLayout()
        self.led_controller = QLabel("Controller")
        self.led_vna = QLabel("VNA")
        self.led_ttl = QLabel("TTL")
        for w in [self.led_controller, self.led_vna, self.led_ttl]:
            w.setObjectName("statusLedOff")
            led_row.addWidget(w)
        layout.addLayout(led_row)

        tools_row = QHBoxLayout()
        self.self_check_btn = QPushButton("Self-Check")
        self.self_check_btn.clicked.connect(self._run_self_check)
        self.function_test_btn = QPushButton("Fonksiyon Testi")
        self.function_test_btn.clicked.connect(self._run_function_demo_checks)
        self.icd_load_btn = QPushButton("ICD Yukle")
        self.icd_load_btn.clicked.connect(self._load_icd_placeholder)
        tools_row.addWidget(self.self_check_btn)
        tools_row.addWidget(self.function_test_btn)
        tools_row.addWidget(self.icd_load_btn)
        layout.addLayout(tools_row)

        self.icd_path_label = QLabel("ICD: yuklenmedi")
        self.icd_map_label = QLabel("Map: beklemede")
        layout.addWidget(self.icd_path_label)
        layout.addWidget(self.icd_map_label)
        return box

    def _make_dock(self, title: str, content: QWidget, area: Qt.DockWidgetArea) -> QDockWidget:
        dock = QDockWidget(title, self)
        dock.setObjectName(f"dock_{title.lower().replace(' ', '_')}")
        dock.setWidget(content)
        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
            | Qt.DockWidgetArea.TopDockWidgetArea
            | Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.addDockWidget(area, dock)
        self._dock_widgets.append(dock)
        return dock

    def _build_dock_layout(self) -> None:
        self.setDockNestingEnabled(True)

        manual = self._make_dock("Manuel Kontrol", self._build_manual_card(), Qt.DockWidgetArea.LeftDockWidgetArea)
        recipe = self._make_dock("Tarama Recetesi", self._build_recipe_card(), Qt.DockWidgetArea.LeftDockWidgetArea)
        scan = self._make_dock("Otomatik Tarama", self._build_scan_control_card(), Qt.DockWidgetArea.LeftDockWidgetArea)
        vna_settings = self._make_dock("VNA Ayarlari", self._build_vna_settings_card(), Qt.DockWidgetArea.LeftDockWidgetArea)
        self.vna_settings_dock = vna_settings

        trace = self._make_dock("Canli S21 Trace", self._build_trace_card(), Qt.DockWidgetArea.RightDockWidgetArea)
        heatmap = self._make_dock("XZ Tarama Haritasi", self._build_heatmap_card(), Qt.DockWidgetArea.RightDockWidgetArea)
        time_series = self._make_dock("S21 Zaman Akisi", self._build_time_card(), Qt.DockWidgetArea.RightDockWidgetArea)
        log = self._make_dock("Alarm / Log", self._build_log_card(), Qt.DockWidgetArea.BottomDockWidgetArea)
        scan_plan = self._make_dock("Tarama Nokta Plani", self._build_scan_plan_card(), Qt.DockWidgetArea.BottomDockWidgetArea)

        self.splitDockWidget(manual, recipe, Qt.Orientation.Vertical)
        self.splitDockWidget(recipe, scan, Qt.Orientation.Vertical)
        self.splitDockWidget(scan, vna_settings, Qt.Orientation.Vertical)

        self.splitDockWidget(trace, heatmap, Qt.Orientation.Vertical)
        self.splitDockWidget(heatmap, time_series, Qt.Orientation.Vertical)
        self.splitDockWidget(time_series, log, Qt.Orientation.Vertical)
        self.splitDockWidget(log, scan_plan, Qt.Orientation.Horizontal)

        self.resizeDocks([manual, trace], [420, 1080], Qt.Orientation.Horizontal)
        self.resizeDocks([manual, recipe, scan, vna_settings], [220, 220, 260, 220], Qt.Orientation.Vertical)
        self.vna_settings_dock.hide()

        self._set_layout_edit_mode(False)

    def _build_scan_plan_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        layout = QVBoxLayout(box)
        layout.addWidget(QLabel("Tarama Nokta Plani (Yesil=taranan, Kirmizi=taranmayan)"))
        self.scan_overview_plot = pg.PlotWidget()
        self.scan_overview_plot.showGrid(x=True, y=True, alpha=0.2)
        self.scan_overview_plot.setLabel("left", "Z", units="mm")
        self.scan_overview_plot.setLabel("bottom", "X", units="mm")
        self.scan_overview_plot.setMinimumHeight(260)
        self.scan_overview_scanned = pg.ScatterPlotItem(
            pen=pg.mkPen("#16a34a"), brush=pg.mkBrush("#22c55e"), size=8
        )
        self.scan_overview_unscanned = pg.ScatterPlotItem(
            pen=pg.mkPen("#dc2626"), brush=pg.mkBrush("#ef4444"), size=7
        )
        self.scan_overview_current = pg.ScatterPlotItem(
            pen=pg.mkPen("#1d4ed8"), brush=pg.mkBrush("#3b82f6"), size=12
        )
        self.scan_overview_plot.addItem(self.scan_overview_unscanned)
        self.scan_overview_plot.addItem(self.scan_overview_scanned)
        self.scan_overview_plot.addItem(self.scan_overview_current)
        layout.addWidget(self.scan_overview_plot)
        return box

    def _build_trace_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel("Canli S21 Trace"))
        self.trace_plot = pg.PlotWidget()
        self.trace_plot.showGrid(x=True, y=True, alpha=0.2)
        self.trace_plot.setLabel("left", "S21", units="dB")
        self.trace_plot.setLabel("bottom", "Frekans", units="GHz")
        self.trace_curve = self.trace_plot.plot(pen=pg.mkPen("#203040", width=2))
        lay.addWidget(self.trace_plot)
        return box

    def _build_heatmap_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel("XZ Tarama Haritasi"))
        self.heatmap = pg.ImageView(view=pg.PlotItem())
        self.heatmap.ui.histogram.hide()
        self.heatmap.ui.roiBtn.hide()
        self.heatmap.ui.menuBtn.hide()
        lay.addWidget(self.heatmap)
        lay.addWidget(QLabel("Renk Skalasi Birimi: dB"))
        return box

    def _build_time_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel("S21 Zaman Akisi"))
        self.time_plot = pg.PlotWidget()
        self.time_plot.showGrid(x=True, y=True, alpha=0.2)
        self.time_plot.setLabel("left", "S21", units="dB")
        self.time_plot.setLabel("bottom", "Zaman", units="s")
        self.time_curve = self.time_plot.plot(pen=pg.mkPen("#1e90ff", width=2))
        lay.addWidget(self.time_plot)
        return box

    def _build_log_card(self) -> QWidget:
        box = QFrame()
        box.setObjectName("card")
        lay = QVBoxLayout(box)
        lay.addWidget(QLabel("Alarm / Log"))

        self.log_table = QTableWidget(0, 3)
        self.log_table.setHorizontalHeaderLabels(["Seviye", "Kaynak", "Mesaj"])
        self.log_table.setMinimumHeight(180)
        self.log_table.setMaximumHeight(220)
        lay.addWidget(self.log_table)

        btn = QPushButton("Temizle")
        btn.clicked.connect(lambda: self.log_table.setRowCount(0))
        lay.addWidget(btn)
        return box

    def _wire_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(250)

    def _install_context_menu_sources(self) -> None:
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_layout_context_menu)
        if self.centralWidget() is not None:
            self.centralWidget().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.centralWidget().customContextMenuRequested.connect(self._show_layout_context_menu)
        for dock in self._dock_widgets:
            dock.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            dock.customContextMenuRequested.connect(self._show_layout_context_menu)
            w = dock.widget()
            if w is not None:
                w.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                w.customContextMenuRequested.connect(self._show_layout_context_menu)

    def _wire_enter_shortcuts(self) -> None:
        self.x_speed.returnPressed.connect(self._apply_speed)
        self.z_speed.returnPressed.connect(self._apply_speed)

        for w in [
            self.r_name,
            self.r_x_start,
            self.r_x_stop,
            self.r_x_step,
            self.r_z_start,
            self.r_z_stop,
            self.r_z_step,
        ]:
            w.returnPressed.connect(self._apply_recipe)

        self.vna_start.editingFinished.connect(self._apply_vna_settings)
        self.vna_stop.editingFinished.connect(self._apply_vna_settings)
        self.vna_points.editingFinished.connect(self._apply_vna_settings)
        self.vna_ifbw.editingFinished.connect(self._apply_vna_settings)
        self.vna_power.editingFinished.connect(self._apply_vna_settings)
        self.vna_model_combo.currentTextChanged.connect(lambda _: self._apply_vna_settings())

    def _set_report_ready(self, ready: bool) -> None:
        self.report_btn.setEnabled(ready)
        if ready:
            self.report_btn.setStyleSheet(
                "QPushButton { background-color: #16a34a; color: #ffffff; font-weight: 600; }"
            )
        else:
            self.report_btn.setStyleSheet(
                "QPushButton { background-color: #6b7280; color: #d1d5db; font-weight: 500; }"
            )

    def _apply_speed(self) -> None:
        try:
            self.system.set_speed("x", float(self.x_speed.text()))
            self.system.set_speed("z", float(self.z_speed.text()))
            self._push_log("INFO", "Manual", "Hiz degerleri uygulandi")
        except ValueError:
            self._push_log("ERROR", "Manual", "Hiz degeri sayi olmali")

    def _start_scan(self) -> None:
        self._set_report_ready(False)
        self._last_scan_report = {}
        self._last_auto_report_path = None
        self._scan_completed_popup_shown = False
        self.system.start_scan()
        self._push_log("INFO", "Scan", "Tarama baslatildi")

    def _pause_scan(self) -> None:
        self.system.pause_scan()
        self._push_log("INFO", "Scan", "Tarama duraklatildi")

    def _resume_scan(self) -> None:
        self.system.resume_scan()
        self._push_log("INFO", "Scan", "Tarama devam ediyor")

    def _abort_scan(self) -> None:
        self.system.abort_scan()
        self._set_report_ready(False)
        self._push_log("WARN", "Scan", "Tarama iptal edildi")

    def _apply_recipe(self) -> None:
        try:
            recipe = ScanRecipe(
                name=self.r_name.text().strip() or "Recipe",
                x_start_mm=float(self.r_x_start.text()),
                x_stop_mm=float(self.r_x_stop.text()),
                x_step_mm=float(self.r_x_step.text()),
                z_start_mm=float(self.r_z_start.text()),
                z_stop_mm=float(self.r_z_stop.text()),
                z_step_mm=float(self.r_z_step.text()),
                snaking=self.r_snaking.isChecked(),
            )
            self.system.apply_recipe(recipe)
            self._push_log("INFO", "Recipe", f"Recete uygulandi: {recipe.name}")
        except ValueError:
            self._push_log("ERROR", "Recipe", "Recete alanlari gecerli sayi olmali")

    def _apply_vna_settings(self) -> None:
        model = self.vna_model_combo.currentText()
        self.system.set_vna_settings(
            model=model,
            start_ghz=float(self.vna_start.value()),
            stop_ghz=float(self.vna_stop.value()),
            points=int(self.vna_points.value()),
            ifbw_hz=float(self.vna_ifbw.value()),
            power_dbm=float(self.vna_power.value()),
        )
        self._push_log(
            "INFO",
            "VNA",
            f"{model} ayarlari uygulandi: {self.system.vna_start_ghz:.3f}-{self.system.vna_stop_ghz:.3f} GHz, {self.system.vna_points} pt, IFBW {self.system.vna_ifbw_hz:.1f} Hz, Pwr {self.system.vna_power_dbm:.1f} dBm",
        )

    def _on_vna_connect_clicked(self) -> None:
        if self.vna_settings_dock is not None:
            self.vna_settings_dock.setVisible(True)
            self.vna_settings_dock.raise_()
            self.vna_settings_dock.activateWindow()
        self._apply_vna_settings()
        self._push_log("INFO", "VNA", "VNA baglanti/ayar paneli acildi")

    def _tick(self) -> None:
        t = self.system.tick(0.25)

        self.x_label.setText(f"X Konum: {t.x_axis.position_mm:.2f} mm")
        self.z_label.setText(f"Z Konum: {t.z_axis.position_mm:.2f} mm")
        self.mode_label.setText(f"Sistem Modu: {t.mode}")
        self.safety_label.setText(f"Safety: {t.safety_state}")
        self.ttl_label.setText(f"TTL Sayac: {t.ttl_count}")
        peak_gain = max(t.s21_trace_db) if t.s21_trace_db else float("nan")
        self.gain_label.setText(f"Gain (Peak): {peak_gain:.2f} dB")
        self.gain_side_label.setText(f"Gain (Peak): {peak_gain:.2f} dB")

        self.trace_curve.setData(self.system.trace_freq_ghz, t.s21_trace_db)
        self.time_curve.setData(self.system.time_axis, t.s21_time_db)
        self.heatmap.setImage(np.array(t.heatmap_db), autoLevels=True)

        pct = int((t.progress.completed_points / t.progress.total_points) * 100)
        self.progress.setValue(pct)
        self.progress_label.setText(
            f"Ilerleme: {t.progress.completed_points}/{t.progress.total_points}"
        )
        self._update_scan_overview()
        self._handle_scan_completion(t)

    def _push_log(self, level: str, source: str, message: str) -> None:
        row = self.log_table.rowCount()
        self.log_table.insertRow(row)
        self.log_table.setItem(row, 0, QTableWidgetItem(level))
        self.log_table.setItem(row, 1, QTableWidgetItem(source))
        self.log_table.setItem(row, 2, QTableWidgetItem(message))

    def _apply_limits(self) -> None:
        self.system.set_limit_state(
            x_limit=self.x_limit_check.isChecked(),
            z_limit=self.z_limit_check.isChecked(),
        )

    def _set_runtime_mode(self, mode: str) -> None:
        status = self.runtime.set_mode(mode, use_mock_vna=not self.real_vna_check.isChecked())
        level = "INFO" if status.connected else "WARN"
        self.runtime_label.setText(f"Runtime: {status.mode}")
        self._push_log(level, "Runtime", status.detail)

    def _dry_run_runtime(self) -> None:
        status = self.runtime.dry_run()
        level = "INFO" if status.connected else "WARN"
        self._push_log(level, "DryRun", status.detail)

    def _run_self_check(self) -> None:
        checks: list[tuple[str, bool, str]] = []
        checks.append(("runtime_mode", True, f"mode={self.runtime.mode}"))
        checks.append(("ui_timer", self.timer.isActive(), "ui timer active"))

        st = self.runtime.component_status()
        checks.append(("controller", st["controller"], "controller adapter"))
        checks.append(("vna", st["vna"], "vna adapter"))
        checks.append(("ttl", st["ttl"], "ttl adapter"))

        self._set_led(self.led_controller, st["controller"])
        self._set_led(self.led_vna, st["vna"])
        self._set_led(self.led_ttl, st["ttl"])

        for name, ok, detail in checks:
            self._push_log("INFO" if ok else "WARN", "SelfCheck", f"{name}: {detail}")

    def _run_function_demo_checks(self) -> None:
        checks: list[tuple[str, bool]] = []

        # 1) Manual motion
        x0 = self.system.x.position_mm
        self.system.jog("x", 50.0)
        for _ in range(6):
            self.system.tick(0.25)
        checks.append(("manual_jog_x", self.system.x.position_mm > x0))

        # 2) Recipe + scan point generation
        self._apply_recipe()
        checks.append(("recipe_points", len(self.system.scan_points) > 0))

        # 3) Scan progress
        before_idx = self.system.scan_index
        self.system.start_scan()
        for _ in range(20):
            self.system.tick(0.25)
        checks.append(("scan_progress", self.system.scan_index > before_idx))

        # 4) Safety estop latch/reset
        self.system.estop_press()
        estop_ok = self.system.mode in {"ESTOP_LATCHED", "STOPPED"}
        self.system.estop_reset()
        reset_ok = self.system.mode == "READY"
        checks.append(("safety_estop", estop_ok and reset_ok))

        # 5) Runtime dry-run path
        _ = self.runtime.set_mode("HARDWARE", use_mock_vna=True)
        dr = self.runtime.dry_run()
        checks.append(("runtime_dry_run", dr.connected))
        _ = self.runtime.set_mode("DEMO", use_mock_vna=True)

        passed = 0
        for name, ok in checks:
            if ok:
                passed += 1
            self._push_log("INFO" if ok else "ERROR", "FuncTest", f"{name}: {'PASS' if ok else 'FAIL'}")
        self._push_log("INFO", "FuncTest", f"Summary: {passed}/{len(checks)} PASS")

    def _load_icd_placeholder(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "ICD Dokumani Sec",
            str(Path.home()),
            "Documents (*.docx *.pdf *.txt *.md);;All Files (*.*)",
        )
        if not path:
            return
        self.icd_path_label.setText(f"ICD: {path}")
        self.icd_map_label.setText("Map: parser/activation esleme hazir (taslak)")
        self._push_log("INFO", "ICD", "ICD dosyasi secildi, wizard taslagi hazir")

    def _set_led(self, label: QLabel, ok: bool) -> None:
        label.setObjectName("statusLedOn" if ok else "statusLedOff")
        self.style().unpolish(label)
        self.style().polish(label)

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_btn.setText("Tam Ekran")
        else:
            self.showFullScreen()
            self.fullscreen_btn.setText("Pencere")

    def _toggle_layout_edit_mode(self) -> None:
        self._set_layout_edit_mode(not self.layout_edit_mode)
        self._push_log(
            "INFO",
            "Layout",
            "Layout edit mode acildi" if self.layout_edit_mode else "Layout edit mode kapandi",
        )

    def _set_layout_edit_mode(self, enabled: bool) -> None:
        self.layout_edit_mode = enabled
        if enabled:
            features = (
                QDockWidget.DockWidgetMovable
                | QDockWidget.DockWidgetFloatable
            )
            self.layout_btn.setText("Ayarlar: Duzenleme Acik")
        else:
            features = QDockWidget.NoDockWidgetFeatures
            self.layout_btn.setText("Ayarlar: Kilitli")

        for dock in self._dock_widgets:
            dock.setFeatures(features)
        if not enabled:
            self._apply_responsive_layout()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        if not self.layout_edit_mode:
            self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        width = max(1, self.width())
        height = max(1, self.height())

        # Compact typography on smaller windows
        if width < 1300:
            dynamic_qss = "\nQMainWindow{font-size:11px;}"
            plan_h = 210
        elif width < 1550:
            dynamic_qss = "\nQMainWindow{font-size:12px;}"
            plan_h = 240
        else:
            dynamic_qss = "\nQMainWindow{font-size:12px;}"
            plan_h = 280
        self.setStyleSheet(self._base_qss + dynamic_qss)

        # Keep scan plan usable while resizing
        if hasattr(self, "scan_overview_plot"):
            self.scan_overview_plot.setMinimumHeight(plan_h)

        # Proportional dock sizing (effective when layout locked)
        left_w = int(width * 0.30)
        right_w = max(200, width - left_w - 40)
        left_h_top = int(height * 0.56)
        left_h_bottom = max(180, height - left_h_top - 120)

        docks_by_name = {d.windowTitle(): d for d in self._dock_widgets}
        manual = docks_by_name.get("Manuel Kontrol")
        recipe = docks_by_name.get("Tarama Recetesi")
        scan = docks_by_name.get("Otomatik Tarama")
        trace = docks_by_name.get("Canli S21 Trace")
        heatmap = docks_by_name.get("XZ Tarama Haritasi")
        time_series = docks_by_name.get("S21 Zaman Akisi")
        log = docks_by_name.get("Alarm / Log")
        scan_plan = docks_by_name.get("Tarama Nokta Plani")

        if manual and trace:
            self.resizeDocks([manual, trace], [left_w, right_w], Qt.Orientation.Horizontal)
        if manual and recipe and scan:
            self.resizeDocks(
                [manual, recipe, scan],
                [int(left_h_top * 0.35), int(left_h_top * 0.30), int(left_h_top * 0.35)],
                Qt.Orientation.Vertical,
            )
        if trace and heatmap and time_series:
            self.resizeDocks(
                [trace, heatmap, time_series],
                [int(height * 0.32), int(height * 0.32), int(height * 0.24)],
                Qt.Orientation.Vertical,
            )
        if log and scan_plan:
            self.resizeDocks([log, scan_plan], [left_h_bottom, left_h_bottom], Qt.Orientation.Horizontal)

    def _update_scan_overview(self) -> None:
        pts = self.system.scan_points
        done = max(0, min(self.system.scan_index, len(pts)))
        if pts:
            done_pts = [{"pos": (x, z)} for x, z in pts[:done]]
            remaining_pts = [{"pos": (x, z)} for x, z in pts[done:]]
            self.scan_overview_scanned.setData(done_pts)
            self.scan_overview_unscanned.setData(remaining_pts)
        else:
            self.scan_overview_scanned.setData([])
            self.scan_overview_unscanned.setData([])
        self.scan_overview_current.setData([{"pos": (self.system.x.position_mm, self.system.z.position_mm)}])

    def _handle_scan_completion(self, telemetry) -> None:
        became_ready_after_scan = (
            telemetry.mode == "READY"
            and telemetry.progress.total_points > 0
            and telemetry.progress.completed_points >= telemetry.progress.total_points
        )
        if became_ready_after_scan and not self._scan_completed_popup_shown:
            self._scan_completed_popup_shown = True
            self._set_report_ready(True)
            self._last_scan_report = self._collect_scan_report_data(telemetry)
            self._last_auto_report_path = self._write_auto_report_file()
            self._show_info_popup("Tarama Durumu", "Tarama tamamlandi")
            if self._last_auto_report_path:
                self._push_log(
                    "INFO",
                    "Scan",
                    f"Tarama tamamlandi, rapor hazir: {self._last_auto_report_path}",
                )
            else:
                self._push_log("INFO", "Scan", "Tarama tamamlandi, rapor hazir")
        if telemetry.mode in {"SCANNING", "MOVING", "PAUSED"}:
            self._scan_completed_popup_shown = False
            self._set_report_ready(False)

    def _collect_scan_report_data(self, telemetry) -> dict[str, float | int | str]:
        trace = telemetry.s21_trace_db or [0.0]
        heat = np.array(telemetry.heatmap_db) if telemetry.heatmap_db else np.zeros((1, 1))
        peak_gain = float(max(trace))
        avg_gain = float(sum(trace) / len(trace))
        health = "IYI" if peak_gain > -8.0 else ("ORTA" if peak_gain > -15.0 else "ZAYIF")
        efficiency = max(0.0, min(100.0, (peak_gain + 40.0) / 40.0 * 100.0))
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": self.system.vna_model,
            "freq_start": self.system.vna_start_ghz,
            "freq_stop": self.system.vna_stop_ghz,
            "points": self.system.vna_points,
            "ifbw": self.system.vna_ifbw_hz,
            "power_dbm": self.system.vna_power_dbm,
            "scan_total": telemetry.progress.total_points,
            "scan_completed": telemetry.progress.completed_points,
            "peak_gain_db": peak_gain,
            "avg_gain_db": avg_gain,
            "heatmap_min_db": float(heat.min()),
            "heatmap_max_db": float(heat.max()),
            "ttl_count": telemetry.ttl_count,
            "health": health,
            "efficiency_pct": float(efficiency),
            "alarm_count": len(telemetry.alarms),
        }

    def _build_report_text(self) -> str:
        data = self._last_scan_report
        if not data:
            return "Henüz tamamlanmış bir tarama raporu yok."
        lines = [
            "XZ TARAMA SONUC RAPORU",
            "======================",
            f"Tarih/Saat: {data['timestamp']}",
            "",
            "VNA AYARLARI",
            f"Model: {data['model']}",
            f"Frekans: {data['freq_start']:.3f} - {data['freq_stop']:.3f} GHz",
            f"Nokta: {int(data['points'])}",
            f"IFBW: {data['ifbw']:.1f} Hz",
            f"Guc: {data['power_dbm']:.1f} dBm",
            "",
            "TARAMA OZETI",
            f"Toplam Nokta: {int(data['scan_total'])}",
            f"Taranan Nokta: {int(data['scan_completed'])}",
            f"TTL Tetik Sayisi: {int(data['ttl_count'])}",
            "",
            "PERFORMANS",
            f"Peak Gain: {data['peak_gain_db']:.2f} dB",
            f"Ortalama Gain: {data['avg_gain_db']:.2f} dB",
            f"Harita Min/Max: {data['heatmap_min_db']:.2f} / {data['heatmap_max_db']:.2f} dB",
            "",
            "ANTEN DEGERLENDIRME",
            f"Saglik Durumu: {data['health']}",
            f"Tahmini Verimlilik: %{data['efficiency_pct']:.1f}",
            f"Alarm Sayisi: {int(data['alarm_count'])}",
            "",
            "Not: Bu rapor demo modundaki olcum simulasyonu uzerinden uretilmistir.",
        ]
        return "\n".join(lines)

    def _write_auto_report_file(self) -> Path | None:
        if not self._last_scan_report:
            return None
        reports_dir = Path(__file__).resolve().parents[2] / "state" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        file_path = reports_dir / f"scan_report_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path.write_text(self._build_report_text(), encoding="utf-8")
        return file_path

    def _download_scan_report(self) -> None:
        if not self._last_scan_report:
            QMessageBox.warning(self, "Rapor", "Önce bir taramayı tamamlamalısınız.")
            return
        default_name = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Raporu Kaydet",
            str(Path.home() / default_name),
            "Text Files (*.txt);;All Files (*.*)",
        )
        if not path:
            return
        Path(path).write_text(self._build_report_text(), encoding="utf-8")
        self._push_log("INFO", "Report", f"Rapor kaydedildi: {path}")
        QMessageBox.information(self, "Rapor", "Rapor basariyla kaydedildi")

    def _show_layout_context_menu(self, pos) -> None:
        sender = self.sender()
        if isinstance(sender, QWidget):
            global_pos = sender.mapToGlobal(pos)
        else:
            global_pos = self.mapToGlobal(pos)
        menu = QMenu(self)
        for dock in self._dock_widgets:
            action = menu.addAction(dock.windowTitle())
            action.setCheckable(True)
            action.setChecked(dock.isVisible())
            action.toggled.connect(dock.setVisible)
        menu.exec(global_pos)

    def _show_info_popup(self, title: str, text: str) -> None:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet("QLabel { color: #ffffff; }")
        msg.exec()


def run() -> None:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()


