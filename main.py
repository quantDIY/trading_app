import asyncio
from trading_app.websocket_handler import WebSocketHandler
from trading_app.data_aggregation import DataAggregator
from trading_app.indicators import Indicators
from trading_app.trading_logic import TradingLogic


async def main():
    """
    Main entry point for the trading application.
    """
    print("Initializing trading application...")

    # Initialize core components
    websocket_handler = WebSocketHandler()
    data_aggregator = DataAggregator()
    indicators = Indicators()
    trading_logic = TradingLogic()

    try:
        # Connect to WebSocket
        await websocket_handler.connect()

        print("WebSocket connected. Streaming live data...")
        while True:
            # Retrieve live tick data
            live_data = websocket_handler.live_data.copy()

            # If new tick data exists, process it
            if not live_data.empty:
                # Aggregate tick data into 30-second bars
                data_aggregator.aggregate(live_data)

                # Retrieve 30-second bars
                bars_30s = data_aggregator.get_aggregated_bars()

                # Process indicators and make trading decisions
                trading_logic.process_data_and_trade(bars_30s)

            await asyncio.sleep(1)  # Avoid overloading the event loop

    except KeyboardInterrupt:
        print("\nShutting down the trading application...")

    finally:
        # Ensure WebSocket connection is closed
        await websocket_handler.close_connection()
        print("Application stopped.")


if __name__ == "__main__":
    asyncio.run(main())
