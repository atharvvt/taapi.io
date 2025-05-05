import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


url = "https://api.taapi.io/bulk"

payload = {
    "secret": os.getenv("TAAPI_IO"),
    "construct": {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1h",
        "indicators": [
            {
                "indicator": "rsi"
            }, 
            {
                "indicator": "ema",
                "period": 20
            },
            {
                "indicator": "macd"
            }, 
            {
                "indicator": "kdj"
            },
            {
                "indicator": "dmi"
            }
        ]
    }
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

pprint(response.text)