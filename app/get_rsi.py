from supabase_client import supabase

def update_signal_in_db(symbol: str, exchange: str, interval: str, prev_rsi: float, last_signal: str):
    """Insert or update signal in the Supabase database."""
    existing = supabase.table("signals") \
        .select("*") \
        .eq("symbol", symbol) \
        .eq("exchange", exchange) \
        .eq("interval", interval) \
        .limit(1) \
        .execute()

    if existing.data:
        supabase.table("signals").update({
            "prev_rsi": prev_rsi,
            "last_signal": last_signal,
            "updated_at": "now()"
        }).eq("symbol", symbol) \
          .eq("exchange", exchange) \
          .eq("interval", interval) \
          .execute()
    else:
        supabase.table("signals").insert({
            "symbol": symbol,
            "exchange": exchange,
            "interval": interval,
            "prev_rsi": prev_rsi,
            "last_signal": last_signal
        }).execute()

def get_prev_rsi(symbol: str, interval: str, exchange: str):
    """Fetch previous RSI and last signal from Supabase."""
    response = supabase.table("signals") \
        .select("prev_rsi", "last_signal", "updated_at") \
        .eq("symbol", symbol) \
        .eq("interval", interval) \
        .eq("exchange", exchange) \
        .limit(1) \
        .execute()

    if response.data and len(response.data) > 0:
        data = response.data[0]
        return data.get("prev_rsi"), data.get("last_signal"), data.get("updated_at")

    return None, None , None


