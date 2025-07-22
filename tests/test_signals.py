import pandas as pd
from analysis.signals import generate_trade_signals

def test_generate_trade_signals():
    # Create dummy data
    df = pd.DataFrame({
        'close': [1,2,3,4,5,4,3,2,1,2,3,4,5],
    })
    signals = generate_trade_signals(df)
    assert 'final_signal' in signals.columns 