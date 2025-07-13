# agents/volatility.py

from utils.data_fetching import fetch_alpha_vantage
from .base import BaseAgent

class VolatilityAgent(BaseAgent):
    name = "volatility"

    async def analyze(self):
        data = await fetch_alpha_vantage(self.ticker)
        returns = data["close"].pct_change().dropna()
        return {
            "volatility_30d": float(returns[-30:].std()),
            "volatility_90d": float(returns[-90:].std())
        }
