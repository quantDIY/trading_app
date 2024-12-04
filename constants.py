#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:14:25 2024

@author: duncan
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Demo credentials
DEMO_CREDENTIALS = {
    "username": os.getenv("TRADING_APP_DEMO_USERNAME"),
    "password": os.getenv("TRADING_APP_DEMO_PASSWORD"),
    "apiKey": os.getenv("TRADING_APP_DEMO_API_KEY")
}

# Live credentials
LIVE_CREDENTIALS = {
    "username": os.getenv("TRADING_APP_LIVE_USERNAME"),
    "password": os.getenv("TRADING_APP_LIVE_PASSWORD"),
    "apiKey": os.getenv("TRADING_APP_LIVE_API_KEY")
}

# Environment toggle
USE_LIVE_ENV = os.getenv("USE_LIVE_ENV", "False").lower() == "true"

# API URLs
DEMO_API_URL = os.getenv("DEMO_API_URL", "https://demo.ironbeamapi.com/v2")
LIVE_API_URL = os.getenv("LIVE_API_URL", "https://live.ironbeamapi.com/v2")
API_URL = LIVE_API_URL if USE_LIVE_ENV else DEMO_API_URL

# Hardcoded symbols maximum 10
SYMBOLS = {
    #"ES": "ESZ24",  # E-mini S&P 500 December 2024
    #"CL": "CLZ24",  # Crude Oil December 2024
    #"GC": "GCZ24",   # Gold December 2024
    "NQ": "NQ.Z24"  # E-mini Nasdaq December 2024
}
