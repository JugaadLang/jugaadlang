@echo off
setlocal EnableExtensions
chcp >nul 65001

REM ANSI colors (Windows 10+ terminal)
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[0;31m"
set "GREEN=%ESC%[0;32m"
set "BLUE=%ESC%[0;34m"
set "YELLOW=%ESC%[1;33m"
set "NC=%ESC%[0m"

REM Exit immediately if a command exits with a non-zero status (|| exit /b 1)

REM Prefer the project virtualenv's interpreter when present
set "PYTHON=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PYTHON=%~dp0.venv\Scripts\python.exe"

if "%~1"=="" goto run_all
if /I "%~1"=="test" goto run_test
if /I "%~1"=="build" goto run_build
if /I "%~1"=="install" goto run_install
if /I "%~1"=="web" goto run_web
if /I "%~1"=="website" goto run_web
goto show_help

:show_help
echo %BLUE%JugaadLang Development Script%NC%
echo Usage: run.bat [command]
echo.
echo Commands:
echo   test    - Run test suite using pytest
echo   build   - Build source ^(sdist^) and binary ^(wheel^) distributions
echo   install - Install local package in editable mode with all optional dependencies
echo   web     - Serve the landing website locally and open it in browser
echo   all     - Run tests, build the package, and install it
echo   help    - Show this help message
exit /b 0

:run_test
echo %YELLOW%⚡ Ensuring dependencies are installed...%NC%
uv pip install -e .[all] || exit /b 1
echo %YELLOW%⚡ Running test suite...%NC%
%PYTHON% -m pytest || exit /b 1
echo %GREEN%✓ Tests completed successfully!%NC%
exit /b 0

:run_build
echo %YELLOW%⚡ Building JugaadLang package...%NC%
uv pip install --upgrade build || exit /b 1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
%PYTHON% -m build || exit /b 1
echo %GREEN%✓ Package built successfully (artifacts in dist/)%NC%
exit /b 0

:run_install
echo %YELLOW%⚡ Installing JugaadLang locally...%NC%
uv pip install -e .[all] || exit /b 1
echo %GREEN%✓ Package installed successfully in editable mode!%NC%
echo You can now run '%BLUE%jug%NC%' command from anywhere!
exit /b 0

:run_web
call "%~dp0run_website.bat"
exit /b %errorlevel%

:run_all
call :run_test || exit /b 1
call :run_build || exit /b 1
call :run_install || exit /b 1
exit /b 0
