from datetime import datetime
from enums.Granularity import Granularity
from enums.Source import Source
from pydantic import BaseModel

class CandleBase(BaseModel):
    close: float
    granularity: Granularity
    high: float
    low: float
    open: float
    source: Source
    ticker: str
    timestamp: datetime
    volume: float
