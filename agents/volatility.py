# agents/volatility.py

from utils.data_fetching import fetch_alpha_vantage
from .base import BaseAgent
import numpy as np
import traceback

class VolatilityAgent(BaseAgent):
    name = "volatility"

    async def analyze(self):
        try:
            data = await fetch_alpha_vantage(self.ticker)
            if data is None:
                raise ValueError("No data returned from all sources.")
            source = getattr(data, 'source', 'unknown') if hasattr(data, 'source') else 'unknown'
            returns = data["close"].pct_change().dropna()
            vol_30d = float(returns[-30:].std())
            vol_90d = float(returns[-90:].std())
            annualized_vol = float(returns.std() * np.sqrt(252))
            return {
                "volatility_30d": vol_30d,
                "volatility_90d": vol_90d,
                "annualized_volatility": annualized_vol,
                "data_source": source
            }
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
