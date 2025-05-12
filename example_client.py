#!/usr/bin/env python3
"""
Example client for FMP MCP Server
"""

import os
import asyncio
from fastmcp.client import Client
from pprint import pprint

async def main():
    """
    Example usage of FMP MCP client.
    """
    # Connect to the server
    client = await Client.connect("http://localhost:8080/mcp")
    
    # Get all available tools
    tools = await client.list_tools()
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 1: Get EPS surprise for AAPL
    print("Example 1: EPS surprise for AAPL")
    eps_result = await client.invoke("get_eps_surprise", {"symbol": "AAPL"})
    pprint(eps_result)
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 2: Get RSI for NVDA
    print("Example 2: RSI for NVDA")
    rsi_result = await client.invoke("get_rsi", {
        "symbol": "NVDA",
        "time_period": 14
    })
    pprint(rsi_result)
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 3: Get price targets for MSFT
    print("Example 3: Price targets for MSFT")
    targets_result = await client.invoke("get_price_targets", {"symbol": "MSFT"})
    pprint(targets_result)
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 4: Get insider trading for TSLA
    print("Example 4: Insider trading for TSLA")
    insider_result = await client.invoke("get_insider_trading", {"symbol": "TSLA", "limit": 5})
    pprint(insider_result)
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 5: Get earnings calendar
    print("Example 5: Earnings calendar")
    calendar_result = await client.invoke("get_earnings_calendar", {})
    pprint(calendar_result[:5])  # Only show first 5 results

if __name__ == "__main__":
    asyncio.run(main())
