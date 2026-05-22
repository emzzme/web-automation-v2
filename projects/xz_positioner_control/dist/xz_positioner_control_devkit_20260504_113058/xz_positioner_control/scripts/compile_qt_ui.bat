@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "UI_FILE=%ROOT_DIR%\src\xz_control_ui\ui\main_window.ui"
set "OUT_PY=%ROOT_DIR%\src\xz_control_ui\ui\main_window_ui.py"

if not exist "%ROOT_DIR%\.venv\Scripts\pyside6-uic.exe" (
  echo pyside6-uic bulunamadi. Once scripts\setup_dev_env.bat calistirin.
  pause
  exit /b 1
)

"%ROOT_DIR%\.venv\Scripts\pyside6-uic.exe" "%UI_FILE%" -o "%OUT_PY%"
echo Uretildi: %OUT_PY%
pause
