#!/bin/bash
# Build and start the FMP MCP server
# This script can be called from the main build-all-mcp-servers.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if .env file exists, if not create one
if [ ! -f .env ]; then
    echo "No .env file found. Creating from .env.example"
    cp .env.example .env
    echo "Please edit .env file with your FMP API key."
    exit 1
fi

# Check if running in Docker mode
if [ "$1" == "docker" ]; then
    echo "Building FMP MCP server Docker image..."
    docker build -t fmp-mcp-server .
    
    echo "Starting FMP MCP server in Docker..."
    docker run -d --name fmp-mcp-server \
        --restart unless-stopped \
        -p 8080:8080 \
        --env-file .env \
        fmp-mcp-server
    
    echo "FMP MCP server started in Docker on port 8080"
else
    # Local mode
    echo "Setting up virtual environment for FMP MCP server..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Starting FMP MCP server locally..."
    python3 fmp_mcp_server.py
fi
