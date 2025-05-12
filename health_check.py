#!/usr/bin/env python3
"""
Health check script for the FMP MCP server.
This script checks if the server is running and responding to requests.
"""

import os
import sys
import logging
import argparse
import requests
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def check_server_health(host="localhost", port=8080):
    """Check if the MCP server is healthy."""
    url = f"http://{host}:{port}/health"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "healthy":
                logger.info("✅ Server is healthy")
                
                # Check if API key is configured
                if data.get("api_key_configured"):
                    logger.info("✅ API key is configured")
                else:
                    logger.warning("⚠️  API key is NOT configured")
                    return False
                
                return True
            else:
                logger.error(f"❌ Server status is not healthy: {data.get('status', 'unknown')}")
                return False
        else:
            logger.error(f"❌ Server responded with code {response.status_code}")
            return False
    except RequestException as e:
        logger.error(f"❌ Failed to connect to server: {str(e)}")
        return False

def check_mcp_endpoint(host="localhost", port=8080):
    """Check if the MCP endpoint is responding."""
    url = f"http://{host}:{port}/mcp"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.info("✅ MCP endpoint is responding")
            return True
        else:
            logger.error(f"❌ MCP endpoint responded with code {response.status_code}")
            return False
    except RequestException as e:
        logger.error(f"❌ Failed to connect to MCP endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health check for FMP MCP server")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    
    args = parser.parse_args()
    
    logger.info(f"Checking FMP MCP server health at {args.host}:{args.port}")
    
    server_healthy = check_server_health(args.host, args.port)
    mcp_healthy = check_mcp_endpoint(args.host, args.port)
    
    if server_healthy and mcp_healthy:
        logger.info("✅ All checks passed. Server is healthy.")
        sys.exit(0)
    else:
        logger.error("❌ One or more checks failed. Server may not be functioning correctly.")
        sys.exit(1)
