# agents/high_frequency.py

from utils.data_fetching import fetch_alpha_vantage
from .base import BaseAgent
import numpy as np
import traceback
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

class HighFrequencyAgent(BaseAgent):
    name = "high_frequency"

    async def analyze(self):
        try:
            # For demo, use daily data as placeholder; in production, fetch tick/intraday data
            data = await fetch_alpha_vantage(self.ticker)
            if data is None:
                raise ValueError("No data returned from all sources.")
            # Calculate ultra-short-term technicals (simulate HFT with daily)
            data['sma_2'] = data['close'].rolling(2).mean()
            data['sma_5'] = data['close'].rolling(5).mean()
            data['vol_2'] = data['close'].pct_change().rolling(2).std()
            data['vol_5'] = data['close'].pct_change().rolling(5).std()
            # Simple HFT signal: SMA crossover
            signal = None
            if data['sma_2'].iloc[-1] > data['sma_5'].iloc[-1]:
                signal = 'hft_long'
            elif data['sma_2'].iloc[-1] < data['sma_5'].iloc[-1]:
                signal = 'hft_short'
            # ML-based prediction (using ultra-short-term returns)
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
                'sma_2': float(data['sma_2'].iloc[-1]),
                'sma_5': float(data['sma_5'].iloc[-1]),
                'vol_2': float(data['vol_2'].iloc[-1]),
                'vol_5': float(data['vol_5'].iloc[-1]),
                'hft_signal': signal,
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