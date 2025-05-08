from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.strategy3 import process_signal  # ensure this is imported

app = FastAPI()

load_dotenv()
memory_store = {}

BASE_URL = "https://api.taapi.io"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/monitor_buy_signal")
def monitor_buy(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})
    if signal_data.signal == "buy":
        return {"status": signal_data.signal, "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}


@app.get("/monitor_sell_signal")
def monitor_sell(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})

    if signal_data.signal == "sell":
        return {"status": signal_data.signal, "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}


@app.get("/monitor_exit_signal")
def monitor_exit(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": "Failed to fetch indicators"
            }
        )

    # Only respond if an exit signal is generated
    if signal_data.signal in ("exit-long", "exit-short", "exit"):
        return {
            "status": signal_data.signal,  # status is "exit-long" or "exit-short"
            "rsi": signal_data.rsi,
            "exchange": exchange,
            "symbol": symbol,
            "interval": interval,
            "last_signal": signal_data.last_signal,
            "previous_signal_at": signal_data.updated_at
        }

    # If no exit condition, return hold/empty status
    return {
        "status": "",
        "rsi": signal_data.rsi,
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval,
        "last_signal": signal_data.last_signal,
        "previous_signal_at": signal_data.updated_at
    }


@app.get("/monitor_hold_signal")
def monitor_buy(symbol: str = "BTC/USDT", interval: str = "5m", exchange: str = "binance"):
    signal_data = process_signal(symbol, interval, exchange)

    if signal_data.signal == "error":
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Failed to fetch indicators"})
    if signal_data.signal == "hold":
        return {"status": signal_data.signal, "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}
    return {"status": "", "rsi": signal_data.rsi, "exchange": exchange, "symbol": symbol, "interval":interval, "last_signal":signal_data.last_signal, "previous_signal_at": signal_data.updated_at}
