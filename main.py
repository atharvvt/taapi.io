import requests 
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import time
from app.service import generate_signal

app = FastAPI()

load_dotenv()
memory_store = {}

BASE_URL = "https://api.taapi.io"

@app.get("/")
def home():
    return {"status" : "ok", "message" : "add /docs at end of url"}

@app.get("/generate_signal")
def analyze(period=50, symbol="BTC/USDT", interval="5m", exchange="binance"):
    return generate_signal(period, symbol, interval, exchange)
