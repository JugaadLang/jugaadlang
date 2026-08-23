@echo off
setlocal EnableExtensions
chcp >nul 65001

for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[0;31m"
set "GREEN=%ESC%[0;32m"
set "BLUE=%ESC%[0;34m"
set "YELLOW=%ESC%[1;33m"
set "NC=%ESC%[0m"

set "PORT=8000"
echo %YELLOW%⚡ Starting local web server for JugaadLang website on port %PORT%...%NC%

REM Find python interpreter
set "PYTHON_CMD=python"
where python >nul 2>nul || set "PYTHON_CMD=py"
where %PYTHON_CMD% >nul 2>nul
if errorlevel 1 (
    echo %RED%✗ Error: Python is required to run the local server.%NC%
    exit /b 1
)

REM Open the browser once the server has spun up
echo %BLUE%⚡ Launching browser...%NC%
start "" cmd /c "timeout /t 2 /nobreak >nul & start "" http://localhost:%PORT%"

echo %GREEN%✓ Local website server is running!%NC%
echo Press Ctrl+C to stop the server.

REM Run the server in the foreground; Ctrl+C stops it
%PYTHON_CMD% -m http.server --directory website %PORT%

echo %YELLOW%⚡ Stopping server...%NC%
