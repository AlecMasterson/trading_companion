from enums.Granularity import Granularity
from enums.Indicator import Indicator
from pydantic import BaseModel
from typing import Optional


class IndicatorRequest(BaseModel):
    granularity: Granularity
    indicator: Indicator
    period: Optional[int] = None
    period_fast: Optional[int] = None
    period_signal: Optional[int] = None
    period_slow: Optional[int] = None
    ticker: str
