from pydantic import BaseModel
from datetime import datetime

class SignalResponse(BaseModel):
    signal: str
    rsi: float
    ema: float
    last_signal: str
    updated_at: datetime