#!/usr/bin/env bash
set -e

ENV_FILE=".env"
VENV_DIR=".venv"
MARKER_FILE="$VENV_DIR/.deps_installed"

# Load environment variables if .env exists (optional)
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
  echo "[init_mcp.sh] Environment variables loaded from $ENV_FILE."
else
  echo "[init_mcp.sh] Warning: $ENV_FILE not found. Continuing without env variables..."
fi

# Choose python
PYTHON_CMD="python3"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
  else
    echo "[init_mcp.sh] Error: python3 or python not found in PATH."
    exit 1
  fi
fi

# Remove existing venv (full re-init)
if [ -d "$VENV_DIR" ]; then
  echo "[init_mcp.sh] Removing existing virtual environment at $VENV_DIR..."
  rm -rf "$VENV_DIR"
fi

echo "[init_mcp.sh] Creating virtual environment in $VENV_DIR..."
"$PYTHON_CMD" -m venv "$VENV_DIR"

# Activate new venv
# shellcheck disable=SC1091
. "$VENV_DIR/bin/activate"

if [ ! -f "requirements.txt" ]; then
  echo "[init_mcp.sh] Error: requirements.txt not found."
  exit 1
fi

echo "[init_mcp.sh] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Mark deps as installed so run_mcp.* can skip reinstall
touch "$MARKER_FILE"
echo "[init_mcp.sh] Initialization complete. You can now run ./run_mcp.sh"
