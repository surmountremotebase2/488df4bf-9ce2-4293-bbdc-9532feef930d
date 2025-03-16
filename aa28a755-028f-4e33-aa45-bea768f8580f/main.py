from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"] # The selected asset for trading.

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day" # Utilizing daily data for analysis.

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            rsi_values = RSI(ticker, data["ohlcv"], 14) # 14-day RSI
            macd_values = MACD(ticker, data["ohlcv"], fast=12, slow=26) # Standard MACD(12,26,9)

            if not rsi_values or not macd_values['MACD'] or not macd_values['signal']:
                log(f"Insufficient data for {ticker}")
                allocation_dict[ticker] = 0
                continue

            latest_rsi = rsi_values[-1]
            latest_macd = macd_values['MACD'][-1]
            latest_signal = macd_values['signal'][-1]

            if latest_rsi < 30 and latest_macd > latest_signal:
                allocation_dict[ticker] = 1.0 # Full allocation to buy signal
            elif latest_rsi > 70 and latest_macd < latest_signal:
                allocation_dict[ticker] = 0 # Sell or short signal, no allocation
            else:
                allocation_dict[ticker] = 0.5 # Hold or partial allocation for no clear signal

        return TargetAllocation(allocation_dict)