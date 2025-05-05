import requests 
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import time
from app.service import generate_signal
from app.get_rsi import get_prev_rsi
from datetime import datetime

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
    
    # Initialize response_message
    response_message = "init"  # Default to "init" if no valid signal
    
    # If the signal is "buy"
    if signal == "buy":
        response_message = f"""
        You can sell {symbol} now. The RSI is {rsi}.\n 
        The previous sell signal was at {last_signal if last_signal != 'init' else 'N/A'}.\n
        Note: Please consider other conditions too.
        """
    # If the signal is "sell"
    elif signal == "sell":
        response_message = f"""
        You can sell {symbol} now. The RSI is {rsi}.\n 
        The previous sell signal was at {last_signal if last_signal != 'init' else 'N/A'}.\n
        Note: Please consider other conditions too.
        """
    # If the signal is "hold"
    elif signal == "hold":
        response_message = f"""
        You can sell {symbol} now. The RSI is {rsi}.\n 
        The previous sell signal was at {last_signal if last_signal != 'init' else 'N/A'}.\n
        Note: Please consider other conditions too.
        """

    return response_message



@app.get("/generate_signal_binance")
def generate_binance_signal():
    signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="binance")
    signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "binance", "BTC/USDT")
    return {"message": signal_message}


# @app.get("/generate_signal_bybit")
# def generate_bybit_signal():
#     signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="bybit")
#     signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "bybit", "BTC/USDT")
#     return {"message": signal_message}


# @app.get("/generate_signal_bitget")
# def generate_bitget_signal():
#     signal_response = generate_signal(period=50, symbol="BTC/USDT", interval="5m", exchange="bitget")
#     signal_message = format_signal_response(signal_response.signal, signal_response.rsi, "bitget", "BTC/USDT")
#     return {"message": signal_message}