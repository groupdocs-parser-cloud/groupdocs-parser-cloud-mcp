@echo off
setlocal

set "ENV_FILE=.env"
set "VENV_DIR=.venv"
set "MARKER_FILE=%VENV_DIR%\.deps_installed"

if not exist "%ENV_FILE%" (
    echo [run_mcp.bat] Error: %ENV_FILE% file not found. Create it before running this script.
    exit /b 1
)

REM Load variables from .env (skip comments)
for /f "usebackq eol=# tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
    set "%%A=%%B"
)

echo [run_mcp.bat] Environment variables loaded.

REM Ensure python exists
where python >nul 2>nul
if errorlevel 1 (
    echo [run_mcp.bat] Python not found in PATH.
    exit /b 1
)

REM Create venv
if not exist "%VENV_DIR%" (
    echo [run_mcp.bat] Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"

REM Install requirements
if not exist "%MARKER_FILE%" (
    if not exist "requirements.txt" (
        echo [run_mcp.bat] Error: requirements.txt not found.
        exit /b 1
    )
    echo [run_mcp.bat] Installing dependencies...
    pip install -r requirements.txt
    > "%MARKER_FILE%" type nul
    echo [run_mcp.bat] Dependencies installed.
)

echo [run_mcp.bat] Starting MCP server...
python src\server.py

endlocal

