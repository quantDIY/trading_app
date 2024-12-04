import pandas as pd
from trading_app.websocket_handler import WebSocketHandler


class Indicators:
    def __init__(self):
        """
        Initialize the Indicators class.
        """
        self.websocket_handler = WebSocketHandler()  # Connect to WebSocket data
        self.one_minute_bars = pd.DataFrame(columns=["timestamp", "symbol", "open", "high", "low", "close", "volume"])
        self.moving_averages = pd.DataFrame(columns=["timestamp", "symbol", "200_minute", "1000_minute"])

    async def process_data(self):
        """
        Process incoming data from WebSocket and calculate indicators.
        """
        await self.websocket_handler.connect()
        print("WebSocket connected. Aggregating 30-second bars into 1-minute bars...")

        while True:
            # Get the live tick data
            tick_data = self.websocket_handler.live_data

            # Aggregate the tick data into 30-second bars if available
            if not tick_data.empty:
                self.aggregate_to_one_minute(tick_data)

                # Calculate moving averages from the 1-minute bars
                self.calculate_moving_averages()

                # Print the most recent moving average values
                if not self.moving_averages.empty:
                    latest_ma = self.moving_averages.iloc[-1]
                    print(f"Latest Moving Averages: {latest_ma}")

    def aggregate_to_one_minute(self, bars_30s):
        """
        Aggregate 30-second bars into 1-minute bars.
        :param bars_30s: DataFrame with 30-second bars.
        :return: None
        """
        if bars_30s.empty:
            print("No data to aggregate for 1-minute bars.")
            return

        # Convert timestamp to ensure proper datetime format
        bars_30s["timestamp"] = pd.to_datetime(bars_30s["timestamp"])

        # Group by 1-minute intervals and aggregate
        bars_30s.set_index("timestamp", inplace=True)
        resampled = bars_30s.resample("1min").agg({
            "symbol": "first",
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }).dropna().reset_index()

        self.one_minute_bars = pd.concat([self.one_minute_bars, resampled], ignore_index=True).drop_duplicates(subset=["timestamp"])
        print("1-minute bars aggregated.")

    def calculate_moving_averages(self):
        """
        Calculate 200-minute and 1000-minute moving averages from 1-minute bars.
        :return: None
        """
        if self.one_minute_bars.empty:
            print("No 1-minute data available for moving averages.")
            return

        self.one_minute_bars["close"] = self.one_minute_bars["close"].astype(float)

        # Calculate moving averages
        self.one_minute_bars["200_minute"] = self.one_minute_bars["close"].rolling(window=200, min_periods=1).mean()
        self.one_minute_bars["1000_minute"] = self.one_minute_bars["close"].rolling(window=1000, min_periods=1).mean()

        # Record moving average positions for each minute
        moving_avg_positions = self.one_minute_bars[["timestamp", "symbol", "200_minute", "1000_minute"]].dropna()
        self.moving_averages = pd.concat([self.moving_averages, moving_avg_positions], ignore_index=True).drop_duplicates(subset=["timestamp"])
        print("Moving averages calculated and recorded.")
