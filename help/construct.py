import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


url = "https://api.taapi.io/bulk"
# more than 1 contruct requires advanced plans
payload = {
    "secret": os.getenv("TAAPI_IO"),
    "construct": [
		{
			"exchange": "binance",
			"symbol": "BTC/USDT",
			"interval": "1m",
			"indicators": [
				{
					"indicator": "rsi",
					"period": 14
				}
			]
		},
		{
			"exchange": "binance",
			"symbol": "BTC/USDT",
			"interval": "15m",
			"indicators": [
				{
					"indicator": "rsi",
					"period": 14
				}
			]
		},
		{
			"exchange": "binance",
			"symbol": "BTC/USDT",
			"interval": "1h",
			"indicators": [
				{
					"indicator": "rsi",
					"period": 14
				}
			]
		}
	]
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

pprint(response.text)