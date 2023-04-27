from dataclasses import dataclass
from enums.Indicator import Indicator
from models.Candle import Candle
from typing import List


@dataclass
class IndicatorRequest:
    indicator: Indicator
    candles: List[Candle]
