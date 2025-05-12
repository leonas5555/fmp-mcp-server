#!/bin/bash
# Script to start the FMP MCP Server

# Check if .env file exists, if not create one from example
if [ ! -f .env ]; then
    echo "No .env file found. Creating from .env.example"
    cp .env.example .env
    echo "Please edit .env file with your FMP API key."
    exit 1
fi

# Check if requirements are installed
pip install -r requirements.txt

# Start the server
python fmp_mcp_server.py
