#!/usr/bin/env python3
"""
FMP MCP Server

A MCP server for Financial Modeling Prep API using fastmcp.
"""

import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Depends
from fastmcp import Server, Tool, Annotated
from typing import List, Optional
import json

from config import config
from models import (
    SymbolInput, TechnicalIndicatorInput, EarningsCalendarInput,
    PriceTargetInput, InsiderTradingInput, EarningsReport, IndicatorOutput,
    AnalystConsensus, InsiderActivity, EarningsCalendarEvent
)
import api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FMP MCP Server",
    description="""Model Context Protocol (MCP) server for Financial Modeling Prep data.
    Provides structured financial data for trading strategies.""",
    version="1.0.0",
)

server = Server(app=app, path="/mcp")

@server.tool("get_eps_surprise")
async def get_eps_surprise(symbol: Annotated[str, "The stock symbol to fetch earnings surprise data for"]) -> List[EarningsReport]:
    """
    Get earnings surprise data for a symbol.
    
    This endpoint returns structured EPS data (actual/estimated/surprise percentage)
    for the specified symbol. Critical for PEAD strategy implementation.
    """
    try:
        return api.get_eps_surprise(symbol)
    except Exception as e:
        logger.error(f"Error in get_eps_surprise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching EPS surprise data: {str(e)}")

@server.tool("get_rsi")
async def get_rsi(
    symbol: Annotated[str, "The stock symbol to fetch RSI data for"],
    time_period: Annotated[int, "Time period for RSI calculation"] = 14,
    from_date: Annotated[Optional[str], "Start date in YYYY-MM-DD format"] = None,
    to_date: Annotated[Optional[str], "End date in YYYY-MM-DD format"] = None
) -> IndicatorOutput:
    """
    Get Relative Strength Index (RSI) data for a symbol.
    
    Returns RSI values over the specified time period. Useful for
    technical analysis and backtesting.
    """
    try:
        return api.get_technical_indicator(symbol, "rsi", time_period, from_date, to_date)
    except Exception as e:
        logger.error(f"Error in get_rsi: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching RSI data: {str(e)}")

@server.tool("get_sma")
async def get_sma(
    symbol: Annotated[str, "The stock symbol to fetch SMA data for"],
    time_period: Annotated[int, "Time period for SMA calculation"] = 20,
    from_date: Annotated[Optional[str], "Start date in YYYY-MM-DD format"] = None,
    to_date: Annotated[Optional[str], "End date in YYYY-MM-DD format"] = None
) -> IndicatorOutput:
    """
    Get Simple Moving Average (SMA) data for a symbol.
    
    Returns SMA values over the specified time period. Useful for
    technical analysis and backtesting.
    """
    try:
        return api.get_technical_indicator(symbol, "sma", time_period, from_date, to_date)
    except Exception as e:
        logger.error(f"Error in get_sma: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching SMA data: {str(e)}")

@server.tool("get_price_targets")
async def get_price_targets(symbol: Annotated[str, "The stock symbol to fetch price targets for"]) -> AnalystConsensus:
    """
    Get analyst price target consensus for a symbol.
    
    Returns analyst consensus price targets, high/low targets, and number of analysts.
    Important for long-term risk filters and analyst extreme detection.
    """
    try:
        return api.get_price_targets(symbol)
    except Exception as e:
        logger.error(f"Error in get_price_targets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching price target data: {str(e)}")

@server.tool("get_insider_trading")
async def get_insider_trading(
    symbol: Annotated[str, "The stock symbol to fetch insider trading data for"],
    page: Annotated[int, "Page number for pagination"] = 0,
    limit: Annotated[int, "Number of results per page"] = 100
) -> List[InsiderActivity]:
    """
    Get insider trading data for a symbol.
    
    Returns recent insider trading activity for a symbol, including transaction
    type, shares, price, and value. Useful for news-halt heuristics on large insider sales.
    """
    try:
        return api.get_insider_trading(symbol, page, limit)
    except Exception as e:
        logger.error(f"Error in get_insider_trading: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching insider trading data: {str(e)}")

@server.tool("get_earnings_calendar")
async def get_earnings_calendar(
    from_date: Annotated[Optional[str], "Start date in YYYY-MM-DD format"] = None,
    to_date: Annotated[Optional[str], "End date in YYYY-MM-DD format"] = None,
    symbol: Annotated[Optional[str], "Filter by specific symbol"] = None
) -> List[EarningsCalendarEvent]:
    """
    Get earnings calendar events.
    
    Returns upcoming earnings events in the specified date range. Optionally filter
    by symbol. Useful for PEAD strategy and volatility forecasting.
    """
    try:
        return api.get_earnings_calendar(from_date, to_date, symbol)
    except Exception as e:
        logger.error(f"Error in get_earnings_calendar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching earnings calendar data: {str(e)}")

@app.get("/")
async def root():
    return {
        "name": "FMP MCP Server",
        "description": "Model Context Protocol (MCP) server for Financial Modeling Prep data",
        "version": "1.0.0",
        "endpoints": {
            "mcp": "/mcp",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "api_key_configured": bool(config.FMP_API_KEY)}

if __name__ == "__main__":
    logger.info(f"Starting FMP MCP Server on {config.HOST}:{config.PORT}")
    uvicorn.run("fmp_mcp_server:app", host=config.HOST, port=config.PORT, reload=True)
