from enums.Signal import Signal
from models.CandleBase import CandleBase
from models.IndicatorEntry import IndicatorEntry
from pydantic import Field
from typing import List

class EnrichedCandle(CandleBase):
    indicators: List[IndicatorEntry] = Field(default=[])
    signals: List[Signal] = Field(default=[])
