import pytest
import asyncio
from trading_app.websocket_handler import WebSocketHandler

@pytest.mark.asyncio
async def test_websocket_handler():
    """
    Test the WebSocketHandler functionality.
    """
    handler = WebSocketHandler()

    # Connect to the WebSocket
    await handler.connect()

    # Keep the connection open for 10 seconds for testing
    await asyncio.sleep(10)

    # Close the connection
    await handler.close_connection()
