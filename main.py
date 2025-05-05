import requests 
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import time
from app.strategy1 import generate_signal
from app.get_rsi import get_prev_rsi
from datetime import datetime
from fastapi.responses import HTMLResponse
from pytz import timezone, all_timezones
import pytz
from app.strategy2 import get_signal_data, check_buy_signal, check_sell_signal, check_exit_signal

app = FastAPI()

load_dotenv()
memory_store = {}

BASE_URL = "https://api.taapi.io"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from app.strategy2 import process_signal  # ensure this is imported

@app.get("/monitor_buy_signal")
def monitor_buy(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})

    if signal_data.signal == "buy":
        return {"status": "buy", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}


@app.get("/monitor_sell_signal")
def monitor_sell(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})

    if signal_data.signal == "sell":
        return {"status": "buy", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}


@app.get("/monitor_exit_signal")
def monitor_exit(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})

    if signal_data.signal in ("exit-long", "exit-short"):
        return {"status": "buy", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval}
