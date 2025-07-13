# agents/execution.py

from .base import BaseAgent
import backtrader as bt
import pandas as pd
from utils.data_fetching import fetch_alpha_vantage

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma_short = bt.ind.SMA(period=10)
        sma_long = bt.ind.SMA(period=30)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma_short, sma_long))

class ExecutionAgent(BaseAgent):
    name = "execution"

    async def analyze(self):
        data = await fetch_alpha_vantage(self.ticker)
        df = data.reset_index()[["index", "close"]]
        df.columns = ["datetime", "close"]
        df["open"] = df["high"] = df["low"] = df["close"]
        df["volume"] = 1000
        df["openinterest"] = 0
        df = df.sort_values("datetime")

        cerebro = bt.Cerebro()
        datafeed = bt.feeds.PandasData(dataname=df, datetime="datetime")
        cerebro.adddata(datafeed)
        cerebro.addstrategy(SmaCross)
        cerebro.broker.set_cash(100000)
        cerebro.run()
        final_value = cerebro.broker.getvalue()
        return {
            "final_portfolio_value": final_value
        }
