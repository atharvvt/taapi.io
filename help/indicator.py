# Import the requests library 
import requests 
import os
from dotenv import load_dotenv

load_dotenv()
# Define indicator
indicator = "rsi"
  
# Define endpoint 
endpoint = f"https://api.taapi.io/{indicator}"
  
# Define a parameters dict for the parameters to be sent to the API 
parameters = {
    'secret': os.getenv('TAAPI_IO'),
    'exchange': 'binance',
    'symbol': 'ETH/USDT',
    'interval': '1h'
    } 
  
# Send get request and save the response as response object 
response = requests.get(url = endpoint, params = parameters)
  
# Extract data in json format 
result = response.json() 

# Print result
print(result)