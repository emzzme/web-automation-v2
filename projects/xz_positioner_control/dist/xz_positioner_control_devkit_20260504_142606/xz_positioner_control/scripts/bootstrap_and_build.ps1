param(
  [string]$ProjectRoot = "C:\Users\mzeray\Documents\Web-Automation-V2\projects\xz_positioner_control",
  [string]$IcdPath = ""
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$py = "C:\Users\mzeray\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path ".venv")) {
  & $py -m venv .venv
}

$venvPy = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$venvPip = Join-Path $ProjectRoot ".venv\Scripts\pip.exe"

& $venvPip install -r requirements.txt
& $venvPip install pyinstaller

if ($IcdPath -ne "") {
  & $venvPy scripts\resumable_pipeline.py --root $ProjectRoot --icd $IcdPath
} else {
  & $venvPy scripts\resumable_pipeline.py --root $ProjectRoot
}

& $venvPy -m PyInstaller --noconfirm --windowed --name XZControlUI --paths src --add-data "src\xz_control_ui\ui\theme.qss;xz_control_ui\ui" src\xz_control_ui\main.py

Write-Host "Build complete. EXE path: $ProjectRoot\dist\XZControlUI\XZControlUI.exe"
Write-Host "If Inno Setup is installed, run scripts\make_setup.ps1 for setup.exe"
