# utils/preprocessing.py

import numpy as np

def safe_float(series):
    try:
        return float(series.iloc[-1]) if not series.empty and not np.isnan(series.iloc[-1]) else None
    except Exception:
        return None

def calculate_metrics(returns):
    try:
        return {
            "mean_return": returns.mean(),
            "volatility": returns.std(),
            "sharpe_ratio": returns.mean() / returns.std() * np.sqrt(252),
            "sortino_ratio": returns.mean() / returns[returns < 0].std() * np.sqrt(252),
            "max_drawdown": ((1 + returns).cumprod() / (1 + returns).cumprod().cummax() - 1).min()
        }
    except Exception:
        return {k: None for k in ["mean_return", "volatility", "sharpe_ratio", "sortino_ratio", "max_drawdown"]}
