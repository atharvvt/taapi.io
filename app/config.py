import os
from dotenv import load_dotenv

load_dotenv()

TAAPI_SECRET = os.getenv("TAAPI_SECRET")
BASE_URL = "https://api.taapi.io"