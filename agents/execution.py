# agents/execution.py

from .base import BaseAgent
import backtrader as bt
import pandas as pd
from utils.data_fetching import fetch_alpha_vantage
import traceback

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma_short = bt.ind.SMA(period=10)
        sma_long = bt.ind.SMA(period=30)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma_short, sma_long))

class CustomPandasData(bt.feeds.PandasData):
    params = (
        ('datetime', 'datetime'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', 'openinterest'),
    )

class ExecutionAgent(BaseAgent):
    name = "execution"

    async def analyze(self):
        try:
        data = await fetch_alpha_vantage(self.ticker)
            df = data.copy()
            # Ensure index is named 'datetime' and reset
            if not df.index.name:
                df.index.name = 'datetime'
            df = df.reset_index()
            if 'datetime' not in df.columns:
                df.rename(columns={str(df.columns[0]): 'datetime'}, inplace=True)
            if 'close' not in df.columns:
                raise ValueError("'close' column missing in data for execution agent.")
            # Prepare columns for Backtrader
            df['open'] = df['high'] = df['low'] = df['close']
            df['volume'] = 1000
            df['openinterest'] = 0
            df = df.sort_values('datetime')

        cerebro = bt.Cerebro()
            datafeed = CustomPandasData(dataname=df)
        cerebro.adddata(datafeed)
        cerebro.addstrategy(SmaCross)
        cerebro.broker.set_cash(100000)
        cerebro.run()
        final_value = cerebro.broker.getvalue()
        return {
                "final_portfolio_value": final_value,
                "data_source": 'yfinance or Alpha Vantage'
            }
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
        }
