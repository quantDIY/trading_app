#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:12:50 2024

@author: duncan
"""
import asyncio
import websockets
import json
import pandas as pd
from trading_app.streamID_handler import StreamIDHandler
from trading_app.constants import API_URL, SYMBOLS


class WebSocketHandler:
    def __init__(self):
        """
        Initialize the WebSocket handler.
        """
        self.stream_id_handler = StreamIDHandler()
        self.token = self.stream_id_handler.authenticator.get_token()
        self.stream_id = None
        self.connection = None
        self.historical_data = pd.DataFrame(columns=["timestamp", "symbol", "price", "volume"])
        self.live_data = pd.DataFrame(columns=["timestamp", "symbol", "price", "volume"])
        self.reconnect_attempts = 0

    async def connect(self):
        """
        Connect to the WebSocket using the current streamId.
        """
        self.stream_id = self.stream_id_handler.get_stream_id()
        websocket_url = f"wss://{API_URL.split('://')[1]}/stream/{self.stream_id}?token={self.token}"
        print(f"Connecting to WebSocket: {websocket_url}")

        try:
            self.connection = await websockets.connect(websocket_url)
            self.reconnect_attempts = 0
            print("WebSocket connection established.")

            # Subscribe to both live and historical trades
            await self.subscribe_trades()

            await self.handle_messages()

        except websockets.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}")
            await self.reconnect()

        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            await self.reconnect()

    async def reconnect(self):
        """
        Handle WebSocket reconnection.
        """
        self.reconnect_attempts += 1
        if self.reconnect_attempts > 5:
            print("Max reconnection attempts reached. Exiting.")
            return

        print(f"Reconnecting... Attempt {self.reconnect_attempts}")
        self.stream_id_handler.refresh_stream_id()
        await asyncio.sleep(5)  # Wait before retrying
        await self.connect()

    async def subscribe_trades(self):
        """
        Subscribe to live trades and historical tick data for each symbol.
        """
        for symbol, current_symbol in SYMBOLS.items():
            subscription_message = {
                "action": "subscribe",
                "type": "trades",
                "symbol": current_symbol,
                "flags": ["live", "historical"]  # Flags to indicate both live and historical data
            }
            await self.connection.send(json.dumps(subscription_message))
            print(f"Subscribed to live and historical trades for {symbol} ({current_symbol}).")

    async def handle_messages(self):
        """
        Handle incoming WebSocket messages.
        """
        try:
            async for message in self.connection:
                data = json.loads(message)
                await self.route_message(data)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")
            await self.reconnect()
        except Exception as e:
            print(f"Error handling WebSocket messages: {e}")

    async def route_message(self, data):
        """
        Route incoming data based on its type.
        """
        if "trades" in data:
            self.handle_trade_data(data["trades"])

    def handle_trade_data(self, trade_data):
        """
        Handle incoming trade data for live and historical trades.
        """
        for trade in trade_data:
            trade_entry = {
                "timestamp": trade.get("timestamp"),
                "symbol": trade.get("symbol"),
                "price": trade.get("price"),
                "volume": trade.get("volume"),
            }

            # Determine if the trade is historical or live based on timestamp logic or API fields
            if trade.get("is_historical", False):
                self.historical_data = pd.concat([
                    self.historical_data,
                    pd.DataFrame([trade_entry])
                ])
                print(f"[Historical Trade] {trade_entry}")
            else:
                self.live_data = pd.concat([
                    self.live_data,
                    pd.DataFrame([trade_entry])
                ])
                print(f"[Live Trade] {trade_entry}")

    async def close_connection(self):
        """
        Close the WebSocket connection.
        """
        if self.connection:
            await self.connection.close()
            print("WebSocket connection closed.")
