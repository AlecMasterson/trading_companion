from dataclasses import dataclass
from models.Candle import Candle
from typing import List


@dataclass
class IndicatorRequest:
    candles: List[Candle]
