param(
  [string]$ProjectRoot = "$(Split-Path -Parent $PSScriptRoot)",
  [string]$OutDir = "$(Join-Path (Split-Path -Parent $PSScriptRoot) 'dist')"
)

$ErrorActionPreference = "Stop"

$projectName = "xz_positioner_control"
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$bundleRoot = Join-Path $OutDir ("{0}_devkit_{1}" -f $projectName, $stamp)
$bundleProject = Join-Path $bundleRoot $projectName
$zipPath = "$bundleRoot.zip"

New-Item -ItemType Directory -Force -Path $bundleProject | Out-Null

$excludeDirs = @(
  ".venv",
  "dist",
  "build",
  "__pycache__",
  ".pytest_cache",
  ".git"
)

$excludeFiles = @(
  "*.pyc",
  "*.pyo",
  "*.log"
)

$robocopyArgs = @(
  $ProjectRoot,
  $bundleProject,
  "/MIR",
  "/R:1",
  "/W:1",
  "/NFL",
  "/NDL",
  "/NP",
  "/NJH",
  "/NJS"
)

foreach ($d in $excludeDirs) { $robocopyArgs += @("/XD", $d) }
foreach ($f in $excludeFiles) { $robocopyArgs += @("/XF", $f) }
$robocopyArgs += @("/XD", "pytest-cache-files-*")

& robocopy @robocopyArgs | Out-Null
$rc = $LASTEXITCODE
if ($rc -ge 8) {
  throw "Robocopy basarisiz. Cikis kodu: $rc"
}

$readme = @"
XZ Positioner Control - Dev Kit

1) scripts\\setup_dev_env.bat dosyasini calistirin.
2) Qt Designer: scripts\\open_qt_designer.bat
3) Canli UI onizleme: scripts\\run_ui_live_preview.bat
4) Tam fonksiyonlu demo: scripts\\launch_demo_full.bat
5) Testler: scripts\\run_tests.bat
6) Adim adim UI gelistirme rehberi:
   docs\\qt_designer_gelistirme_rehberi_tr.md

VS Code kullanimi:
- Klasoru acin: $projectName
- .vscode ayarlari otomatik yuklenir.
- Tasklar: Setup Dev Environment / Run Demo / Run Tests
"@

$readme | Set-Content -LiteralPath (Join-Path $bundleRoot "START_HERE.txt") -Encoding UTF8

if (Test-Path $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
Compress-Archive -Path $bundleRoot -DestinationPath $zipPath -Force

Write-Host "Bundle hazir: $zipPath"
