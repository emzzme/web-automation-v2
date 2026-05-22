@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%scripts\build_dev_bundle.ps1"
if errorlevel 1 (
  echo Bundle olusturma basarisiz.
  pause
  exit /b 1
)
echo Bundle olusturuldu.
pause
