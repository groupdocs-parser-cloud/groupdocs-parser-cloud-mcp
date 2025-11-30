#!/usr/bin/env bash
set -e

ENV_FILE=".env"
VENV_DIR=".venv"
MARKER_FILE="$VENV_DIR/.deps_installed"

if [ ! -f "$ENV_FILE" ]; then
  echo "[run_mcp.sh] Error: $ENV_FILE file not found. Create it before running this script."
  exit 1
fi

# Load environment variables safely
set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

echo "[run_mcp.sh] Environment variables loaded."

# Pick python command
PYTHON_CMD="python3"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

# Create venv
if [ ! -d "$VENV_DIR" ]; then
  echo "[run_mcp.sh] Creating virtual environment..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# Activate venv
# shellcheck disable=SC1091
. "$VENV_DIR/bin/activate"

# Install dependencies once
if [ ! -f "$MARKER_FILE" ]; then
  echo "[run_mcp.sh] Installing dependencies..."
  pip install -r requirements.txt
  touch "$MARKER_FILE"
  echo "[run_mcp.sh] Dependencies installed."
fi

echo "[run_mcp.sh] Starting MCP server..."
python src/server.py
