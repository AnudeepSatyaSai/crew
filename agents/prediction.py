# agents/prediction.py

from utils.data_fetching import fetch_alpha_vantage
from sklearn.ensemble import RandomForestRegressor
from .base import BaseAgent
import traceback
import numpy as np

class PricePredictionAgent(BaseAgent):
    name = "prediction"

    async def analyze(self):
        try:
            data = await fetch_alpha_vantage(self.ticker)
            if data is None:
                raise ValueError("No data returned from all sources.")
            data["Return"] = data["close"].pct_change().dropna()
            data["Lag1"] = data["Return"].shift(1)
            X = data[["Lag1"]].dropna()
            y = data["Return"].dropna()
            try:
                model = RandomForestRegressor()
                model.fit(X.values, y.values)
                pred_ret = model.predict([[X["Lag1"].iloc[-1]]])[0]
            except Exception:
                # Fallback: use mean return
                pred_ret = np.mean(y)
            return {
                "predicted_price": float(data["close"].iloc[-1] * (1 + pred_ret)),
                "latest_price": float(data["close"].iloc[-1])
            }
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
