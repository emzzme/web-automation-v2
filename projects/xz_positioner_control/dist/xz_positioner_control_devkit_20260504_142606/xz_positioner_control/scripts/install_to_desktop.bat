@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install_to_desktop.ps1"
if errorlevel 1 (
  echo Masaustune kurulum basarisiz.
  pause
  exit /b 1
)
echo Masaustune kurulum tamamlandi.
pause
