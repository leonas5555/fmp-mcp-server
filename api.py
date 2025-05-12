from fmpsdk import fmp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging

from config import config
from models import (
    EarningsReport, IndicatorOutput, IndicatorValue, AnalystConsensus,
    InsiderActivity, EarningsCalendarEvent, AnalystRating
)

logger = logging.getLogger(__name__)

def get_eps_surprise(symbol: str) -> List[EarningsReport]:
    """Get earnings surprise data for a symbol."""
    try:
        raw_data = fmp.earnings_surprises(config.FMP_API_KEY, symbol)
        
        # Convert data to our model format
        result = []
        for item in raw_data:
            # Convert to camel case keys to match our model
            report = EarningsReport(
                symbol=item.get('symbol'),
                date=item.get('date'),
                eps=item.get('actualEarningResult', 0.0),
                eps_estimated=item.get('estimatedEarning', 0.0),
                time=item.get('time'),
                revenue=item.get('revenue'),
                revenue_estimated=item.get('revenueEstimated'),
                surprise=item.get('surprise'),
                surprise_percentage=item.get('surprisePercentage'),
                quarter=item.get('quarter'),
                year=item.get('year')
            )
            result.append(report)
        
        return result
    except Exception as e:
        logger.error(f"Error getting EPS surprise for {symbol}: {str(e)}")
        raise

def get_technical_indicator(symbol: str, indicator: str, time_period: int = 14, 
                            from_date: Optional[str] = None, to_date: Optional[str] = None) -> IndicatorOutput:
    """Get technical indicator data for a symbol."""
    try:
        # Handle date parameters
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        if not from_date:
            # Default to 100 days of data if not specified
            from_date = (datetime.strptime(to_date, "%Y-%m-%d") - timedelta(days=100)).strftime("%Y-%m-%d")
        
        raw_data = fmp.technical_indicators(
            config.FMP_API_KEY, 
            symbol, 
            indicator,
            time_period
        )
        
        # Convert to our model format
        values = []
        for item in raw_data:
            if indicator.lower() in item:
                value = item[indicator.lower()]
            else:
                # Some indicators use different key names
                fallback_keys = ['value', indicator, 'indicator_value']
                value = None
                for key in fallback_keys:
                    if key in item:
                        value = item[key]
                        break
                
                if value is None:
                    # If we can't find the value, skip this item
                    continue
                    
            values.append(IndicatorValue(
                date=item.get('date', ''),
                value=float(value) if value is not None else 0.0
            ))
        
        # Filter by date range
        filtered_values = [v for v in values if from_date <= v.date <= to_date]
        
        return IndicatorOutput(
            symbol=symbol,
            indicator=indicator,
            time_period=time_period,
            values=filtered_values
        )
    except Exception as e:
        logger.error(f"Error getting technical indicator {indicator} for {symbol}: {str(e)}")
        raise

def get_price_targets(symbol: str) -> AnalystConsensus:
    """Get price target consensus for a symbol."""
    try:
        raw_data = fmp.price_target_consensus(config.FMP_API_KEY, symbol)
        
        # Handle case where API returns multiple items
        if isinstance(raw_data, list) and len(raw_data) > 0:
            raw_data = raw_data[0]
        
        # Convert to our model format
        consensus = AnalystConsensus(
            symbol=symbol,
            target_consensus=raw_data.get('targetConsensus', 0.0),
            target_high=raw_data.get('targetHigh', 0.0),
            target_low=raw_data.get('targetLow', 0.0),
            number_of_analysts=raw_data.get('numberOfAnalysts', 0),
            last_analyst_consensus_date=raw_data.get('lastAnalystConsensusDate', ''),
            rating_consensus=raw_data.get('ratingConsensus', '')
        )
        
        # Try to get detailed analyst ratings if available
        try:
            analyst_data = fmp.price_target(config.FMP_API_KEY, symbol)
            ratings = []
            
            for item in analyst_data:
                ratings.append(AnalystRating(
                    analyst_name=item.get('analystName', 'Unknown'),
                    date=item.get('date', ''),
                    rating=item.get('rating', ''),
                    price_target=item.get('priceTarget', 0.0)
                ))
            
            consensus.ratings = ratings
        except Exception:
            # Individual analyst ratings are optional
            pass
            
        return consensus
    except Exception as e:
        logger.error(f"Error getting price targets for {symbol}: {str(e)}")
        raise

def get_insider_trading(symbol: str, page: int = 0, limit: int = 100) -> List[InsiderActivity]:
    """Get insider trading data for a symbol."""
    try:
        raw_data = fmp.insider_trading(config.FMP_API_KEY, symbol, page=page, limit=limit)
        
        # Convert to our model format
        result = []
        for item in raw_data:
            activity = InsiderActivity(
                symbol=item.get('symbol', symbol),
                filing_date=item.get('filingDate', ''),
                transaction_date=item.get('transactionDate', ''),
                reporter_name=item.get('reporterName', ''),
                reporter_title=item.get('reporterTitle', ''),
                transaction_type=item.get('transactionType', ''),
                shares=item.get('acquistionOrDisposition', 0),
                price=item.get('price'),
                value=item.get('value'),
                url=item.get('link', '')
            )
            result.append(activity)
        
        return result
    except Exception as e:
        logger.error(f"Error getting insider trading for {symbol}: {str(e)}")
        raise

def get_earnings_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None, 
                          symbol: Optional[str] = None) -> List[EarningsCalendarEvent]:
    """Get earnings calendar events."""
    try:
        # Handle date parameters
        if not to_date:
            to_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        if not from_date:
            from_date = datetime.now().strftime("%Y-%m-%d")
        
        # If symbol is provided, use the symbol-specific endpoint
        if symbol:
            raw_data = fmp.earnings_calendar_confirmed(config.FMP_API_KEY, symbol)
        else:
            raw_data = fmp.earnings_calendar(config.FMP_API_KEY, from_date=from_date, to_date=to_date)
        
        # Convert to our model format
        result = []
        for item in raw_data:
            # Skip if outside date range
            event_date = item.get('date', '')
            if event_date < from_date or event_date > to_date:
                continue
                
            event = EarningsCalendarEvent(
                symbol=item.get('symbol', ''),
                date=event_date,
                eps=item.get('eps'),
                eps_estimated=item.get('epsEstimated'),
                time=item.get('time'),
                revenue=item.get('revenue'),
                revenue_estimated=item.get('revenueEstimated'),
                quarter=item.get('quarter'),
                year=item.get('year')
            )
            result.append(event)
        
        return result
    except Exception as e:
        logger.error(f"Error getting earnings calendar: {str(e)}")
        raise
