import requests
import os
from dotenv import load_dotenv

load_dotenv()

indicator = 'irs' #can try diff indicators

url = "https://api.taapi.io/candles" 
url1 = "https://api.taapi.io/candle" 
url2 = f"https://api.taapi.io/{indicator}" 

params = {
    "secret": os.getenv("TAAPI_IO"),
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1h",
    "chart": "heikinashi"
}

response = requests.get(url, params=params)
data = response.json()
print("RSI (Heikin Ashi):", data)
