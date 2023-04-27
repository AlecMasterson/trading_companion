from dataclasses import dataclass
from enums.Model import Model
from models.Candle import Candle
from typing import List


@dataclass
class ModelRequest:
    model: Model
    candles: List[Candle]
