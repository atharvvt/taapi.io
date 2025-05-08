# In a market with low volatility or minimal movement, traditional high-signal indicators like RSI, EMA crossovers, and price gaps are less decisive. Here are strategic approaches for Buy, Sell, Exit, and Hold decisions under such conditions, tailored to your dataset using RSI and EMA behavior:

# ⸻

# 1. Buy Strategies

# Buy when:
# 	•	RSI slowly climbs from below 40 to around 45–50, indicating accumulation in a low-volatility environment.
# 	•	Price is slightly below or just touched EMA and starts moving up (e.g., last_price < EMA but EMA is flat or starting to rise).
# 	•	Multiple small bullish RSI changes (e.g., +1 to +3%) are observed across 3–5 candles, suggesting building pressure.
# 	•	EMA remains stable or slightly increasing while price stays within 0.1–0.2% of EMA — a classic consolidation zone for re-entry.

# ⸻

# 2. Sell Strategies

# Sell when:
# 	•	RSI falls gently from above 60 to around 50–55, signaling fading bullishness.
# 	•	Price is slightly above EMA, but EMA is turning flat or slightly downward.
# 	•	Small negative RSI changes over 3+ intervals (-1% to -3%) without volume or price breakout.
# 	•	Failed breakout pattern: price crossed above EMA but quickly returns near or below it, indicating weak momentum.

# ⸻

# 3. Exit (Close Position) Strategies

# Exit when:
# 	•	RSI flattens between 45–55 for multiple candles, signaling indecision.
# 	•	Price converges tightly with EMA and RSI variance stays under ±1% for 15–30 minutes.
# 	•	No directional price bias for 4–6 intervals after entry — preserve capital by exiting early.
# 	•	Entry was based on expected momentum but EMA remains unchanged or reverts slightly.

# ⸻

# 4. Hold Strategies

# Hold when:
# 	•	RSI is in the range of 45–55 with micro-movements and you’re not at a loss or too close to your stop-loss.
# 	•	The EMA direction is consistent, even if price is sideways — this indicates macro trend stability.
# 	•	RSI shows alternating ±2% changes every few candles without a strong direction (whipsaw region).
# 	•	Your entry was positioned early in the channel, and you’re waiting for clearer confirmation.

import requests
import os
import time
from dotenv import load_dotenv
from app.schema import SignalResponse
from app.get_rsi import update_signal_in_db, get_prev_rsi

load_dotenv()

BASE_URL = "https://api.taapi.io"
TAAPI_SECRET = os.getenv("TAAPI_IO_PRO")

memory_store = {}

def get_bulk_indicators(symbol, interval, exchange):
    url = f"{BASE_URL}/bulk"
    params = {"secret": TAAPI_SECRET}
    json_data = {
        "secret": TAAPI_SECRET,
        "construct": [
            {
                "exchange": exchange,
                "symbol": symbol,
                "interval": interval,
                "indicators": [
                    {"indicator": "rsi", "params": {"period": 14}},
                    {"indicator": "ema", "params": {"period": 9}},
                    {"indicator": "ema", "params": {"period": 21}},
                    {"indicator": "price"}
                ]
            }
        ]
    }

    response = requests.post(url, params=params, json=json_data)

    if response.status_code == 200:
        data = response.json().get("data", [])
        if len(data) >= 4:
            rsi = data[0]["result"]["value"]
            ema_9 = data[1]["result"]["value"]
            ema_21 = data[2]["result"]["value"]
            price = data[3]["result"]["value"]
            return rsi, ema_9, ema_21, price
    else:
        print("Bulk API Error:", response.status_code, response.text)

    return None, None, None, None





def get_signal_data(symbol, interval, exchange):
    prev_rsi, last_signal, updated_at = get_prev_rsi(symbol, interval, exchange)
    rsi, ema_9, ema_21, price = get_bulk_indicators(symbol, interval, exchange)

    if None in (rsi, ema_9, ema_21, price):
 
        return None
    
    print({
        "rsi": rsi,
        "prev_rsi": prev_rsi,
        "ema_9": ema_9,
        "ema_21": ema_21,
        "price": price
    })

    return {
        "rsi": rsi,
        "prev_rsi": prev_rsi,
        "ema_9": ema_9,
        "ema_21": ema_21,
        "price": price,
        "last_signal" : last_signal,
        "previous_signal_at": updated_at
    }

def check_buy_signal(data):
    rsi = data["rsi"]
    prev_rsi = data["prev_rsi"]
    price = data["price"]
    ema = data["ema_9"]

    return (
        40 < rsi < 50 and
        prev_rsi is not None and 35 < prev_rsi <= 45 and
        abs(price - ema) / ema <= 0.002 and
        data["ema_9"] >= data["ema_21"]
    )

def check_sell_signal(data):
    rsi = data["rsi"]
    prev_rsi = data["prev_rsi"]
    price = data["price"]
    ema = data["ema_9"]

    return (
        50 < rsi < 60 and
        prev_rsi is not None and 60 <= prev_rsi <= 70 and
        abs(price - ema) / ema <= 0.002 and
        data["ema_9"] <= data["ema_21"]
    )

def check_exit_signal(data):
    rsi = data["rsi"]
    prev_rsi = data["prev_rsi"]
    price = data["price"]
    ema = data["ema_9"]

    return (
        45 <= rsi <= 55 and
        prev_rsi is not None and abs(rsi - prev_rsi) <= 1.0 and
        abs(price - ema) / ema <= 0.002
    )


def check_hold(data):
    rsi = data["rsi"]
    prev_rsi = data["prev_rsi"]
    ema_slope_flat = abs(data["ema_9"] - data["ema_21"]) / data["ema_21"] < 0.002

    return (
        45 <= rsi <= 55 and
        prev_rsi is not None and abs(rsi - prev_rsi) <= 2.0 and
        ema_slope_flat
    )


def process_signal(symbol, interval, exchange):
    data = get_signal_data(symbol, interval, exchange)

    print("*" * 50)
    print(data)
    print("*" * 50)

    if not data:
        print("Error fetching indicator data.")
        return SignalResponse(signal="error", rsi=0.0, ema=0.0)

    signal = ""

    # Signal checks with debug logs
    if check_buy_signal(data):
        signal = "buy"
        print("[DEBUG] Buy signal triggered")
    elif check_sell_signal(data):
        signal = "sell"
        print("[DEBUG] Sell signal triggered")
    elif check_exit_signal(data):
        signal = "exit"
        print("[DEBUG] Exit signal triggered")
    elif check_hold(data):
        signal = "hold"
        print("[DEBUG] Hold signal triggered")
    else:
        print("[DEBUG] No actionable signal at this time.")
        signal = ""

    # ✅ Save latest RSI and signal
    if signal in ("buy", "sell", "exit", "hold"):
        update_signal_in_db(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            prev_rsi=data["rsi"],
            last_signal=signal
        )

    return SignalResponse(
        signal=signal,
        rsi=round(data["rsi"], 2),
        ema=round(data["ema_9"], 2),
        last_signal=data.get("last_signal", ""),
        updated_at=data["previous_signal_at"]
    )
