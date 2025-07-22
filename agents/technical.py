# agents/technical.py

from utils.data_fetching import fetch_alpha_vantage
from utils.preprocessing import safe_float
from .base import BaseAgent
import ta.momentum
import ta.trend
import ta.volatility
import traceback

class TechnicalAgent(BaseAgent):
    name = "technical"

    async def analyze(self):
        try:
        data = await fetch_alpha_vantage(self.ticker)
            if data is None:
                raise ValueError("No data returned from all sources.")
            source = getattr(data, 'source', 'unknown') if hasattr(data, 'source') else 'unknown'
            close = data["close"]
            rsi = ta.momentum.RSIIndicator(close).rsi()
            macd = ta.trend.MACD(close)
            bb = ta.volatility.BollingerBands(close)
        return {
            "rsi": safe_float(rsi),
                "macd": safe_float(macd.macd()),
                "macd_signal": safe_float(macd.macd_signal()),
                "bb_high": safe_float(bb.bollinger_hband()),
                "bb_low": safe_float(bb.bollinger_lband()),
                "data_source": source
            }
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
        }
