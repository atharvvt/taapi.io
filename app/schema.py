from pydantic import BaseModel

class SignalResponse(BaseModel):
    signal: str
    rsi: float
    ema: float