import pytest
import asyncio
import pandas as pd
from trading_app.websocket_handler import WebSocketHandler


@pytest.mark.asyncio
async def test_websocket_live_data():
    """
    Test the WebSocketHandler by printing incoming live trade data in DataFrame format for 10 seconds.
    """
    handler = WebSocketHandler()

    try:
        # Connect to the WebSocket
        await handler.connect()

        print("Listening for live trade data for 10 seconds...")

        # Monitor live data for 10 seconds
        for _ in range(10):  # Loop for 10 iterations, one per second
            await asyncio.sleep(1)

            # Display the live_data DataFrame if it has data
            if not handler.live_data.empty:
                print("\nLive Trade Data:")
                print(handler.live_data.tail())  # Show the most recent trades
            else:
                print("\nNo live trade data received yet...")

    except Exception as e:
        print(f"Error during live data test: {e}")

    finally:
        # Close the connection after testing
        await handler.close_connection()
        print("WebSocket connection closed.")
