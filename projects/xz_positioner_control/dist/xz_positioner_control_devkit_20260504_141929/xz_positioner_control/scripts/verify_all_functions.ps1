param(
  [string]$ProjectRoot = "C:\Users\mzeray\Documents\Web-Automation-V2\projects\xz_positioner_control"
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$env:PYTHONPATH = "src"
$py = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

& $py -m pytest -q tests
if ($LASTEXITCODE -ne 0) {
  throw "Test suite failed"
}

Write-Host "All function tests passed."
