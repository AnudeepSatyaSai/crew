import MetaTrader5 as mt5
from datetime import datetime

class MT5Integration:
    def __init__(self, login=None, password=None, server=None, path=None):
        self.login = login
        self.password = password
        self.server = server
        self.path = path
        self.connected = False

    def connect(self):
        if self.path:
            mt5.initialize(self.path)
        else:
            mt5.initialize()
        if self.login and self.password and self.server:
            authorized = mt5.login(self.login, self.password, self.server)
            self.connected = authorized
            return authorized
        self.connected = mt5.initialize()
        return self.connected

    def shutdown(self):
        mt5.shutdown()
        self.connected = False

    def get_account_info(self):
        return mt5.account_info()._asdict() if self.connected else None

    def get_historical_data(self, symbol, timeframe, start, end):
        '''
        symbol: str, e.g. 'EURUSD'
        timeframe: mt5.TIMEFRAME_M1, mt5.TIMEFRAME_H1, etc.
        start, end: datetime objects
        '''
        rates = mt5.copy_rates_range(symbol, timeframe, start, end)
        return rates

    def send_order(self, symbol, lot, order_type, price=None, sl=None, tp=None, deviation=20, magic=0, comment="AI Trade"):
        '''
        order_type: mt5.ORDER_TYPE_BUY or mt5.ORDER_TYPE_SELL
        '''
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info.visible:
            mt5.symbol_select(symbol, True)
        point = symbol_info.point
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price if price else mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result 