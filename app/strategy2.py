import requests
import os
import time
from dotenv import load_dotenv
from app.schema import SignalResponse
from app.get_rsi import update_signal_in_db, get_prev_rsi
# _____________________________
# Buy, Sell and Exit Strategy 

# TAAPI.IO APIs used in the RSI-based crypto trading strategy:

# 	1.	RSI – for detecting overbought or oversold conditions
# 	2.	EMA (Exponential Moving Average) – for trend confirmation
# 	3.	Price – for retrieving the current or latest candle price
# ______________________________
# 1. Buy when RSI(14) crosses above 30 and EMA(9) crosses above EMA(21).
# 2. Sell when RSI(14) crosses below 70 and EMA(9) crosses below EMA(21).
# 3. Exit longs if RSI goes above 70 and reverses, or if EMA(9) drops below EMA(21).
# 4. Exit shorts if RSI goes below 30 and reverses, or if EMA(9) rises above EMA(21).
# ______________________________

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
    return (
        data["rsi"] > 30
        and data["prev_rsi"] is not None
        and data["prev_rsi"] <= 30
        and data["ema_9"] > data["ema_21"]
    )

def check_sell_signal(data):
    return (
        data["rsi"] < 70
        and data["prev_rsi"] is not None
        and data["prev_rsi"] >= 70
        and data["ema_9"] < data["ema_21"]
    )

def check_exit_long(data):
    return (
        (data["prev_rsi"] is not None and data["prev_rsi"] > 70 and data["rsi"] < data["prev_rsi"])
        or (data["ema_9"] < data["ema_21"])
    )

def check_exit_short(data):
    return (
        (data["prev_rsi"] is not None and data["prev_rsi"] < 30 and data["rsi"] > data["prev_rsi"])
        or (data["ema_9"] > data["ema_21"])
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
        print("[DEBUG] Buy signal triggered: RSI crossed above 30 and EMA(9) > EMA(21)")
    elif check_sell_signal(data):
        signal = "sell"
        print("[DEBUG] Sell signal triggered: RSI crossed below 70 and EMA(9) < EMA(21)")
    elif check_exit_long(data):
        signal = "exit-long"
        print("[DEBUG] Exit-long signal triggered: RSI reversed from >70 or EMA(9) < EMA(21)")
    elif check_exit_short(data):
        signal = "exit-short"
        print("[DEBUG] Exit-short signal triggered: RSI reversed from <30 or EMA(9) > EMA(21)")
    else:
        print("[DEBUG] No actionable signal at this time.")
        signal = ""

    # ✅ Save latest RSI and signal
    if signal in ("buy", "sell", "exit-long", "exit-short"):
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
