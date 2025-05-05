import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get candles from your own source
candles = [
    {
        "open": 100,
        "high": 105,
        "low": 99,
        "close": 104,
        "volume": 250
    },
    {
        "open": 104,
        "high": 106,
        "low": 103,
        "close": 105,
        "volume": 300
    },
    {
        "open": 105,
        "high": 107,
        "low": 104,
        "close": 106,
        "volume": 320
    }
]


# Define indicator
indicator = "rsi"

# Define endpoint
endpoint = f"https://api.taapi.io/{indicator}"

# Parameters to be sent to API
parameters = {
    'secret': os.getenv("TAAPI_IO"),
    'candles': candles
}

# Send post request and save response as response object
response = requests.post(url = endpoint, json = parameters)

# Extract data in json format
result = response.json()

# Print result
print(result)