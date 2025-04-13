from enums.Indicator import Indicator
from pydantic import BaseModel, Field
from typing import Optional

class IndicatorConfig(BaseModel):
    id: str
    indicator: Indicator
    period: Optional[int] = None
    period_fast: Optional[int] = Field(alias="periodFast", default=None)
    period_signal: Optional[int] = Field(alias="periodSignal", default=None)
    period_slow: Optional[int] = Field(alias="periodSlow", default=None)
    window_size: Optional[int] = Field(alias="windowSize", default=None)
