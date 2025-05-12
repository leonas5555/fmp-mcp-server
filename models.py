from typing import Dict, List, Optional, Union
from datetime import datetime, date
from pydantic import BaseModel, Field

# Input models
class SymbolInput(BaseModel):
    """Input for endpoints that require a symbol."""
    symbol: str = Field(..., description="The stock symbol to fetch data for")

class TechnicalIndicatorInput(BaseModel):
    """Input for technical indicator endpoints."""
    symbol: str = Field(..., description="The stock symbol to fetch data for")
    indicator: str = Field(..., description="Indicator type (e.g. 'rsi', 'sma')")
    time_period: int = Field(default=14, description="Time period for the indicator calculation")
    chart_type: str = Field(default="line", description="Chart type (line, bar, etc.)")
    from_date: Optional[str] = Field(default=None, description="Start date in YYYY-MM-DD format")
    to_date: Optional[str] = Field(default=None, description="End date in YYYY-MM-DD format")

class EarningsCalendarInput(BaseModel):
    """Input for earnings calendar endpoint."""
    from_date: Optional[str] = Field(default=None, description="Start date in YYYY-MM-DD format")
    to_date: Optional[str] = Field(default=None, description="End date in YYYY-MM-DD format")
    symbol: Optional[str] = Field(default=None, description="Filter by specific symbol")

class PriceTargetInput(BaseModel):
    """Input for price target consensus endpoint."""
    symbol: str = Field(..., description="The stock symbol to fetch price targets for")

class InsiderTradingInput(BaseModel):
    """Input for insider trading endpoint."""
    symbol: str = Field(..., description="The stock symbol to fetch insider trading data for")
    page: int = Field(default=0, description="Page number for pagination")
    limit: int = Field(default=100, description="Number of results per page")

# Output models
class EarningsReport(BaseModel):
    """Earnings report with surprise data."""
    symbol: str
    date: str
    eps: float
    eps_estimated: float
    time: Optional[str] = None
    revenue: Optional[float] = None
    revenue_estimated: Optional[float] = None
    updated_from_date: Optional[str] = None
    surprise: Optional[float] = None
    surprise_percentage: Optional[float] = None
    quarter: Optional[float] = None
    year: Optional[int] = None

class IndicatorValue(BaseModel):
    """Single technical indicator value."""
    date: str
    value: float

class IndicatorOutput(BaseModel):
    """Technical indicator output."""
    symbol: str
    indicator: str
    time_period: int
    values: List[IndicatorValue]

class AnalystRating(BaseModel):
    """Individual analyst rating."""
    analyst_name: Optional[str] = None
    date: str
    rating: str
    price_target: float

class AnalystConsensus(BaseModel):
    """Price target consensus data."""
    symbol: str
    target_consensus: float
    target_high: float
    target_low: float
    number_of_analysts: int
    last_analyst_consensus_date: str
    rating_consensus: Optional[str] = None
    ratings: Optional[List[AnalystRating]] = None

class InsiderActivity(BaseModel):
    """Insider trading activity."""
    symbol: str
    filing_date: str
    transaction_date: str
    reporter_name: str
    reporter_title: str
    transaction_type: str
    shares: int
    price: Optional[float] = None
    value: Optional[float] = None
    url: Optional[str] = None

class EarningsCalendarEvent(BaseModel):
    """Earnings calendar event."""
    symbol: str
    date: str
    eps: Optional[float] = None
    eps_estimated: Optional[float] = None
    time: Optional[str] = None
    revenue: Optional[float] = None
    revenue_estimated: Optional[float] = None
    quarter: Optional[int] = None
    year: Optional[int] = None
