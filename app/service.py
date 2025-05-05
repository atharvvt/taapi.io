import requests
import os
import time
from dotenv import load_dotenv
from app.schema import SignalResponse
from app.get_rsi import update_signal_in_db, get_prev_rsi

load_dotenv()

BASE_URL = "https://api.taapi.io"
TAAPI_SECRET = os.getenv("TAAPI_IO")

memory_store = {}

def get_rsi(symbol, interval, exchange):
    url = f"{BASE_URL}/rsi"
    params = {
        "secret": TAAPI_SECRET,
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval
    }
    response = requests.get(url, params=params)
    print("-"*50)
    print("rsi_response",response.status_code, response.text)
    print("-"*50)
    if response.status_code == 200:
        return response.json().get("value")
    print("RSI API Error:", response.status_code, response.text)
    return None


def get_ema(period, symbol, interval, exchange):
    url = f"{BASE_URL}/ema"
    params = {
        "secret": TAAPI_SECRET,
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval,
        "period": period
    }
    response = requests.get(url, params=params)
    print("-"*50)
    print("ema_response",response.status_code, response.text)
    print("-"*50)
    if response.status_code == 200:
        return response.json().get("value")
    print("EMA API Error:", response.status_code, response.text)
    return None


def get_price(symbol, interval, exchange):
    url = f"{BASE_URL}/candle"
    params = {
        "secret": TAAPI_SECRET,
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval,
        "chart": "heikinashi"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Heikin Ashi Candle:", data)
        return data.get("close")
    print("Price API Error:", response.status_code, response.text)
    return None


def generate_signal(period, symbol, interval, exchange):
    prev_rsi, last_signal = get_prev_rsi(symbol, interval, exchange)

    ema = get_ema(period, symbol, interval, exchange)
    time.sleep(15)
    rsi = get_rsi(symbol, interval, exchange)
    time.sleep(15)
    current_price = get_price(symbol, interval, exchange)

    if rsi is None or ema is None or current_price is None:
        return SignalResponse(signal="error", rsi=0.0, ema=0.0)

    signal = "hold"

    if prev_rsi is not None:
        if prev_rsi < 25 and 25 < rsi < 30 and current_price > ema:
            signal = "buy"
        elif prev_rsi > 75 and 70 < rsi < 75 and current_price < ema:
            signal = "sell"

    update_signal_in_db(symbol, interval, exchange, rsi, signal)
    return SignalResponse(signal=signal, rsi=round(rsi, 2), ema=round(ema, 2))