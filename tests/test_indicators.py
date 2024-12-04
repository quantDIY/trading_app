import pytest
import asyncio
from trading_app.indicators import Indicators


@pytest.mark.asyncio
async def test_indicators_live_data():
    """
    Test the Indicators class using live data from WebSocketHandler.
    """
    indicators = Indicators()

    try:
        # Start processing live data for 60 seconds
        print("Testing Indicators with live WebSocket data for 60 seconds...")
        await asyncio.wait_for(indicators.process_data(), timeout=60)

    except asyncio.TimeoutError:
        print("Test completed after 60 seconds.")

    finally:
        await indicators.websocket_handler.close_connection()
        print("WebSocket connection closed.")
