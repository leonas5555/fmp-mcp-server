# FMP MCP Server

A Model Context Protocol (MCP) server for Financial Modeling Prep (FMP) API data, designed for integration with LLM-powered trading strategies.

## Overview

This server wraps key FMP API endpoints into a standardized MCP format, providing structured financial data for:

- Earnings surprise data (`get_eps_surprise`)
- Technical indicators (`get_rsi`, `get_sma`)
- Analyst price targets (`get_price_targets`)
- Insider trading activity (`get_insider_trading`)
- Earnings calendar (`get_earnings_calendar`)

These endpoints were specifically selected to support PEAD (Post-Earnings Announcement Drift) strategy, sentiment-pullback strategies, and risk management through analyst consensus and insider trading activity monitoring.

## Prerequisites

1. Python 3.11 or newer
2. FMP API key (get one at [Financial Modeling Prep](https://financialmodelingprep.com/))

## Installation

### Local Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your FMP API key.

4. Start the server:
   ```bash
   ./start.sh
   # Or directly:
   python fmp_mcp_server.py
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t fmp-mcp-server .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 --env-file .env fmp-mcp-server
   ```

## Usage

Once the server is running, you can access:

- API documentation: `http://localhost:8080/docs`
- OpenAPI spec: `http://localhost:8080/openapi.json`
- MCP endpoint: `http://localhost:8080/mcp`

### Example MCP Tool Calls

Get earnings surprise data for AAPL:
```python
from langchain.tools import MCP

tools = MCP.from_url("http://localhost:8080/mcp").tools()
eps_data = tools.get_eps_surprise(symbol="AAPL")
print(eps_data)
```

Get RSI data for NVDA:
```python
rsi_data = tools.get_rsi(symbol="NVDA", time_period=14)
print(rsi_data)
```

### Integration with Trading Fleet

This server is designed to work with the agentic-trading-fleet architecture. The tools provided here complement the Insight Sentry API by providing structured financial data that is particularly useful for PEAD strategy, risk management, and backtesting.

## Endpoints

| Tool Name             | Purpose                                        | Strategy Use Case                                |
|-----------------------|------------------------------------------------|--------------------------------------------------|
| `get_eps_surprise`    | Structured EPS data (actual/est/surprise)      | PEAD strategy, earnings drift                    |
| `get_rsi`             | RSI technical indicator values                 | Sentiment-Pullback, technical backtest           |
| `get_sma`             | SMA technical indicator values                 | Technical analysis, moving average strategies    |
| `get_price_targets`   | Analyst consensus and price targets            | Long-horizon risk filter                         |
| `get_insider_trading` | Insider transactions (buys/sells)              | News-halt heuristic for large insider sales      |
| `get_earnings_calendar`| Upcoming earnings events                      | PEAD strategy, volatility forecasting            |

## License

[MIT](LICENSE)