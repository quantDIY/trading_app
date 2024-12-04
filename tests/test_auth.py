#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:14:25 2024

@author: duncan
"""

from trading_app.auth import Authenticator
from trading_app.constants import DEMO_CREDENTIALS, LIVE_CREDENTIALS

def test_auth():
    """
    Test the authentication functionality.
    """
    # Initialize the authenticator
    authenticator = Authenticator(
        demo_credentials=DEMO_CREDENTIALS,
        live_credentials=LIVE_CREDENTIALS
    )

    try:
        # Authenticate and retrieve the token
        token = authenticator.get_token()
        print("Authentication successful!")
        print(f"Token: {token}")
    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    test_auth()
