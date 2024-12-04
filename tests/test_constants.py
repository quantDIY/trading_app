#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:14:25 2024

@author: duncan
"""

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading_app.constants import DEMO_CREDENTIALS, LIVE_CREDENTIALS, USE_LIVE_ENV, API_URL

def test_constants():
    print("USE_LIVE_ENV:", USE_LIVE_ENV)
    print("API_URL:", API_URL)
    print("DEMO_CREDENTIALS:", DEMO_CREDENTIALS)
    print("LIVE_CREDENTIALS:", LIVE_CREDENTIALS)

if __name__ == "__main__":
    try:
        test_constants()
    except ValueError as e:
        print("Error:", e)
