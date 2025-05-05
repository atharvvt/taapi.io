import requests 
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import time
from app.service import generate_signal
from app.get_rsi import get_prev_rsi
from datetime import datetime
from fastapi.responses import HTMLResponse

app = FastAPI()

load_dotenv()
memory_store = {}

BASE_URL = "https://api.taapi.io"

@app.get("/")
def home():
    return {"status" : "ok", "message" : "add /docs at end of url"}

# @app.get("/generate_signal")
# def analyze(period=50, symbol="BTC/USDT", interval="5m", exchange="binance"):
#     return generate_signal(period, symbol, interval, exchange)


def format_signal_response(signal, rsi, exchange, symbol):
    # Get previous RSI and signal time from Supabase
    prev_rsi, last_signal = get_prev_rsi(symbol, "5m", exchange)
    
    # Formatted current time
    current_time_full = datetime.utcnow().strftime("%d%m%Y %H %M %S")
    readable_time = datetime.utcnow().strftime("%d %B %Y - %H:%M:%S UTC")

    if signal == "buy":
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
            <h2 style="color: green;">Buy Signal</h2>
            <p><strong>{readable_time}</strong></p>
            <p><strong>You can buy {symbol} now.</strong> The RSI is <strong>{rsi}</strong>.</p>
            <p>The previous buy signal was at <strong>{last_signal if last_signal != 'init' else 'N/A'}</strong>.</p>
            <p style="color: gray;">Note: Please consider other conditions too.</p>
            <hr/>
        </body>
        </html>
        """
    elif signal == "sell":
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
            <h2 style="color: red;">Sell Signal</h2>
            <p><strong>{readable_time}</strong></p>
            <p><strong>You can sell {symbol} now.</strong> The RSI is <strong>{rsi}</strong>.</p>
            <p>The previous sell signal was at <strong>{last_signal if last_signal != 'init' else 'N/A'}</strong>.</p>
            <p style="color: gray;">Note: Please consider other conditions too.</p>
            <hr/>
        </body>
        </html>
        """
    else:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
            <h2 style="color: orange;">Hold Signal</h2>
            <p><strong>{readable_time}</strong></p>
            <p>No actionable signal. Current RSI is <strong>{rsi}</strong>.</p>
            <p>Previous signal: <strong>{last_signal if last_signal != 'init' else 'N/A'}</strong>.</p>
            <p style="color: gray;">Note: Please consider other conditions too.</p>
            <hr/>
        </body>
        </html>
        """

    return HTMLResponse(content=html)




@app.get("/generate_signal_binance", response_class=HTMLResponse)
def generate_binance_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="binance")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "binance", "BTC/USDT")
    return signal_message


@app.get("/generate_signal_bybit", response_class=HTMLResponse)
def generate_bybit_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="bybit")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "bybit", "BTC/USDT")
    return signal_message


@app.get("/generate_signal_bitget", response_class=HTMLResponse)
def generate_bitget_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="bitget")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "bitget", "BTC/USDT")
    return signal_message


@app.get("/generate_signal_gateio", response_class=HTMLResponse)
def generate_gateio_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="gateio")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "gateio", "BTC/USDT")
    return signal_message


@app.get("/generate_signal_whitebit", response_class=HTMLResponse)
def generate_whitebit_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="whitebit")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "whitebit", "BTC/USDT")
    return signal_message
