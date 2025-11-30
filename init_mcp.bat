@echo off
setlocal

set "ENV_FILE=.env"
set "VENV_DIR=.venv"
set "MARKER_FILE=%VENV_DIR%\.deps_installed"

REM Load .env if present (optional, skip comments)
if exist "%ENV_FILE%" (
    for /f "usebackq eol=# tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
        set "%%A=%%B"
    )
    echo [init_mcp.bat] Environment variables loaded from %ENV_FILE%.
) else (
    echo [init_mcp.bat] Warning: %ENV_FILE% not found. Continuing without env variables...
)

REM Ensure python exists
where python >nul 2>nul
if errorlevel 1 (
    echo [init_mcp.bat] Error: Python not found in PATH.
    exit /b 1
)

REM Remove existing venv
if exist "%VENV_DIR%" (
    echo [init_mcp.bat] Removing existing virtual environment at %VENV_DIR%...
    rmdir /s /q "%VENV_DIR%"
)

echo [init_mcp.bat] Creating virtual environment in %VENV_DIR%...
python -m venv "%VENV_DIR%"

call "%VENV_DIR%\Scripts\activate.bat"

if not exist "requirements.txt" (
    echo [init_mcp.bat] Error: requirements.txt not found.
    exit /b 1
)

echo [init_mcp.bat] Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Mark deps as installed so run_mcp.bat can skip reinstall
> "%MARKER_FILE%" type nul

echo [init_mcp.bat] Initialization complete. You can now run run_mcp.bat

endlocal
