#!/usr/bin/env python3
"""
Integration test for FMP MCP Server.
This script tests that all endpoints are working correctly.
"""

import os
import sys
import json
import logging
import asyncio
from fastmcp.client import Client
from pprint import pprint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Test parameters
TEST_SYMBOLS = ["AAPL", "MSFT", "NVDA", "TSLA"]
MCP_URL = "http://localhost:8080/mcp"

async def test_endpoints():
    """Run tests on all FMP MCP endpoints."""
    try:
        # Connect to the MCP server
        client = await Client.connect(MCP_URL)
        logger.info(f"Connected to MCP server at {MCP_URL}")
        
        # Get all available tools
        tools = await client.list_tools()
        logger.info(f"Found {len(tools)} tools:")
        for tool in tools:
            logger.info(f"- {tool.name}")
        
        # Test 1: get_eps_surprise
        logger.info("\n--- Testing get_eps_surprise ---")
        symbol = TEST_SYMBOLS[0]
        try:
            eps_data = await client.invoke("get_eps_surprise", {"symbol": symbol})
            logger.info(f"Retrieved {len(eps_data)} EPS records for {symbol}")
            logger.info(f"First record: {json.dumps(eps_data[0], indent=2) if eps_data else 'No data'}")
            if eps_data:
                assert "eps" in eps_data[0], "Missing 'eps' field in response"
                assert "eps_estimated" in eps_data[0], "Missing 'eps_estimated' field in response"
        except Exception as e:
            logger.error(f"get_eps_surprise test failed: {str(e)}")
        
        # Test 2: get_rsi
        logger.info("\n--- Testing get_rsi ---")
        symbol = TEST_SYMBOLS[1]
        try:
            rsi_data = await client.invoke("get_rsi", {"symbol": symbol, "time_period": 14})
            logger.info(f"Retrieved RSI data for {symbol} with {len(rsi_data.get('values', [])) if rsi_data else 0} data points")
            if rsi_data and rsi_data.get('values'):
                assert len(rsi_data['values']) > 0, "No RSI values returned"
                assert "date" in rsi_data['values'][0], "Missing 'date' field in RSI value"
                assert "value" in rsi_data['values'][0], "Missing 'value' field in RSI value"
        except Exception as e:
            logger.error(f"get_rsi test failed: {str(e)}")
        
        # Test 3: get_sma
        logger.info("\n--- Testing get_sma ---")
        symbol = TEST_SYMBOLS[2]
        try:
            sma_data = await client.invoke("get_sma", {"symbol": symbol, "time_period": 20})
            logger.info(f"Retrieved SMA data for {symbol} with {len(sma_data.get('values', [])) if sma_data else 0} data points")
            if sma_data and sma_data.get('values'):
                assert len(sma_data['values']) > 0, "No SMA values returned"
        except Exception as e:
            logger.error(f"get_sma test failed: {str(e)}")
        
        # Test 4: get_price_targets
        logger.info("\n--- Testing get_price_targets ---")
        symbol = TEST_SYMBOLS[0]
        try:
            targets = await client.invoke("get_price_targets", {"symbol": symbol})
            logger.info(f"Retrieved price targets for {symbol}")
            logger.info(f"Consensus: {targets.get('target_consensus', 'N/A')}, High: {targets.get('target_high', 'N/A')}, Low: {targets.get('target_low', 'N/A')}")
            assert "target_consensus" in targets, "Missing 'target_consensus' field in response"
        except Exception as e:
            logger.error(f"get_price_targets test failed: {str(e)}")
        
        # Test 5: get_insider_trading
        logger.info("\n--- Testing get_insider_trading ---")
        symbol = TEST_SYMBOLS[3]
        try:
            insider_data = await client.invoke("get_insider_trading", {"symbol": symbol, "limit": 5})
            logger.info(f"Retrieved {len(insider_data) if insider_data else 0} insider transactions for {symbol}")
            if insider_data and len(insider_data) > 0:
                logger.info(f"First transaction: {insider_data[0].get('reporter_name', 'Unknown')} - {insider_data[0].get('transaction_type', 'Unknown')}")
                assert "transaction_type" in insider_data[0], "Missing 'transaction_type' field in response"
        except Exception as e:
            logger.error(f"get_insider_trading test failed: {str(e)}")
        
        # Test 6: get_earnings_calendar
        logger.info("\n--- Testing get_earnings_calendar ---")
        try:
            calendar = await client.invoke("get_earnings_calendar", {})
            logger.info(f"Retrieved {len(calendar) if calendar else 0} earnings calendar events")
            if calendar and len(calendar) > 0:
                logger.info(f"First event: {calendar[0].get('symbol', 'Unknown')} on {calendar[0].get('date', 'Unknown')}")
                assert "symbol" in calendar[0], "Missing 'symbol' field in response"
                assert "date" in calendar[0], "Missing 'date' field in response"
        except Exception as e:
            logger.error(f"get_earnings_calendar test failed: {str(e)}")
        
        logger.info("\n--- All tests completed ---")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(test_endpoints())
    sys.exit(exit_code)
