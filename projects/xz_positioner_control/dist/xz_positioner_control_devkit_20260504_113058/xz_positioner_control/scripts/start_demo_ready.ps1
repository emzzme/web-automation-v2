param(
  [string]$ProjectRoot = "C:\Users\mzeray\Documents\Web-Automation-V2\projects\xz_positioner_control"
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$venvPy = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
  powershell -ExecutionPolicy Bypass -File scripts\run_demo.ps1
  exit 0
}

if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "src;$env:PYTHONPATH"
} else {
  $env:PYTHONPATH = "src"
}

& $venvPy scripts\smoke_demo.py
if ($LASTEXITCODE -ne 0) {
  throw "Smoke test failed"
}

Write-Host "Smoke test passed. Launching demo UI..."
& $venvPy -m xz_control_ui.main
