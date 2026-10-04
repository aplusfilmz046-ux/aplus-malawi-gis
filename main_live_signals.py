"""
main_live_signals.py
Run this on your own computer, with the Xness MT5 terminal open and
logged into your demo account. It polls new candles every POLL_SECONDS,
regenerates signals on the freshest data, and alerts you the first time
a new signal appears (it won't spam you with the same signal twice).

USAGE:
    python main_live_signals.py
"""

import time
import pandas as pd

import mt5_connector as mt5c
from smc_engine import generate_signals
from alert_system import fire_alert

SYMBOL = "EURUSD"          # change to whatever pair you want to watch
TIMEFRAME = "M15"          # execution timeframe
CANDLE_COUNT = 500         # how much history to keep in the rolling window
RISK_REWARD = 3.0
SESSION_FILTER = list(range(7, 17))  # UTC hours: London (7-16) + NY open overlap
POLL_SECONDS = 60          # how often to check for a new closed candle

already_alerted = set()    # signal timestamps we've already alerted on


def run():
    if not mt5c.connect():
        return

    print(f"Watching {SYMBOL} on {TIMEFRAME}. Press Ctrl+C to stop.")
    try:
        while True:
            df = mt5c.get_candles(SYMBOL, TIMEFRAME, CANDLE_COUNT)
            signals = generate_signals(df, risk_reward=RISK_REWARD, session_filter=SESSION_FILTER)

            for sig in signals:
                if sig.timestamp not in already_alerted:
                    fire_alert(sig)
                    already_alerted.add(sig.timestamp)

            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        mt5c.shutdown()


if __name__ == "__main__":
    run()
