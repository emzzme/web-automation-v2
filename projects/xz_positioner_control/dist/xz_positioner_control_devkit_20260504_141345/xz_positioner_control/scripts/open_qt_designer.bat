@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "UI_FILE=%ROOT_DIR%\src\xz_control_ui\ui\main_window.ui"

if not exist "%ROOT_DIR%\.venv\Scripts\pyside6-designer.exe" (
  echo pyside6-designer bulunamadi. Once scripts\setup_dev_env.bat calistirin.
  pause
  exit /b 1
)

"%ROOT_DIR%\.venv\Scripts\pyside6-designer.exe" "%UI_FILE%"
