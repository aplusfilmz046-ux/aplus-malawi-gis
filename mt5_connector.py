"""
mt5_connector.py
Connects to your Xness demo account through the MetaTrader5 terminal.

REQUIREMENTS (run these on YOUR computer, not in this chat):
  1. Install the MetaTrader 5 desktop terminal from Xness and log into
     your demo account inside it at least once.
  2. pip install MetaTrader5 pandas
  3. Keep the MT5 terminal application open while this script runs —
     the Python package talks to the running terminal, it does not
     replace it.

This file only READS price data. It never sends orders — that is a
deliberate choice matching your "signals only, I execute manually"
plan.
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime


TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
}


def connect() -> bool:
    """Initializes connection to whichever MT5 terminal is already logged in."""
    if not mt5.initialize():
        print("MT5 initialize() failed:", mt5.last_error())
        return False
    info = mt5.account_info()
    if info is None:
        print("Could not read account info — are you logged into the demo account in MT5?")
        return False
    print(f"Connected: account #{info.login}, balance {info.balance} {info.currency}, server {info.server}")
    return True


def get_candles(symbol: str, timeframe: str = "M15", count: int = 500) -> pd.DataFrame:
    """
    Fetches the last `count` closed candles for `symbol` at `timeframe`
    and returns a DataFrame indexed by UTC time with columns
    open, high, low, close, tick_volume.
    """
    tf = TIMEFRAME_MAP[timeframe]
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"No data returned for {symbol} {timeframe}: {mt5.last_error()}")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df = df.set_index("time")
    return df[["open", "high", "low", "close", "tick_volume"]]


def shutdown():
    mt5.shutdown()
