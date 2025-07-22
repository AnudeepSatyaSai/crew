import pandas as pd

class BacktestEngine:
    def __init__(self):
        self.data = None

    def load_csv(self, filepath):
        """
        Loads historical data from a CSV file.
        """
        self.data = pd.read_csv(filepath)
        return self.data

    def run_backtest(self, signal_func, *args, **kwargs):
        """
        Runs a backtest using the provided signal function.
        signal_func: function that generates trade signals from data
        Returns backtest results (PnL, trades, etc.)
        """
        # TODO: Implement backtest logic
        pass

    def run_forward_test(self, signal_func, *args, **kwargs):
        """
        Runs a forward test (paper trading) using the provided signal function.
        Returns forward test results.
        """
        # TODO: Implement forward test logic
        pass 