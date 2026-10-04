"""
backtester.py
Walks forward candle-by-candle after each signal is generated to see
whether stop-loss or take-profit was hit first. Reports win rate,
expectancy, and equity curve. This never looks into the future beyond
the signal's own timestamp — each signal is only evaluated against
candles that occur after it.
"""

import pandas as pd
from typing import List
from smc_engine import Signal


def evaluate_signals(df: pd.DataFrame, signals: List[Signal], max_lookahead: int = 100) -> pd.DataFrame:
    """
    For each signal, scan forward up to max_lookahead candles to see
    whether price hit stop_loss or take_profit first.
    Returns a DataFrame log with outcome per signal.
    """
    records = []
    for sig in signals:
        try:
            start_idx = df.index.get_loc(sig.timestamp)
        except KeyError:
            continue

        outcome = "open"  # neither hit within lookahead window
        exit_price = None
        exit_time = None

        for j in range(start_idx + 1, min(start_idx + 1 + max_lookahead, len(df))):
            bar = df.iloc[j]
            if sig.direction == "BUY":
                if bar["low"] <= sig.stop_loss:
                    outcome, exit_price, exit_time = "loss", sig.stop_loss, df.index[j]
                    break
                if bar["high"] >= sig.take_profit:
                    outcome, exit_price, exit_time = "win", sig.take_profit, df.index[j]
                    break
            else:  # SELL
                if bar["high"] >= sig.stop_loss:
                    outcome, exit_price, exit_time = "loss", sig.stop_loss, df.index[j]
                    break
                if bar["low"] <= sig.take_profit:
                    outcome, exit_price, exit_time = "win", sig.take_profit, df.index[j]
                    break

        records.append({
            "timestamp": sig.timestamp,
            "direction": sig.direction,
            "entry": sig.entry,
            "stop_loss": sig.stop_loss,
            "take_profit": sig.take_profit,
            "outcome": outcome,
            "exit_price": exit_price,
            "exit_time": exit_time,
        })

    return pd.DataFrame(records)


def summarize(results: pd.DataFrame, risk_reward: float = 3.0) -> dict:
    """Compute win rate and expectancy in R-multiples."""
    closed = results[results["outcome"].isin(["win", "loss"])]
    n = len(closed)
    if n == 0:
        return {"trades": 0, "win_rate": None, "expectancy_R": None}

    wins = (closed["outcome"] == "win").sum()
    win_rate = wins / n
    # Expectancy in R: win_rate * RR - loss_rate * 1
    expectancy = win_rate * risk_reward - (1 - win_rate) * 1
    return {
        "trades": n,
        "wins": int(wins),
        "losses": int(n - wins),
        "win_rate": round(win_rate, 3),
        "expectancy_R": round(expectancy, 3),
    }
