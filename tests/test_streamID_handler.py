#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 14:20:20 2024

@author: duncan
"""

from trading_app.streamID_handler import StreamIDHandler

def test_stream_id_handler():
    """
    Test the StreamIDHandler functionality.
    """
    handler = StreamIDHandler()
    
    # Test getting the initial streamId
    initial_stream_id = handler.get_stream_id()
    assert initial_stream_id is not None, "Failed to create initial streamId"
    print(f"Initial streamId: {initial_stream_id}")
    
    # Test refreshing the streamId
    handler.refresh_stream_id()
    refreshed_stream_id = handler.get_stream_id()
    assert refreshed_stream_id is not None, "Failed to refresh streamId"
    assert initial_stream_id != refreshed_stream_id, "StreamID did not update!"
    print(f"Refreshed streamId: {refreshed_stream_id}")
