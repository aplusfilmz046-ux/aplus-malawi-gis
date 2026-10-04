"""
alert_system.py
Turns a Signal object into something that will actually wake you up:
  - a loud console beep (works while you're near the computer)
  - an optional Telegram message (works while you're asleep in another
    room, as long as your phone has notifications on)

Telegram setup (optional, 5 minutes):
  1. In Telegram, message @BotFather -> /newbot -> follow prompts -> copy the token.
  2. Message your new bot once (anything) so it can reply to you.
  3. Visit https://api.telegram.org/bot<TOKEN>/getUpdates in a browser,
     find "chat":{"id": ...} in the JSON, copy that number.
  4. Fill TELEGRAM_TOKEN and TELEGRAM_CHAT_ID below.
"""

import sys
from smc_engine import Signal

TELEGRAM_TOKEN = ""      # fill in if you want phone alerts
TELEGRAM_CHAT_ID = ""    # fill in if you want phone alerts


def beep(times: int = 3):
    for _ in range(times):
        sys.stdout.write("\a")
        sys.stdout.flush()


def format_signal(sig: Signal) -> str:
    return (
        f"[{sig.direction}] setup detected\n"
        f"Time: {sig.timestamp}\n"
        f"Entry: {sig.entry:.5f}\n"
        f"Stop Loss: {sig.stop_loss:.5f}\n"
        f"Take Profit: {sig.take_profit:.5f}\n"
        f"R:R: 1:{sig.risk_reward}\n"
        f"Reason: {sig.reason}\n"
    )


def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return  # not configured, skip silently
    import requests  # pip install requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=10)
    except Exception as e:
        print("Telegram send failed:", e)


def fire_alert(sig: Signal):
    message = format_signal(sig)
    print("=" * 50)
    print(message)
    print("=" * 50)
    beep()
    send_telegram(message)
