#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:14:25 2024

@author: duncan
"""

import requests
from trading_app.constants import API_URL, DEMO_CREDENTIALS, LIVE_CREDENTIALS
from trading_app.auth import Authenticator


class StreamIDHandler:
    def __init__(self):
        """
        Initialize the handler, authenticate, and create a streamId.
        """
        # Pass demo and live credentials to the Authenticator
        self.authenticator = Authenticator(
            demo_credentials=DEMO_CREDENTIALS,
            live_credentials=LIVE_CREDENTIALS
        )
        self.token = self.authenticator.get_token()  # Retrieve the authentication token
        self.stream_id = None
        self.create_stream_id()  # Generate the initial streamId

    def create_stream_id(self):
        """
        Create a new streamId using the Ironbeam API.
        """
        try:
            url = f"{API_URL}/stream/create"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP issues
            self.stream_id = response.json().get("streamId")
            print(f"Created new streamId: {self.stream_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error creating streamId: {e}")
            raise

    def refresh_stream_id(self):
        """
        Refresh the streamId by creating a new one.
        """
        print("Refreshing streamId...")
        self.create_stream_id()

    def get_stream_id(self):
        """
        Retrieve the current streamId.
        :return: The current streamId.
        """
        if not self.stream_id:
            self.create_stream_id()
        return self.stream_id
