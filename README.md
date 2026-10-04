# SMC Day-Trading Signal Bot (Signals Only — No Auto-Execution)

## The strategy this codes up

This is a Smart Money Concepts (SMC) day-trading strategy, the same
framework called ICT trading, which shows up repeatedly as one of the
most-used retail approaches right now. It does NOT predict price —
it looks for a specific, repeatable structural pattern:

1. **Swing structure** — find swing highs/lows using the 3-candle
   fractal rule (a candle whose high/low is more extreme than both
   neighbors).
2. **Break of Structure (BOS) / Change of Character (CHoCH)** — when
   price closes beyond the last swing point, that confirms the current
   trend (BOS) or flags a reversal (CHoCH).
3. **Order Block** — the last opposite-colored candle right before the
   breakout candle. This is the zone institutional-style theory says
   is where big orders were placed.
4. **Retracement + rejection** — wait for price to pull back into that
   Order Block and print a rejection candle (closes back in the
   direction of the break).
5. **Entry / Stop / Target** — enter at the rejection candle's close,
   stop just beyond the Order Block, target fixed at 1:3 risk-reward
   (configurable).
6. **Session filter** — only watch during London + New York session
   hours (UTC 7–16 by default), since that's when forex has the
   volume to make structure breaks meaningful; thin overnight ranges
   produce a lot of false signals.

This is signals-only by design, matching what you asked for: the bot
watches the market and alerts you, you decide whether to actually take
the trade in your Xness demo account.

## Files

| File | Purpose |
|---|---|
| `smc_engine.py` | Core detection logic: swings, BOS/CHoCH, order blocks, FVGs, signal generation |
| `backtester.py` | Replays historical signals to compute win rate and expectancy (in R-multiples) |
| `mt5_connector.py` | Reads live/historical price data from your Xness MT5 terminal. Read-only — never places orders |
| `alert_system.py` | Beeps + optional Telegram push when a new signal fires |
| `main_live_signals.py` | Ties it together into a polling loop you run locally |

## Setup on your machine

1. Install the MetaTrader 5 terminal from Xness (if not already) and
   log into your demo account inside it once.
2. `pip install MetaTrader5 pandas numpy`
3. Leave the MT5 terminal open in the background.
4. Edit `main_live_signals.py`: set `SYMBOL` to the pair you want to
   watch (e.g. `"EURUSD"`, `"GBPUSD"`).
5. Run: `python main_live_signals.py`
6. When a signal fires, you'll see entry/stop/target printed and hear
   a beep. Look at the chart yourself, decide if you agree, and place
   the trade manually in your demo account if you do.

## Backtesting first (do this before running live)

Before trusting any live signal, backtest on history you pull from
MT5:

```python
import mt5_connector as mt5c
from smc_engine import generate_signals
from backtester import evaluate_signals, summarize

mt5c.connect()
df = mt5c.get_candles("EURUSD", "M15", 5000)  # last 5000 M15 candles
signals = generate_signals(df, risk_reward=3.0, session_filter=list(range(7,17)))
results = evaluate_signals(df, signals)
print(summarize(results, risk_reward=3.0))
mt5c.shutdown()
```

`win_rate` and `expectancy_R` tell you whether this specific pair/
timeframe combination has historically had an edge with these rules.
An expectancy above 0 means the strategy made money on average per
trade over that sample — but past structure repeating is never
guaranteed, so treat this as a filter for "is this worth forward
testing," not proof it will keep working.

## Honest limitations

- This detects one specific SMC pattern. It will not catch every good
  setup, and it will fire on some setups that fail — no strategy here
  or anywhere gets this right every time. All the "profitable
  strategy" guides agree on this: the strategy is not what saves an
  account, risk management is.
- The order-block and FVG rules used here are simplified,
  interpretable versions of concepts that professional SMC traders
  argue about the exact definition of. Expect to tune the lookback
  windows, the zone-touch tolerance, and the staleness limit once you
  see it running against real data.
- This is Module 1–2 territory from your original curriculum (swing
  detection, structure breaks) already wired end-to-end, plus the
  order-block/FVG layer. Module 3 (feature engineering) and Module 4
  (the ML classifier that scores signal quality) are not built yet —
  right now every signal that matches the pattern fires, with no
  learned filtering on top. That's the natural next step once you've
  watched this run for a while and have real win/loss data to train
  the classifier on.
