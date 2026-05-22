@echo off
setlocal
cd /d "%~dp0"

echo [1/4] Gelistirme ortami kuruluyor...
call scripts\setup_dev_env.bat
if errorlevel 1 (
  echo Kurulum basarisiz.
  pause
  exit /b 1
)

echo [2/4] H?zl? testler calisiyor...
call scripts\run_tests.bat
if errorlevel 1 (
  echo Testler basarisiz. L?tfen loglari kontrol edin.
  pause
  exit /b 1
)

echo [3/4] Demo baslatiliyor...
start "XZ Demo" cmd /c scripts\launch_demo_full.bat

echo [4/4] Devam dokumani aciliyor...
if exist docs\CONTINUE_FROM_HERE_TR.md (
  start "" docs\CONTINUE_FROM_HERE_TR.md
)

echo Hazir. Bu klasorde gelistirmeye devam edebilirsiniz.
pause
