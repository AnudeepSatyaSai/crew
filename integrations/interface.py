from integrations.mt5 import MT5Integration
from integrations.ctrader import CTraderIntegration

class TradingInterface:
    def __init__(self, backend, **kwargs):
        if backend == 'mt5':
            self.engine = MT5Integration(**kwargs)
        elif backend == 'ctrader':
            self.engine = CTraderIntegration(**kwargs)
        else:
            raise ValueError('Unsupported backend')

    def connect(self):
        return self.engine.connect()

    def get_account_info(self):
        return self.engine.get_account_info()

    def get_historical_data(self, symbol, timeframe, start, end):
        return self.engine.get_historical_data(symbol, timeframe, start, end)

    def send_order(self, symbol, volume, order_type, price=None, sl=None, tp=None, **kwargs):
        return self.engine.send_order(symbol, volume, order_type, price, sl, tp, **kwargs) 