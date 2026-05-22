param(
  [string]$SourceRoot = "$(Split-Path -Parent $PSScriptRoot)",
  [string]$TargetName = "XZ_Positioner_Control_Dev"
)

$ErrorActionPreference = "Stop"
$desktop = [Environment]::GetFolderPath("Desktop")
$target = Join-Path $desktop $TargetName

Write-Host "Masaustu hedefi: $target"
if (Test-Path $target) {
  Write-Host "Mevcut klasor siliniyor: $target"
  Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Directory -Path $target | Out-Null

$excludeDirs = @(".venv", "dist", "build", "__pycache__", ".pytest_cache", ".git")
$excludeFiles = @("*.pyc", "*.pyo", "*.log")

$robocopyArgs = @(
  $SourceRoot,
  $target,
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
$robocopyArgs += @("/XD", "pytest-cache-files-*")
foreach ($f in $excludeFiles) { $robocopyArgs += @("/XF", $f) }

& robocopy @robocopyArgs | Out-Null
if ($LASTEXITCODE -ge 8) {
  throw "Kopyalama hatasi. Cikis kodu: $LASTEXITCODE"
}

Write-Host "Kurulum hazirligi basliyor..."
& powershell -ExecutionPolicy Bypass -File (Join-Path $target "scripts\\setup_dev_env.ps1") -ProjectRoot $target

Write-Host "Tamamlandi. Proje klasoru: $target"
