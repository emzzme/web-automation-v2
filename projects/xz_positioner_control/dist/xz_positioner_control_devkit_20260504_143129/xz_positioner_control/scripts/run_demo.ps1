param(
  [string]$ProjectRoot = "C:\Users\mzeray\Documents\Web-Automation-V2\projects\xz_positioner_control"
)
$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$py = "C:\Users\mzeray\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path ".venv")) {
  & $py -m venv .venv
}
$venvPip = Join-Path $ProjectRoot ".venv\Scripts\pip.exe"
$venvPy = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

& $venvPip install -r requirements.txt
if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "src;$env:PYTHONPATH"
} else {
  $env:PYTHONPATH = "src"
}
& $venvPy -m xz_control_ui.main
