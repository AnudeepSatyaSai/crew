# agents/technical.py

from utils.data_fetching import fetch_alpha_vantage
from utils.preprocessing import safe_float
from .base import BaseAgent

class TechnicalAgent(BaseAgent):
    name = "technical"

    async def analyze(self):
        data = await fetch_alpha_vantage(self.ticker)
        delta = data["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        rs = gain.rolling(14).mean() / loss.rolling(14).mean()
        rsi = 100 - (100 / (1 + rs))
        exp1 = data["close"].ewm(span=12).mean()
        exp2 = data["close"].ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        return {
            "rsi": safe_float(rsi),
            "macd": safe_float(macd),
            "macd_signal": safe_float(signal)
        }
