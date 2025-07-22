import traceback
from utils.data_fetching import fetch_alpha_vantage
from utils.preprocessing import calculate_metrics, safe_float
from .base import BaseAgent
import numpy as np

class QuantitativeAgent(BaseAgent):
    name = "quantitative"

    async def analyze(self):
        try:
            data = await fetch_alpha_vantage(self.ticker)
            source = getattr(data, 'source', 'unknown') if hasattr(data, 'source') else 'unknown'
            data["Return"] = data["close"].pct_change().dropna()
            base = calculate_metrics(data["Return"])
            base.update({
                "sma_20": safe_float(data["close"].rolling(20).mean()),
                "ema_50": safe_float(data["close"].ewm(span=50).mean()),
                "latest_price": safe_float(data["close"]),
                "volatility": float(np.std(data["Return"])) if not data["Return"].empty else None,
                "sharpe_ratio": float(np.mean(data["Return"]) / np.std(data["Return"])) if np.std(data["Return"]) != 0 else None,
                "VaR_95": float(np.percentile(data["Return"], 5)) if not data["Return"].empty else None,
                "data_source": source
            })
            return base
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
