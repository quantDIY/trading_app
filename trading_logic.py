import pandas as pd
from trading_app.indicators import Indicators
from trading_app.order_entry import OrderEntry


class TradingLogic:
    def __init__(self):
        """
        Initialize the trading logic, including indicators and order entry.
        """
        self.indicators = Indicators()
        self.order_entry = OrderEntry()
        self.last_signal = None  # To avoid duplicate orders
        self.position = None  # Track the current position ('LONG', 'SHORT', or None)

    def process_data_and_trade(self, one_minute_bars):
        """
        Process the incoming data, calculate indicators, and make trading decisions.

        :param one_minute_bars: DataFrame containing one-minute aggregated bars.
        """
        # Step 1: Update one-minute bars
        self.indicators.aggregate_to_one_minute(one_minute_bars)

        # Step 2: Calculate moving averages
        self.indicators.calculate_moving_averages()

        # Step 3: Make trading decisions based on moving average crossovers
        self.execute_strategy()

    def execute_strategy(self):
        """
        Execute the trading strategy based on moving average crossovers.
        """
        # Fetch the latest moving averages
        moving_averages = self.indicators.moving_averages

        if moving_averages.empty:
            return  # No data to trade on

        # Get the most recent data points
        latest_data = moving_averages.iloc[-1]
        prev_data = moving_averages.iloc[-2] if len(moving_averages) > 1 else None

        # Current moving averages
        ma_200 = latest_data["200_minute"]
        ma_1000 = latest_data["1000_minute"]

        # Previous moving averages
        prev_ma_200 = prev_data["200_minute"] if prev_data is not None else None
        prev_ma_1000 = prev_data["1000_minute"] if prev_data is not None else None

        symbol = latest_data["symbol"]

        # Check for crossover signals
        if prev_ma_200 is not None and prev_ma_1000 is not None:
            # Bullish crossover
            if prev_ma_200 < prev_ma_1000 and ma_200 > ma_1000 and self.last_signal != "BUY":
                print("Bullish crossover detected. Placing buy order.")
                self.place_order(symbol, side="BUY")
                self.last_signal = "BUY"
                self.position = "LONG"

            # Bearish crossover
            elif prev_ma_200 > prev_ma_1000 and ma_200 < ma_1000 and self.last_signal != "SELL":
                print("Bearish crossover detected. Placing sell order.")
                self.place_order(symbol, side="SELL")
                self.last_signal = "SELL"
                self.position = "SHORT"

    def place_order(self, symbol, side):
        """
        Place a market order for the given symbol and side.

        :param symbol: The trading symbol (e.g., "NQ").
        :param side: "BUY" for long positions, "SELL" for short positions.
        """
        try:
            # Define order quantity and placeholder prices for bracket orders
            quantity = 1  # Example: trade 1 contract
            entry_price = None  # For market orders, entry price is not needed
            stop_loss = 10  # Stop-loss value (adjust based on strategy)
            take_profit = 20  # Take-profit value (adjust based on strategy)

            if side == "BUY":
                # Place a market order with a bracket
                self.order_entry.place_bracket_order(
                    symbol=symbol,
                    quantity=quantity,
                    entry_price=entry_price,  # Market price
                    stop_loss=entry_price - stop_loss,
                    take_profit=entry_price + take_profit,
                    side="BUY",
                    order_type="MARKET"
                )
            elif side == "SELL":
                # Place a market order with a bracket
                self.order_entry.place_bracket_order(
                    symbol=symbol,
                    quantity=quantity,
                    entry_price=entry_price,  # Market price
                    stop_loss=entry_price + stop_loss,
                    take_profit=entry_price - take_profit,
                    side="SELL",
                    order_type="MARKET"
                )
        except Exception as e:
            print(f"Error placing order: {e}")
