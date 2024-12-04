import pandas as pd
from datetime import timedelta
from collections import defaultdict


class DataAggregator:
    def __init__(self):
        """
        Initialize the data aggregator for 30-second bars.
        """
        self.tick_data = defaultdict(list)  # {symbol: [tick1, tick2, ...]}
        self.aggregated_bars = defaultdict(list)  # {symbol: [bar1, bar2, ...]}
        self.last_interval = defaultdict(lambda: None)  # {symbol: last_interval}

    def add_tick(self, tick):
        """
        Add a tick to the aggregator and update 30-second bars.
        :param tick: Dictionary with tick data. Example:
                     {"timestamp": ..., "symbol": ..., "price": ..., "volume": ...}
        """
        symbol = tick.get("symbol")
        if not symbol:
            print("Invalid tick: Missing symbol.")
            return

        # Convert timestamp to pandas datetime if not already
        tick["timestamp"] = pd.to_datetime(tick["timestamp"])

        # Determine the 30-second interval for the tick
        interval_start = tick["timestamp"].floor("30s")

        # Check if the interval has changed
        if self.last_interval[symbol] is not None and interval_start > self.last_interval[symbol]:
            # Finalize the bar for the previous interval
            self._create_bar(symbol)

        # Add the tick to the symbol's tick data
        self.tick_data[symbol].append(tick)
        self.last_interval[symbol] = interval_start

    def _create_bar(self, symbol):
        """
        Create a single 30-second bar from the accumulated ticks.
        :param symbol: The symbol for the bar.
        """
        ticks = self.tick_data[symbol]
        if not ticks:
            return

        # Aggregate the tick data into OHLCV format
        ohlc = {
            "timestamp": ticks[0]["timestamp"].floor("30s"),
            "symbol": symbol,
            "open": ticks[0]["price"],
            "high": max(tick["price"] for tick in ticks),
            "low": min(tick["price"] for tick in ticks),
            "close": ticks[-1]["price"],
            "volume": sum(tick["volume"] for tick in ticks),
        }
        self.aggregated_bars[symbol].append(ohlc)
        self.tick_data[symbol] = []  # Clear the processed ticks
        print(f"Aggregated 30-second bar for {symbol}: {ohlc}")

    def get_aggregated_bars(self, symbol):
        """
        Get the aggregated 30-second bars for a given symbol.
        :param symbol: The symbol to retrieve bars for.
        :return: List of 30-second bars for the symbol.
        """
        # Finalize the current interval bar before returning
        if self.tick_data[symbol]:
            self._create_bar(symbol)
        return self.aggregated_bars.get(symbol, [])
