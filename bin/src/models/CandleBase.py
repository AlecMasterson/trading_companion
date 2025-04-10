from datetime import datetime
from enums.Granularity import Granularity
from pydantic import BaseModel

class CandleBase(BaseModel):
    close: float
    granularity: Granularity
    high: float
    low: float
    open: float
    ticker: str
    timestamp: datetime
    volume: float
