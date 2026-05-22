@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%setup_dev_env.ps1"
if errorlevel 1 (
  echo Kurulum basarisiz.
  pause
  exit /b 1
)
echo Kurulum tamamlandi.
pause
