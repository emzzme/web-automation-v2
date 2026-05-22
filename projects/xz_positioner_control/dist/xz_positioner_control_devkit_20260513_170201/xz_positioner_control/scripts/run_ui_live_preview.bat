@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "PY=%ROOT_DIR%\.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo .venv bulunamadi. Once scripts\setup_dev_env.bat calistirin.
  pause
  exit /b 1
)
set "PYTHONPATH=%ROOT_DIR%\src"
set "XZ_UI_MODE=ui"
"%PY%" -m xz_control_ui.ui.live_preview
