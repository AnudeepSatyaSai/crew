# agents/prediction.py

from utils.data_fetching import fetch_alpha_vantage
from sklearn.ensemble import RandomForestRegressor
from .base import BaseAgent

class PricePredictionAgent(BaseAgent):
    name = "prediction"

    async def analyze(self):
        data = await fetch_alpha_vantage(self.ticker)
        data["Return"] = data["close"].pct_change().dropna()
        data["Lag1"] = data["Return"].shift(1)
        X = data[["Lag1"]].dropna()
        y = data["Return"].dropna()
        model = RandomForestRegressor()
        model.fit(X.values, y.values)
        pred_ret = model.predict([[X["Lag1"].iloc[-1]]])[0]
        return {
            "predicted_price": float(data["close"].iloc[-1] * (1 + pred_ret)),
            "latest_price": float(data["close"].iloc[-1])
        }
