import pytest
import asyncio
from trading_app.websocket_handler import WebSocketHandler
from trading_app.data_aggregation import DataAggregator


@pytest.mark.asyncio
async def test_data_aggregation_with_live_feed():
    """
    Test the DataAggregator with live tick data from the WebSocketHandler.
    """
    websocket_handler = WebSocketHandler()
    data_aggregator = DataAggregator()

    async def process_live_data():
        """
        Process live data from the WebSocket and pass it to the DataAggregator.
        """
        try:
            await websocket_handler.connect()
            print("WebSocket connected. Aggregating live data for 30 seconds...")

            # Aggregate live tick data for 30 seconds
            start_time = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_time < 30:
                for tick in websocket_handler.live_data.to_dict("records"):
                    data_aggregator.add_tick(tick)
                await asyncio.sleep(1)  # Allow for new data to arrive

        finally:
            await websocket_handler.close_connection()

    await process_live_data()

    # Get aggregated bars for a symbol (e.g., "NQ")
    symbol = "NQ"
    bars = data_aggregator.get_aggregated_bars(symbol)
    assert len(bars) > 0, f"No 30-second bars were created for {symbol}."
    print(f"Aggregated 30-second bars for {symbol}: {bars}")
