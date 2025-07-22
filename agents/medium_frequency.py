# agents/medium_frequency.py

from utils.data_fetching import fetch_alpha_vantage
from .base import BaseAgent
import numpy as np
import traceback
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

class MediumFrequencyAgent(BaseAgent):
    name = "medium_frequency"

    async def analyze(self):
        try:
            # For demo, use daily data as placeholder; in production, fetch intraday data
            data = await fetch_alpha_vantage(self.ticker)
            if data is None:
                raise ValueError("No data returned from all sources.")
            # Calculate short-term technicals (simulate intraday with daily)
            data['sma_5'] = data['close'].rolling(5).mean()
            data['sma_15'] = data['close'].rolling(15).mean()
            data['vol_5'] = data['close'].pct_change().rolling(5).std()
            data['vol_15'] = data['close'].pct_change().rolling(15).std()
            # Simple scalping/intraday signal: SMA crossover
            signal = None
            if data['sma_5'].iloc[-1] > data['sma_15'].iloc[-1]:
                signal = 'scalp_long'
            elif data['sma_5'].iloc[-1] < data['sma_15'].iloc[-1]:
                signal = 'scalp_short'
            # ML-based prediction (using short-term returns)
            data['Return'] = data['close'].pct_change().dropna()
            data['Lag1'] = data['Return'].shift(1)
            X = data[['Lag1']].dropna()
            y = data['Return'].dropna()
            try:
                model_rf = RandomForestRegressor()
                model_rf.fit(X.values, y.values)
                pred_rf = model_rf.predict([[X['Lag1'].values[-1]]])[0]
            except Exception:
                pred_rf = np.mean(y)
            try:
                model_xgb = XGBRegressor()
                model_xgb.fit(X.values, y.values)
                pred_xgb = model_xgb.predict([[X['Lag1'].values[-1]]])[0]
            except Exception:
                pred_xgb = np.mean(y)
            # Stacking/ensemble: average predictions
            ensemble_pred = (pred_rf + pred_xgb) / 2
            # Placeholder for order book features (not available in demo)
            order_book_feature = None
            return {
                'sma_5': float(data['sma_5'].iloc[-1]),
                'sma_15': float(data['sma_15'].iloc[-1]),
                'vol_5': float(data['vol_5'].iloc[-1]),
                'vol_15': float(data['vol_15'].iloc[-1]),
                'scalping_signal': signal,
                'ml_predicted_return': float(pred_rf),
                'xgb_predicted_return': float(pred_xgb),
                'ensemble_predicted_return': float(ensemble_pred),
                'order_book_feature': order_book_feature
            }
        except Exception as e:
            return {
                'error': str(e),
                'trace': traceback.format_exc()
            } 