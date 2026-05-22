param(
  [string]$ProjectRoot = "$(Split-Path -Parent $PSScriptRoot)"
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

Write-Host "[1/5] Python kontrol ediliyor..."
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
  Write-Host "Python bulunamadi. Python 3.11+ kurup tekrar calistirin." -ForegroundColor Red
  exit 1
}

Write-Host "[2/5] Sanal ortam olusturuluyor..."
if (-not (Test-Path ".venv\\Scripts\\python.exe")) {
  python -m venv .venv
}

$venvPy = Join-Path $ProjectRoot ".venv\\Scripts\\python.exe"

Write-Host "[3/5] Pip guncelleniyor..."
& $venvPy -m pip install --upgrade pip

Write-Host "[4/5] Bagimliliklar kuruluyor..."
& $venvPy -m pip install -r requirements.txt

Write-Host "[5/5] Hızlı dogrulama..."
if ($env:PYTHONPATH) {
  $env:PYTHONPATH = "src;$env:PYTHONPATH"
} else {
  $env:PYTHONPATH = "src"
}
& $venvPy -m py_compile src\\xz_control_ui\\main.py

Write-Host "Kurulum tamamlandi."
Write-Host "Demo baslatmak icin: scripts\\launch_demo.bat"
Write-Host "Test icin: scripts\\run_tests.bat"
