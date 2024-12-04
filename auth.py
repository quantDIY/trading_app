#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:14:25 2024

@author: duncan
"""

import requests
from trading_app.constants import DEMO_API_URL, LIVE_API_URL, USE_LIVE_ENV

class Authenticator:
    def __init__(self, demo_credentials, live_credentials):
        """
        Initialize the Authenticator with demo and live credentials.
        :param demo_credentials: A dictionary with 'username', 'password', 'apiKey' for demo.
        :param live_credentials: A dictionary with 'username', 'password', 'apiKey' for live.
        """
        self.demo_credentials = demo_credentials
        self.live_credentials = live_credentials
        self.api_url = LIVE_API_URL if USE_LIVE_ENV else DEMO_API_URL
        self.token = None

    def authenticate(self):
        """
        Authenticate to the appropriate environment and retrieve the token.
        :return: The authentication token.
        """
        credentials = self.live_credentials if USE_LIVE_ENV else self.demo_credentials
        url = f"{self.api_url}/auth"

        payload = {
            "username": credentials["username"],
            "password": credentials["password"],
            "apiKey": credentials["apiKey"]
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.token = response.json()["token"]
            print(f"Authentication successful! Token: {self.token}")
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            raise

    def get_token(self):
        """
        Get the current token, ensuring authentication if not already done.
        :return: The authentication token.
        """
        if not self.token:
            self.authenticate()
        return self.token
