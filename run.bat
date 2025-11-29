@echo off
REM ================================
REM Load environment variables from .env
REM ================================

if not exist ".env" (
    echo .env file not found!
    exit /b 1
)

REM for /f:
REM   - usebackq  -> allows quoted filename ".env"
REM   - eol=#     -> lines starting with # are treated as comments
REM   - tokens=1,* delims== -> split into NAME (%%A) and VALUE (%%B) by '='
for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
    set "%%A=%%B"
)

echo Environment variables loaded:
echo CLIENT_ID=%CLIENT_ID%
echo CLIENT_SECRET=%CLIENT_SECRET%
echo MCP_PORT=%MCP_PORT%

REM ================================
REM Run the Python server
REM ================================
python src/server.py
