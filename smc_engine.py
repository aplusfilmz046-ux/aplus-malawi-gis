"""
smc_engine.py
Smart Money Concepts (SMC) day-trading signal engine.

Pipeline:
  1. Detect swing highs/lows (3-candle fractal rule)
  2. Determine market structure (HH/HL = bullish, LH/LL = bearish)
  3. Detect Break of Structure (BOS) / Change of Character (CHoCH)
  4. Locate the Order Block that caused the break
  5. Locate Fair Value Gaps (FVG) inside the impulse leg
  6. When price returns into the Order Block / FVG zone with a rejection
     candle, emit a SIGNAL with entry / stop loss / take profit.

This module produces SIGNALS ONLY. It never places trades. It is meant
to be paired with a data feed (mt5_connector.py) and an alert layer
(alert_system.py).
"""

from dataclasses import dataclass
from typing import Optional, List
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Signal:
    timestamp: pd.Timestamp
    direction: str          # "BUY" or "SELL"
    entry: float
    stop_loss: float
    take_profit: float
    reason: str              # human-readable explanation
    risk_reward: float


# ---------------------------------------------------------------------------
# Step 1: Swing highs / lows (3-candle fractal rule)
# ---------------------------------------------------------------------------

def find_swings(df: pd.DataFrame) -> pd.DataFrame:
    """
    df must have columns: open, high, low, close (indexed by time, ascending).
    Adds boolean columns 'swing_high' and 'swing_low' using the classic
    3-candle rule: the middle candle's high (low) is higher (lower) than
    both its neighbors.
    """
    df = df.copy()
    high = df["high"].values
    low = df["low"].values
    n = len(df)

    swing_high = np.zeros(n, dtype=bool)
    swing_low = np.zeros(n, dtype=bool)

    for i in range(1, n - 1):
        if high[i] > high[i - 1] and high[i] > high[i + 1]:
            swing_high[i] = True
        if low[i] < low[i - 1] and low[i] < low[i + 1]:
            swing_low[i] = True

    df["swing_high"] = swing_high
    df["swing_low"] = swing_low
    return df


# ---------------------------------------------------------------------------
# Step 2 & 3: Market structure + Break of Structure / Change of Character
# ---------------------------------------------------------------------------

def detect_structure_breaks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Walks forward through confirmed swing points and tags each candle with:
      - 'trend'   : current structural bias ('bullish' / 'bearish' / None)
      - 'bos'     : True where a Break Of Structure just occurred (trend continuation)
      - 'choch'   : True where a Change Of Character just occurred (trend reversal)
      - 'break_level' : the swing price level that was broken
    """
    df = df.copy()
    df["trend"] = None
    df["bos"] = False
    df["choch"] = False
    df["break_level"] = np.nan

    last_swing_high = None
    last_swing_low = None
    trend = None

    for i in range(len(df)):
        close = df["close"].iloc[i]

        # Update trailing swing references
        if df["swing_high"].iloc[i]:
            last_swing_high = df["high"].iloc[i]
        if df["swing_low"].iloc[i]:
            last_swing_low = df["low"].iloc[i]

        # Bullish break: close above the last confirmed swing high
        if last_swing_high is not None and close > last_swing_high:
            if trend == "bearish":
                df.at[df.index[i], "choch"] = True
            elif trend == "bullish":
                df.at[df.index[i], "bos"] = True
            else:
                df.at[df.index[i], "bos"] = True
            df.at[df.index[i], "break_level"] = last_swing_high
            trend = "bullish"
            last_swing_high = None  # consumed

        # Bearish break: close below the last confirmed swing low
        elif last_swing_low is not None and close < last_swing_low:
            if trend == "bullish":
                df.at[df.index[i], "choch"] = True
            elif trend == "bearish":
                df.at[df.index[i], "bos"] = True
            else:
                df.at[df.index[i], "bos"] = True
            df.at[df.index[i], "break_level"] = last_swing_low
            trend = "bearish"
            last_swing_low = None  # consumed

        df.at[df.index[i], "trend"] = trend

    return df


# ---------------------------------------------------------------------------
# Step 4: Order Block identification
# ---------------------------------------------------------------------------

def find_order_block(df: pd.DataFrame, break_index: int, direction: str) -> Optional[dict]:
    """
    Given the index where a BOS/CHoCH happened, walk backward to find the
    last opposite-colored candle before the impulsive move — that candle's
    range is the Order Block.

    direction: 'bullish' or 'bearish' (direction of the break)
    Returns dict with 'top', 'bottom', 'index' or None if not found.
    """
    lookback_limit = 15  # don't search further back than this
    start = max(0, break_index - lookback_limit)

    if direction == "bullish":
        # last bearish (down) candle before the up-move
        for i in range(break_index - 1, start - 1, -1):
            o, c = df["open"].iloc[i], df["close"].iloc[i]
            if c < o:  # bearish candle
                return {
                    "top": df["high"].iloc[i],
                    "bottom": df["low"].iloc[i],
                    "index": i,
                }
    else:
        # last bullish (up) candle before the down-move
        for i in range(break_index - 1, start - 1, -1):
            o, c = df["open"].iloc[i], df["close"].iloc[i]
            if c > o:  # bullish candle
                return {
                    "top": df["high"].iloc[i],
                    "bottom": df["low"].iloc[i],
                    "index": i,
                }
    return None


# ---------------------------------------------------------------------------
# Step 5: Fair Value Gap (FVG) — a 3-candle imbalance
# ---------------------------------------------------------------------------

def find_fvg(df: pd.DataFrame, i: int, direction: str) -> Optional[dict]:
    """
    Checks candles (i-2, i-1, i) for a Fair Value Gap:
      Bullish FVG: low of candle i-2 candle's ... > wait, standard definition:
        Bullish FVG: high[i-2] < low[i]   (gap between candle 1 high and candle 3 low)
        Bearish FVG: low[i-2] > high[i]
    Returns the gap zone or None.
    """
    if i < 2:
        return None
    if direction == "bullish":
        if df["high"].iloc[i - 2] < df["low"].iloc[i]:
            return {"top": df["low"].iloc[i], "bottom": df["high"].iloc[i - 2]}
    else:
        if df["low"].iloc[i - 2] > df["high"].iloc[i]:
            return {"top": df["low"].iloc[i - 2], "bottom": df["high"].iloc[i]}
    return None


# ---------------------------------------------------------------------------
# Step 6: Signal generation
# ---------------------------------------------------------------------------

def generate_signals(
    df: pd.DataFrame,
    risk_reward: float = 3.0,
    session_filter: Optional[List[int]] = None,
) -> List[Signal]:
    """
    Full pipeline: swings -> structure -> order blocks -> retracement entry.

    session_filter: optional list of allowed UTC hours (e.g. list(range(7,17))
    for London+NY overlap). If None, no session filtering is applied.
    df.index must be tz-aware or naive UTC timestamps.
    """
    df = find_swings(df)
    df = detect_structure_breaks(df)

    signals: List[Signal] = []
    zone_watch = None  # currently active order-block zone waiting for retest

    for i in range(len(df)):
        row = df.iloc[i]

        # A fresh structural break -> define a new zone to watch
        if row["bos"] or row["choch"]:
            direction = row["trend"]
            ob = find_order_block(df, i, direction)
            if ob is not None:
                zone_watch = {
                    "direction": direction,
                    "top": ob["top"],
                    "bottom": ob["bottom"],
                    "created_at": i,
                }
            continue

        # If we have an active zone, watch for price to retrace into it
        if zone_watch is not None:
            age = i - zone_watch["created_at"]
            if age > 40:  # zone goes stale after 40 candles unmitigated
                zone_watch = None
                continue

            if session_filter is not None:
                hour = df.index[i].hour
                if hour not in session_filter:
                    continue

            low, high, close, open_ = row["low"], row["high"], row["close"], row["open"]
            direction = zone_watch["direction"]

            if direction == "bullish":
                touched = low <= zone_watch["top"] and low >= zone_watch["bottom"] - (
                    zone_watch["top"] - zone_watch["bottom"]
                )
                rejection = close > open_  # bullish rejection candle
                if touched and rejection:
                    entry = close
                    stop_loss = zone_watch["bottom"] * 0.999  # small buffer
                    risk = entry - stop_loss
                    take_profit = entry + risk * risk_reward
                    if risk > 0:
                        signals.append(Signal(
                            timestamp=df.index[i],
                            direction="BUY",
                            entry=entry,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            reason="Bullish BOS -> retrace into Order Block -> rejection candle",
                            risk_reward=risk_reward,
                        ))
                        zone_watch = None

            else:  # bearish
                touched = high >= zone_watch["bottom"] and high <= zone_watch["top"] + (
                    zone_watch["top"] - zone_watch["bottom"]
                )
                rejection = close < open_  # bearish rejection candle
                if touched and rejection:
                    entry = close
                    stop_loss = zone_watch["top"] * 1.001
                    risk = stop_loss - entry
                    take_profit = entry - risk * risk_reward
                    if risk > 0:
                        signals.append(Signal(
                            timestamp=df.index[i],
                            direction="SELL",
                            entry=entry,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            reason="Bearish BOS -> retrace into Order Block -> rejection candle",
                            risk_reward=risk_reward,
                        ))
                        zone_watch = None

    return signals
