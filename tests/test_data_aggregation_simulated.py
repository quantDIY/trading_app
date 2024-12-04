from trading_app.data_aggregation import DataAggregator

def test_data_aggregation_with_simulated_data():
    """
    Test the DataAggregator functionality using simulated tick data.
    """
    aggregator = DataAggregator()

    # Simulated tick data
    simulated_ticks = [
        {"timestamp": "2024-12-03T09:30:00", "symbol": "NQ", "price": 15800.5, "volume": 10},
        {"timestamp": "2024-12-03T09:30:10", "symbol": "NQ", "price": 15802.0, "volume": 15},
        {"timestamp": "2024-12-03T09:30:25", "symbol": "NQ", "price": 15803.5, "volume": 8},
        {"timestamp": "2024-12-03T09:30:35", "symbol": "NQ", "price": 15801.0, "volume": 20},
        {"timestamp": "2024-12-03T09:30:50", "symbol": "NQ", "price": 15804.0, "volume": 12},
    ]

    # Add simulated ticks to the aggregator
    for tick in simulated_ticks:
        aggregator.add_tick(tick)

    # Retrieve aggregated 30-second bars
    bars = aggregator.get_aggregated_bars("NQ")

    # Assertions to validate the aggregation
    assert len(bars) == 2, f"Expected 2 bars but got {len(bars)}"
    assert bars[0]["open"] == 15800.5
    assert bars[0]["high"] == 15803.5
    assert bars[0]["low"] == 15800.5
    assert bars[0]["close"] == 15803.5
    assert bars[0]["volume"] == 33
    assert bars[1]["open"] == 15801.0
    assert bars[1]["high"] == 15804.0
    assert bars[1]["low"] == 15801.0
    assert bars[1]["close"] == 15804.0
    assert bars[1]["volume"] == 32
    print("Simulated data aggregation test passed!")
