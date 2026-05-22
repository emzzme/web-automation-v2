# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1520, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setObjectName(u"rootLayout")
        self.topbarFrame = QFrame(self.centralwidget)
        self.topbarFrame.setObjectName(u"topbarFrame")
        self.topbarFrame.setFrameShape(QFrame.StyledPanel)
        self.topbarLayout = QHBoxLayout(self.topbarFrame)
        self.topbarLayout.setObjectName(u"topbarLayout")
        self.projectLabel = QLabel(self.topbarFrame)
        self.projectLabel.setObjectName(u"projectLabel")

        self.topbarLayout.addWidget(self.projectLabel)

        self.recipeLabel = QLabel(self.topbarFrame)
        self.recipeLabel.setObjectName(u"recipeLabel")

        self.topbarLayout.addWidget(self.recipeLabel)

        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topbarLayout.addItem(self.topSpacer)

        self.runtimeModeCombo = QComboBox(self.topbarFrame)
        self.runtimeModeCombo.addItem("")
        self.runtimeModeCombo.addItem("")
        self.runtimeModeCombo.setObjectName(u"runtimeModeCombo")

        self.topbarLayout.addWidget(self.runtimeModeCombo)

        self.realVnaCheckBox = QCheckBox(self.topbarFrame)
        self.realVnaCheckBox.setObjectName(u"realVnaCheckBox")

        self.topbarLayout.addWidget(self.realVnaCheckBox)

        self.vnaConnectButton = QPushButton(self.topbarFrame)
        self.vnaConnectButton.setObjectName(u"vnaConnectButton")

        self.topbarLayout.addWidget(self.vnaConnectButton)

        self.layoutToggleButton = QPushButton(self.topbarFrame)
        self.layoutToggleButton.setObjectName(u"layoutToggleButton")

        self.topbarLayout.addWidget(self.layoutToggleButton)

        self.fullscreenButton = QPushButton(self.topbarFrame)
        self.fullscreenButton.setObjectName(u"fullscreenButton")

        self.topbarLayout.addWidget(self.fullscreenButton)

        self.dryRunButton = QPushButton(self.topbarFrame)
        self.dryRunButton.setObjectName(u"dryRunButton")

        self.topbarLayout.addWidget(self.dryRunButton)

        self.modeLabel = QLabel(self.topbarFrame)
        self.modeLabel.setObjectName(u"modeLabel")

        self.topbarLayout.addWidget(self.modeLabel)

        self.gainLabel = QLabel(self.topbarFrame)
        self.gainLabel.setObjectName(u"gainLabel")

        self.topbarLayout.addWidget(self.gainLabel)

        self.safetyLabel = QLabel(self.topbarFrame)
        self.safetyLabel.setObjectName(u"safetyLabel")

        self.topbarLayout.addWidget(self.safetyLabel)

        self.ttlLabel = QLabel(self.topbarFrame)
        self.ttlLabel.setObjectName(u"ttlLabel")

        self.topbarLayout.addWidget(self.ttlLabel)


        self.rootLayout.addWidget(self.topbarFrame)

        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.leftColumn = QWidget(self.mainSplitter)
        self.leftColumn.setObjectName(u"leftColumn")
        self.leftLayout = QVBoxLayout(self.leftColumn)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.manualGroup = QGroupBox(self.leftColumn)
        self.manualGroup.setObjectName(u"manualGroup")
        self.manualGroupLayout = QVBoxLayout(self.manualGroup)
        self.manualGroupLayout.setObjectName(u"manualGroupLayout")
        self.xPosLabel = QLabel(self.manualGroup)
        self.xPosLabel.setObjectName(u"xPosLabel")

        self.manualGroupLayout.addWidget(self.xPosLabel)

        self.zPosLabel = QLabel(self.manualGroup)
        self.zPosLabel.setObjectName(u"zPosLabel")

        self.manualGroupLayout.addWidget(self.zPosLabel)

        self.speedLayout = QHBoxLayout()
        self.speedLayout.setObjectName(u"speedLayout")
        self.xSpeedText = QLabel(self.manualGroup)
        self.xSpeedText.setObjectName(u"xSpeedText")

        self.speedLayout.addWidget(self.xSpeedText)

        self.xSpeedLineEdit = QLineEdit(self.manualGroup)
        self.xSpeedLineEdit.setObjectName(u"xSpeedLineEdit")

        self.speedLayout.addWidget(self.xSpeedLineEdit)

        self.zSpeedText = QLabel(self.manualGroup)
        self.zSpeedText.setObjectName(u"zSpeedText")

        self.speedLayout.addWidget(self.zSpeedText)

        self.zSpeedLineEdit = QLineEdit(self.manualGroup)
        self.zSpeedLineEdit.setObjectName(u"zSpeedLineEdit")

        self.speedLayout.addWidget(self.zSpeedLineEdit)

        self.applySpeedButton = QPushButton(self.manualGroup)
        self.applySpeedButton.setObjectName(u"applySpeedButton")

        self.speedLayout.addWidget(self.applySpeedButton)


        self.manualGroupLayout.addLayout(self.speedLayout)

        self.jogLayout = QGridLayout()
        self.jogLayout.setObjectName(u"jogLayout")
        self.jogXmButton = QPushButton(self.manualGroup)
        self.jogXmButton.setObjectName(u"jogXmButton")

        self.jogLayout.addWidget(self.jogXmButton, 0, 0, 1, 1)

        self.jogXpButton = QPushButton(self.manualGroup)
        self.jogXpButton.setObjectName(u"jogXpButton")

        self.jogLayout.addWidget(self.jogXpButton, 0, 1, 1, 1)

        self.jogZmButton = QPushButton(self.manualGroup)
        self.jogZmButton.setObjectName(u"jogZmButton")

        self.jogLayout.addWidget(self.jogZmButton, 1, 0, 1, 1)

        self.jogZpButton = QPushButton(self.manualGroup)
        self.jogZpButton.setObjectName(u"jogZpButton")

        self.jogLayout.addWidget(self.jogZpButton, 1, 1, 1, 1)


        self.manualGroupLayout.addLayout(self.jogLayout)

        self.manualCmdLayout = QGridLayout()
        self.manualCmdLayout.setObjectName(u"manualCmdLayout")
        self.homeButton = QPushButton(self.manualGroup)
        self.homeButton.setObjectName(u"homeButton")

        self.manualCmdLayout.addWidget(self.homeButton, 0, 0, 1, 1)

        self.parkButton = QPushButton(self.manualGroup)
        self.parkButton.setObjectName(u"parkButton")

        self.manualCmdLayout.addWidget(self.parkButton, 0, 1, 1, 1)

        self.stopButton = QPushButton(self.manualGroup)
        self.stopButton.setObjectName(u"stopButton")

        self.manualCmdLayout.addWidget(self.stopButton, 0, 2, 1, 1)

        self.estopButton = QPushButton(self.manualGroup)
        self.estopButton.setObjectName(u"estopButton")

        self.manualCmdLayout.addWidget(self.estopButton, 1, 0, 1, 1)

        self.estopResetButton = QPushButton(self.manualGroup)
        self.estopResetButton.setObjectName(u"estopResetButton")

        self.manualCmdLayout.addWidget(self.estopResetButton, 1, 1, 1, 1)


        self.manualGroupLayout.addLayout(self.manualCmdLayout)

        self.xLimitCheckBox = QCheckBox(self.manualGroup)
        self.xLimitCheckBox.setObjectName(u"xLimitCheckBox")

        self.manualGroupLayout.addWidget(self.xLimitCheckBox)

        self.zLimitCheckBox = QCheckBox(self.manualGroup)
        self.zLimitCheckBox.setObjectName(u"zLimitCheckBox")

        self.manualGroupLayout.addWidget(self.zLimitCheckBox)


        self.leftLayout.addWidget(self.manualGroup)

        self.recipeGroup = QGroupBox(self.leftColumn)
        self.recipeGroup.setObjectName(u"recipeGroup")
        self.recipeFormLayout = QFormLayout(self.recipeGroup)
        self.recipeFormLayout.setObjectName(u"recipeFormLayout")
        self.label_recipeName = QLabel(self.recipeGroup)
        self.label_recipeName.setObjectName(u"label_recipeName")

        self.recipeFormLayout.setWidget(0, QFormLayout.LabelRole, self.label_recipeName)

        self.recipeNameLineEdit = QLineEdit(self.recipeGroup)
        self.recipeNameLineEdit.setObjectName(u"recipeNameLineEdit")

        self.recipeFormLayout.setWidget(0, QFormLayout.FieldRole, self.recipeNameLineEdit)

        self.label_xStart = QLabel(self.recipeGroup)
        self.label_xStart.setObjectName(u"label_xStart")

        self.recipeFormLayout.setWidget(1, QFormLayout.LabelRole, self.label_xStart)

        self.xStartLineEdit = QLineEdit(self.recipeGroup)
        self.xStartLineEdit.setObjectName(u"xStartLineEdit")

        self.recipeFormLayout.setWidget(1, QFormLayout.FieldRole, self.xStartLineEdit)

        self.label_xStop = QLabel(self.recipeGroup)
        self.label_xStop.setObjectName(u"label_xStop")

        self.recipeFormLayout.setWidget(2, QFormLayout.LabelRole, self.label_xStop)

        self.xStopLineEdit = QLineEdit(self.recipeGroup)
        self.xStopLineEdit.setObjectName(u"xStopLineEdit")

        self.recipeFormLayout.setWidget(2, QFormLayout.FieldRole, self.xStopLineEdit)

        self.label_xStep = QLabel(self.recipeGroup)
        self.label_xStep.setObjectName(u"label_xStep")

        self.recipeFormLayout.setWidget(3, QFormLayout.LabelRole, self.label_xStep)

        self.xStepLineEdit = QLineEdit(self.recipeGroup)
        self.xStepLineEdit.setObjectName(u"xStepLineEdit")

        self.recipeFormLayout.setWidget(3, QFormLayout.FieldRole, self.xStepLineEdit)

        self.label_zStart = QLabel(self.recipeGroup)
        self.label_zStart.setObjectName(u"label_zStart")

        self.recipeFormLayout.setWidget(4, QFormLayout.LabelRole, self.label_zStart)

        self.zStartLineEdit = QLineEdit(self.recipeGroup)
        self.zStartLineEdit.setObjectName(u"zStartLineEdit")

        self.recipeFormLayout.setWidget(4, QFormLayout.FieldRole, self.zStartLineEdit)

        self.label_zStop = QLabel(self.recipeGroup)
        self.label_zStop.setObjectName(u"label_zStop")

        self.recipeFormLayout.setWidget(5, QFormLayout.LabelRole, self.label_zStop)

        self.zStopLineEdit = QLineEdit(self.recipeGroup)
        self.zStopLineEdit.setObjectName(u"zStopLineEdit")

        self.recipeFormLayout.setWidget(5, QFormLayout.FieldRole, self.zStopLineEdit)

        self.label_zStep = QLabel(self.recipeGroup)
        self.label_zStep.setObjectName(u"label_zStep")

        self.recipeFormLayout.setWidget(6, QFormLayout.LabelRole, self.label_zStep)

        self.zStepLineEdit = QLineEdit(self.recipeGroup)
        self.zStepLineEdit.setObjectName(u"zStepLineEdit")

        self.recipeFormLayout.setWidget(6, QFormLayout.FieldRole, self.zStepLineEdit)

        self.snakingCheckBox = QCheckBox(self.recipeGroup)
        self.snakingCheckBox.setObjectName(u"snakingCheckBox")
        self.snakingCheckBox.setChecked(True)

        self.recipeFormLayout.setWidget(7, QFormLayout.FieldRole, self.snakingCheckBox)

        self.applyRecipeButton = QPushButton(self.recipeGroup)
        self.applyRecipeButton.setObjectName(u"applyRecipeButton")

        self.recipeFormLayout.setWidget(8, QFormLayout.FieldRole, self.applyRecipeButton)


        self.leftLayout.addWidget(self.recipeGroup)

        self.vnaSettingsGroup = QGroupBox(self.leftColumn)
        self.vnaSettingsGroup.setObjectName(u"vnaSettingsGroup")
        self.vnaFormLayout = QFormLayout(self.vnaSettingsGroup)
        self.vnaFormLayout.setObjectName(u"vnaFormLayout")
        self.label_vnaModel = QLabel(self.vnaSettingsGroup)
        self.label_vnaModel.setObjectName(u"label_vnaModel")

        self.vnaFormLayout.setWidget(0, QFormLayout.LabelRole, self.label_vnaModel)

        self.vnaModelCombo = QComboBox(self.vnaSettingsGroup)
        self.vnaModelCombo.addItem("")
        self.vnaModelCombo.addItem("")
        self.vnaModelCombo.setObjectName(u"vnaModelCombo")

        self.vnaFormLayout.setWidget(0, QFormLayout.FieldRole, self.vnaModelCombo)

        self.label_vnaStart = QLabel(self.vnaSettingsGroup)
        self.label_vnaStart.setObjectName(u"label_vnaStart")

        self.vnaFormLayout.setWidget(1, QFormLayout.LabelRole, self.label_vnaStart)

        self.vnaStartSpin = QDoubleSpinBox(self.vnaSettingsGroup)
        self.vnaStartSpin.setObjectName(u"vnaStartSpin")
        self.vnaStartSpin.setDecimals(3)
        self.vnaStartSpin.setMinimum(0.001000000000000)
        self.vnaStartSpin.setMaximum(50.000000000000000)
        self.vnaStartSpin.setValue(1.000000000000000)

        self.vnaFormLayout.setWidget(1, QFormLayout.FieldRole, self.vnaStartSpin)

        self.label_vnaStop = QLabel(self.vnaSettingsGroup)
        self.label_vnaStop.setObjectName(u"label_vnaStop")

        self.vnaFormLayout.setWidget(2, QFormLayout.LabelRole, self.label_vnaStop)

        self.vnaStopSpin = QDoubleSpinBox(self.vnaSettingsGroup)
        self.vnaStopSpin.setObjectName(u"vnaStopSpin")
        self.vnaStopSpin.setDecimals(3)
        self.vnaStopSpin.setMinimum(0.001000000000000)
        self.vnaStopSpin.setMaximum(50.000000000000000)
        self.vnaStopSpin.setValue(14.000000000000000)

        self.vnaFormLayout.setWidget(2, QFormLayout.FieldRole, self.vnaStopSpin)

        self.label_vnaPoints = QLabel(self.vnaSettingsGroup)
        self.label_vnaPoints.setObjectName(u"label_vnaPoints")

        self.vnaFormLayout.setWidget(3, QFormLayout.LabelRole, self.label_vnaPoints)

        self.vnaPointsSpin = QSpinBox(self.vnaSettingsGroup)
        self.vnaPointsSpin.setObjectName(u"vnaPointsSpin")
        self.vnaPointsSpin.setMinimum(11)
        self.vnaPointsSpin.setMaximum(4001)
        self.vnaPointsSpin.setValue(101)

        self.vnaFormLayout.setWidget(3, QFormLayout.FieldRole, self.vnaPointsSpin)

        self.label_vnaIfbw = QLabel(self.vnaSettingsGroup)
        self.label_vnaIfbw.setObjectName(u"label_vnaIfbw")

        self.vnaFormLayout.setWidget(4, QFormLayout.LabelRole, self.label_vnaIfbw)

        self.vnaIfbwSpin = QDoubleSpinBox(self.vnaSettingsGroup)
        self.vnaIfbwSpin.setObjectName(u"vnaIfbwSpin")
        self.vnaIfbwSpin.setMinimum(1.000000000000000)
        self.vnaIfbwSpin.setMaximum(1000000.000000000000000)
        self.vnaIfbwSpin.setValue(1000.000000000000000)

        self.vnaFormLayout.setWidget(4, QFormLayout.FieldRole, self.vnaIfbwSpin)

        self.label_vnaPower = QLabel(self.vnaSettingsGroup)
        self.label_vnaPower.setObjectName(u"label_vnaPower")

        self.vnaFormLayout.setWidget(5, QFormLayout.LabelRole, self.label_vnaPower)

        self.vnaPowerSpin = QDoubleSpinBox(self.vnaSettingsGroup)
        self.vnaPowerSpin.setObjectName(u"vnaPowerSpin")
        self.vnaPowerSpin.setMinimum(-60.000000000000000)
        self.vnaPowerSpin.setMaximum(20.000000000000000)
        self.vnaPowerSpin.setValue(-10.000000000000000)

        self.vnaFormLayout.setWidget(5, QFormLayout.FieldRole, self.vnaPowerSpin)

        self.applyVnaButton = QPushButton(self.vnaSettingsGroup)
        self.applyVnaButton.setObjectName(u"applyVnaButton")

        self.vnaFormLayout.setWidget(6, QFormLayout.FieldRole, self.applyVnaButton)


        self.leftLayout.addWidget(self.vnaSettingsGroup)

        self.mainSplitter.addWidget(self.leftColumn)
        self.centerColumn = QWidget(self.mainSplitter)
        self.centerColumn.setObjectName(u"centerColumn")
        self.centerLayout = QVBoxLayout(self.centerColumn)
        self.centerLayout.setObjectName(u"centerLayout")
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.scanControlGroup = QGroupBox(self.centerColumn)
        self.scanControlGroup.setObjectName(u"scanControlGroup")
        self.scanControlLayout = QVBoxLayout(self.scanControlGroup)
        self.scanControlLayout.setObjectName(u"scanControlLayout")
        self.scanButtonsLayout = QHBoxLayout()
        self.scanButtonsLayout.setObjectName(u"scanButtonsLayout")
        self.startScanButton = QPushButton(self.scanControlGroup)
        self.startScanButton.setObjectName(u"startScanButton")

        self.scanButtonsLayout.addWidget(self.startScanButton)

        self.pauseScanButton = QPushButton(self.scanControlGroup)
        self.pauseScanButton.setObjectName(u"pauseScanButton")

        self.scanButtonsLayout.addWidget(self.pauseScanButton)

        self.resumeScanButton = QPushButton(self.scanControlGroup)
        self.resumeScanButton.setObjectName(u"resumeScanButton")

        self.scanButtonsLayout.addWidget(self.resumeScanButton)

        self.abortScanButton = QPushButton(self.scanControlGroup)
        self.abortScanButton.setObjectName(u"abortScanButton")

        self.scanButtonsLayout.addWidget(self.abortScanButton)

        self.downloadReportButton = QPushButton(self.scanControlGroup)
        self.downloadReportButton.setObjectName(u"downloadReportButton")

        self.scanButtonsLayout.addWidget(self.downloadReportButton)


        self.scanControlLayout.addLayout(self.scanButtonsLayout)

        self.scanProgressBar = QProgressBar(self.scanControlGroup)
        self.scanProgressBar.setObjectName(u"scanProgressBar")
        self.scanProgressBar.setValue(0)

        self.scanControlLayout.addWidget(self.scanProgressBar)

        self.progressLabel = QLabel(self.scanControlGroup)
        self.progressLabel.setObjectName(u"progressLabel")

        self.scanControlLayout.addWidget(self.progressLabel)

        self.gainSideLabel = QLabel(self.scanControlGroup)
        self.gainSideLabel.setObjectName(u"gainSideLabel")

        self.scanControlLayout.addWidget(self.gainSideLabel)

        self.scanToolsLayout = QHBoxLayout()
        self.scanToolsLayout.setObjectName(u"scanToolsLayout")
        self.selfCheckButton = QPushButton(self.scanControlGroup)
        self.selfCheckButton.setObjectName(u"selfCheckButton")

        self.scanToolsLayout.addWidget(self.selfCheckButton)

        self.functionTestButton = QPushButton(self.scanControlGroup)
        self.functionTestButton.setObjectName(u"functionTestButton")

        self.scanToolsLayout.addWidget(self.functionTestButton)

        self.loadIcdButton = QPushButton(self.scanControlGroup)
        self.loadIcdButton.setObjectName(u"loadIcdButton")

        self.scanToolsLayout.addWidget(self.loadIcdButton)


        self.scanControlLayout.addLayout(self.scanToolsLayout)

        self.icdPathLabel = QLabel(self.scanControlGroup)
        self.icdPathLabel.setObjectName(u"icdPathLabel")

        self.scanControlLayout.addWidget(self.icdPathLabel)

        self.icdMapLabel = QLabel(self.scanControlGroup)
        self.icdMapLabel.setObjectName(u"icdMapLabel")

        self.scanControlLayout.addWidget(self.icdMapLabel)


        self.centerLayout.addWidget(self.scanControlGroup)

        self.traceGroup = QGroupBox(self.centerColumn)
        self.traceGroup.setObjectName(u"traceGroup")
        self.traceLayout = QVBoxLayout(self.traceGroup)
        self.traceLayout.setObjectName(u"traceLayout")
        self.tracePlaceholderFrame = QFrame(self.traceGroup)
        self.tracePlaceholderFrame.setObjectName(u"tracePlaceholderFrame")
        self.tracePlaceholderFrame.setFrameShape(QFrame.StyledPanel)
        self.tracePlaceholderLayout = QVBoxLayout(self.tracePlaceholderFrame)
        self.tracePlaceholderLayout.setObjectName(u"tracePlaceholderLayout")
        self.tracePlaceholderLabel = QLabel(self.tracePlaceholderFrame)
        self.tracePlaceholderLabel.setObjectName(u"tracePlaceholderLabel")

        self.tracePlaceholderLayout.addWidget(self.tracePlaceholderLabel)


        self.traceLayout.addWidget(self.tracePlaceholderFrame)


        self.centerLayout.addWidget(self.traceGroup)

        self.heatmapGroup = QGroupBox(self.centerColumn)
        self.heatmapGroup.setObjectName(u"heatmapGroup")
        self.heatmapLayout = QVBoxLayout(self.heatmapGroup)
        self.heatmapLayout.setObjectName(u"heatmapLayout")
        self.heatmapPlaceholderFrame = QFrame(self.heatmapGroup)
        self.heatmapPlaceholderFrame.setObjectName(u"heatmapPlaceholderFrame")
        self.heatmapPlaceholderFrame.setFrameShape(QFrame.StyledPanel)
        self.heatmapPlaceholderLayout = QVBoxLayout(self.heatmapPlaceholderFrame)
        self.heatmapPlaceholderLayout.setObjectName(u"heatmapPlaceholderLayout")
        self.heatmapPlaceholderLabel = QLabel(self.heatmapPlaceholderFrame)
        self.heatmapPlaceholderLabel.setObjectName(u"heatmapPlaceholderLabel")

        self.heatmapPlaceholderLayout.addWidget(self.heatmapPlaceholderLabel)


        self.heatmapLayout.addWidget(self.heatmapPlaceholderFrame)


        self.centerLayout.addWidget(self.heatmapGroup)

        self.mainSplitter.addWidget(self.centerColumn)
        self.rightColumn = QWidget(self.mainSplitter)
        self.rightColumn.setObjectName(u"rightColumn")
        self.rightLayout = QVBoxLayout(self.rightColumn)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.timeSeriesGroup = QGroupBox(self.rightColumn)
        self.timeSeriesGroup.setObjectName(u"timeSeriesGroup")
        self.timeSeriesLayout = QVBoxLayout(self.timeSeriesGroup)
        self.timeSeriesLayout.setObjectName(u"timeSeriesLayout")
        self.timePlaceholderFrame = QFrame(self.timeSeriesGroup)
        self.timePlaceholderFrame.setObjectName(u"timePlaceholderFrame")
        self.timePlaceholderFrame.setFrameShape(QFrame.StyledPanel)
        self.timePlaceholderLayout = QVBoxLayout(self.timePlaceholderFrame)
        self.timePlaceholderLayout.setObjectName(u"timePlaceholderLayout")
        self.timePlaceholderLabel = QLabel(self.timePlaceholderFrame)
        self.timePlaceholderLabel.setObjectName(u"timePlaceholderLabel")

        self.timePlaceholderLayout.addWidget(self.timePlaceholderLabel)


        self.timeSeriesLayout.addWidget(self.timePlaceholderFrame)


        self.rightLayout.addWidget(self.timeSeriesGroup)

        self.scanPlanGroup = QGroupBox(self.rightColumn)
        self.scanPlanGroup.setObjectName(u"scanPlanGroup")
        self.scanPlanLayout = QVBoxLayout(self.scanPlanGroup)
        self.scanPlanLayout.setObjectName(u"scanPlanLayout")
        self.scanPlanPlaceholderFrame = QFrame(self.scanPlanGroup)
        self.scanPlanPlaceholderFrame.setObjectName(u"scanPlanPlaceholderFrame")
        self.scanPlanPlaceholderFrame.setFrameShape(QFrame.StyledPanel)
        self.scanPlanPlaceholderLayout = QVBoxLayout(self.scanPlanPlaceholderFrame)
        self.scanPlanPlaceholderLayout.setObjectName(u"scanPlanPlaceholderLayout")
        self.scanPlanPlaceholderLabel = QLabel(self.scanPlanPlaceholderFrame)
        self.scanPlanPlaceholderLabel.setObjectName(u"scanPlanPlaceholderLabel")

        self.scanPlanPlaceholderLayout.addWidget(self.scanPlanPlaceholderLabel)


        self.scanPlanLayout.addWidget(self.scanPlanPlaceholderFrame)


        self.rightLayout.addWidget(self.scanPlanGroup)

        self.alarmLogGroup = QGroupBox(self.rightColumn)
        self.alarmLogGroup.setObjectName(u"alarmLogGroup")
        self.alarmLogLayout = QVBoxLayout(self.alarmLogGroup)
        self.alarmLogLayout.setObjectName(u"alarmLogLayout")
        self.logTable = QTableWidget(self.alarmLogGroup)
        if (self.logTable.columnCount() < 3):
            self.logTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.logTable.setObjectName(u"logTable")

        self.alarmLogLayout.addWidget(self.logTable)

        self.clearLogButton = QPushButton(self.alarmLogGroup)
        self.clearLogButton.setObjectName(u"clearLogButton")

        self.alarmLogLayout.addWidget(self.clearLogButton)


        self.rightLayout.addWidget(self.alarmLogGroup)

        self.mainSplitter.addWidget(self.rightColumn)

        self.rootLayout.addWidget(self.mainSplitter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"XZ Pozisyoner Ana Kontrol - Full UI", None))
        self.projectLabel.setText(QCoreApplication.translate("MainWindow", u"Proje: Demo_24GHz_Antenna", None))
        self.recipeLabel.setText(QCoreApplication.translate("MainWindow", u"Aktif Recete: Plane_XZ_Scan_5mm", None))
        self.runtimeModeCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"DEMO", None))
        self.runtimeModeCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"HARDWARE", None))

        self.realVnaCheckBox.setText(QCoreApplication.translate("MainWindow", u"Real VNA", None))
        self.vnaConnectButton.setText(QCoreApplication.translate("MainWindow", u"VNA Baglantisi", None))
        self.layoutToggleButton.setText(QCoreApplication.translate("MainWindow", u"Ayarlar: Kilitli", None))
        self.fullscreenButton.setText(QCoreApplication.translate("MainWindow", u"Tam Ekran", None))
        self.dryRunButton.setText(QCoreApplication.translate("MainWindow", u"Dry-Run", None))
        self.modeLabel.setText(QCoreApplication.translate("MainWindow", u"Sistem Modu: READY", None))
        self.gainLabel.setText(QCoreApplication.translate("MainWindow", u"Gain (Peak): - dB", None))
        self.safetyLabel.setText(QCoreApplication.translate("MainWindow", u"Safety: READY", None))
        self.ttlLabel.setText(QCoreApplication.translate("MainWindow", u"TTL Sayac: 0", None))
        self.manualGroup.setTitle(QCoreApplication.translate("MainWindow", u"Manuel Kontrol - X/Z", None))
        self.xPosLabel.setText(QCoreApplication.translate("MainWindow", u"X Konum: 0.00 mm", None))
        self.zPosLabel.setText(QCoreApplication.translate("MainWindow", u"Z Konum: 0.00 mm", None))
        self.xSpeedText.setText(QCoreApplication.translate("MainWindow", u"X hiz", None))
        self.xSpeedLineEdit.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.zSpeedText.setText(QCoreApplication.translate("MainWindow", u"Z hiz", None))
        self.zSpeedLineEdit.setText(QCoreApplication.translate("MainWindow", u"150", None))
        self.applySpeedButton.setText(QCoreApplication.translate("MainWindow", u"Hiz Uygula", None))
        self.jogXmButton.setText(QCoreApplication.translate("MainWindow", u"X Jog -", None))
        self.jogXpButton.setText(QCoreApplication.translate("MainWindow", u"X Jog +", None))
        self.jogZmButton.setText(QCoreApplication.translate("MainWindow", u"Z Jog -", None))
        self.jogZpButton.setText(QCoreApplication.translate("MainWindow", u"Z Jog +", None))
        self.homeButton.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.parkButton.setText(QCoreApplication.translate("MainWindow", u"Park", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.estopButton.setText(QCoreApplication.translate("MainWindow", u"E-STOP", None))
        self.estopResetButton.setText(QCoreApplication.translate("MainWindow", u"E-STOP Reset", None))
        self.xLimitCheckBox.setText(QCoreApplication.translate("MainWindow", u"X Limit", None))
        self.zLimitCheckBox.setText(QCoreApplication.translate("MainWindow", u"Z Limit", None))
        self.recipeGroup.setTitle(QCoreApplication.translate("MainWindow", u"Tarama Recetesi", None))
        self.label_recipeName.setText(QCoreApplication.translate("MainWindow", u"Recete Adi", None))
        self.recipeNameLineEdit.setText(QCoreApplication.translate("MainWindow", u"Plane_XZ_Scan_5mm", None))
        self.label_xStart.setText(QCoreApplication.translate("MainWindow", u"X Baslangic (mm)", None))
        self.xStartLineEdit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_xStop.setText(QCoreApplication.translate("MainWindow", u"X Bitis (mm)", None))
        self.xStopLineEdit.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.label_xStep.setText(QCoreApplication.translate("MainWindow", u"X Adim (mm)", None))
        self.xStepLineEdit.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_zStart.setText(QCoreApplication.translate("MainWindow", u"Z Baslangic (mm)", None))
        self.zStartLineEdit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_zStop.setText(QCoreApplication.translate("MainWindow", u"Z Bitis (mm)", None))
        self.zStopLineEdit.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.label_zStep.setText(QCoreApplication.translate("MainWindow", u"Z Adim (mm)", None))
        self.zStepLineEdit.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.snakingCheckBox.setText(QCoreApplication.translate("MainWindow", u"Snaking", None))
        self.applyRecipeButton.setText(QCoreApplication.translate("MainWindow", u"Receteyi Uygula", None))
        self.vnaSettingsGroup.setTitle(QCoreApplication.translate("MainWindow", u"VNA Ayarlari", None))
        self.label_vnaModel.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.vnaModelCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"R&S ZNL14", None))
        self.vnaModelCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Keysight N9917B", None))

        self.label_vnaStart.setText(QCoreApplication.translate("MainWindow", u"Start (GHz)", None))
        self.label_vnaStop.setText(QCoreApplication.translate("MainWindow", u"Stop (GHz)", None))
        self.label_vnaPoints.setText(QCoreApplication.translate("MainWindow", u"Points", None))
        self.label_vnaIfbw.setText(QCoreApplication.translate("MainWindow", u"IFBW (Hz)", None))
        self.label_vnaPower.setText(QCoreApplication.translate("MainWindow", u"Power (dBm)", None))
        self.applyVnaButton.setText(QCoreApplication.translate("MainWindow", u"VNA Ayarlari Uygula", None))
        self.scanControlGroup.setTitle(QCoreApplication.translate("MainWindow", u"Otomatik Tarama / ICD / Gain", None))
        self.startScanButton.setText(QCoreApplication.translate("MainWindow", u"Baslat", None))
        self.pauseScanButton.setText(QCoreApplication.translate("MainWindow", u"Duraklat", None))
        self.resumeScanButton.setText(QCoreApplication.translate("MainWindow", u"Devam", None))
        self.abortScanButton.setText(QCoreApplication.translate("MainWindow", u"Iptal", None))
        self.downloadReportButton.setText(QCoreApplication.translate("MainWindow", u"Raporu Indir", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWindow", u"Ilerleme: 0/0", None))
        self.gainSideLabel.setText(QCoreApplication.translate("MainWindow", u"Gain (Peak): - dB", None))
        self.selfCheckButton.setText(QCoreApplication.translate("MainWindow", u"Self-Check", None))
        self.functionTestButton.setText(QCoreApplication.translate("MainWindow", u"Fonksiyon Testi", None))
        self.loadIcdButton.setText(QCoreApplication.translate("MainWindow", u"ICD Yukle", None))
        self.icdPathLabel.setText(QCoreApplication.translate("MainWindow", u"ICD: yuklenmedi", None))
        self.icdMapLabel.setText(QCoreApplication.translate("MainWindow", u"Map: beklemede", None))
        self.traceGroup.setTitle(QCoreApplication.translate("MainWindow", u"Canli S21 Trace", None))
        self.tracePlaceholderLabel.setText(QCoreApplication.translate("MainWindow", u"Trace Grafik Alani", None))
        self.heatmapGroup.setTitle(QCoreApplication.translate("MainWindow", u"XZ Tarama Haritasi", None))
        self.heatmapPlaceholderLabel.setText(QCoreApplication.translate("MainWindow", u"Heatmap Grafik Alani", None))
        self.timeSeriesGroup.setTitle(QCoreApplication.translate("MainWindow", u"S21 Zaman Akisi", None))
        self.timePlaceholderLabel.setText(QCoreApplication.translate("MainWindow", u"Zaman Grafik Alani", None))
        self.scanPlanGroup.setTitle(QCoreApplication.translate("MainWindow", u"Tarama Nokta Plani", None))
        self.scanPlanPlaceholderLabel.setText(QCoreApplication.translate("MainWindow", u"Tarama Plani Grafik Alani", None))
        self.alarmLogGroup.setTitle(QCoreApplication.translate("MainWindow", u"Alarm / Log", None))
        ___qtablewidgetitem = self.logTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Seviye", None));
        ___qtablewidgetitem1 = self.logTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Kaynak", None));
        ___qtablewidgetitem2 = self.logTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Mesaj", None));
        self.clearLogButton.setText(QCoreApplication.translate("MainWindow", u"Temizle", None))
    # retranslateUi

