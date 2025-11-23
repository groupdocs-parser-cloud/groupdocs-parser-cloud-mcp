#!/usr/bin/env bash
set -a  # automatically export all variables
source .env
set +a

echo "Environment variables loaded:"
echo "CLIENT_ID=$CLIENT_ID"
echo "CLIENT_SECRET=$CLIENT_SECRET"
echo "MCP_PORT=$MCP_PORT"

python src/server.py