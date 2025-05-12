#!/bin/bash
# Quick smoke test for FMP MCP server

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "Running FMP MCP server health check..."
python3 health_check.py

if [ $? -ne 0 ]; then
    echo "❌ Health check failed. Server may not be running or has issues."
    exit 1
fi

echo "Running quick endpoint test..."
python3 test_server.py

if [ $? -ne 0 ]; then
    echo "❌ Endpoint tests failed. Check server logs for details."
    exit 1
fi

echo "✅ All tests passed. FMP MCP server is working correctly."
exit 0
