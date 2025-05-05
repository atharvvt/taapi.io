from supabase_client import supabase

def update_signal_in_db(symbol, exchange, interval, prev_rsi, last_signal):

    
    # Check if entry exists
    existing = supabase.table("signals").select("*").eq("symbol", symbol).eq("exchange", exchange).eq("interval", interval).execute()
    
    if existing.data:
        supabase.table("signals").update({
            "prev_rsi": prev_rsi,
            "last_signal": last_signal
        }).eq("symbol", symbol).eq("exchange", exchange).eq("interval", interval).execute()
    else:
        supabase.table("signals").insert({
            "symbol": symbol,
            "exchange": exchange,
            "interval": interval,
            "prev_rsi": prev_rsi,
            "last_signal": last_signal
        }).execute()


def get_prev_rsi(symbol, interval, exchange):
    # query Supabase for the latest RSI and signal
    response = supabase.table("signals") \
        .select("prev_rsi", "last_signal") \
        .eq("symbol", symbol) \
        .eq("interval", interval) \
        .eq("exchange", exchange) \
        .limit(1) \
        .execute()

    if response.data and len(response.data) > 0:
        data = response.data[0]
        return data.get("prev_rsi"), data.get("last_signal")
    
    # Return None, "init" as defaults
    return None, "init"

