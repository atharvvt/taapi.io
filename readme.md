```bash
| Endpoint     | Description                           |
| ------------ | ------------------------------------- |
| `rsi`        | Relative Strength Index               |
| `macd`       | Moving Average Convergence Divergence |
| `ema`        | Exponential Moving Average            |
| `sma`        | Simple Moving Average                 |
| `adx`        | Average Directional Index             |
| `bbands`     | Bollinger Bands                       |
| `stoch`      | Stochastic Oscillator                 |
| `candle`     | OHLCV (Open/High/Low/Close/Volume)    |
| `fib`        | Fibonacci levels                      |
| `ichimoku`   | Ichimoku Cloud components             |
| `supertrend` | Supertrend trend-following indicator  |
| `heikinashi` | Heikin Ashi candles                   |
| `atr`        | Average True Range                    |

```


# 🔄 Bulk and Batch APIs #
## TAAPI.IO also supports bulk requests, allowing you to query multiple indicators or multiple symbols in a single call using ##
```bash
/bulk
/batch
```

## These are ideal for minimizing API requests in trading bots or dashboards. ##


# 🛡️ Authentication #
- Every request must include your API secret. 
- API keys are usually tied to a pricing tier (free, pro, etc.), which limits access to features or request rates.


# 📘 TAAPI.IO API Types – Explained Simply

TAAPI.IO offers multiple ways to calculate technical indicators. Here’s a simple breakdown of each method and when to use them.

---

## 📡 [GET] REST – Direct

### What it does:
TAAPI.IO fetches **live or historical price data** from supported exchanges (e.g., Binance, Coinbase, US Stocks) and calculates the indicator for you.

### ✅ Use When:
You want to get **real-time indicators** without providing your own data.

### 🧪 Example:
Get the RSI for BTC/USDT on Binance with one request.

### 📌 Pros:
- Super simple to use.
- No need to collect your own candles.
- Great for real-time or live dashboards.

---

## 📦 [POST] Bulk

### What it does:
Fetch **multiple indicators in one request** for a specific asset.

### ✅ Use When:
You need to evaluate several indicators (e.g., RSI, MACD, EMA200) for the same symbol at once.

### 🧪 Example:
You want RSI, MACD, and EMA200 for ETH/USDT on the 1-hour chart.

### 📌 Pros:
- Saves time and bandwidth.
- Clean and efficient for trading bots or dashboards.

---

## 📝 [POST] REST – Manual (BYOC)

### What it does:
Send your **own candle data** to TAAPI.IO and it will calculate the indicator using that data.

### ✅ Use When:
- You have data from an exchange TAAPI.IO doesn’t support.
- You want to backtest.
- You want to chain indicators (e.g., RSI of EMA50, EMA of RSI).

### 🧪 Example:
Send your own list of OHLCV candles and ask TAAPI.IO to return RSI values.

### 📌 Pros:
- Very flexible.
- Works with any data you provide.
- Allows advanced custom setups.

---

## 🧰 3rd Party Utilities

### What it does:
TAAPI.IO offers **plugins, integrations, and tools** for platforms like Google Sheets, MetaTrader, TradingView, etc.

### ✅ Use When:
You don’t want to code or want to quickly add TAAPI.IO to an existing tool.

### 🧪 Example:
Use TAAPI.IO Google Sheets add-on to auto-calculate RSI from within a spreadsheet.

### 📌 Pros:
- Easy for non-coders.
- Fast setup for analysts and traders.

---

## ⚡ Summary Table

| API Type              | You Provide Data? | TAAPI.IO Fetches Data? | Use When…                             |
|-----------------------|-------------------|-------------------------|----------------------------------------|
| GET REST – Direct     | ❌                | ✅                      | You want quick data from live exchanges |
| POST Bulk             | ❌                | ✅                      | You want many indicators at once       |
| POST REST – Manual    | ✅                | ❌                      | You have your own data (BYOC)          |
| 3rd Party Utilities   | ❌ / ✅           | ✅ / ❌                 | You prefer tools or don’t want to code |

