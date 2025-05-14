# test/smoke_test.py
import pandas as pd
from bot.core import apply_strategies

def test_indicators_run():
    # tiny dummy DataFrame (5 rows)
    df = pd.DataFrame({
        "close": [10, 10.1, 10.2, 10.1, 10.05]
    })
    out = apply_strategies(df.copy())
    # MACD_Signal or BB_Signal column should exist
    assert "Signal" in out.columns
