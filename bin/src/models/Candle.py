from dataclasses import dataclass
from enums.Granularity import Granularity
from enums.Source import Source


@dataclass
class Candle:
    data_source: Source
    ticker: str
    granularity: Granularity
    candle_timestamp: int
    interpolated: bool
    price_close: float
    price_high: float
    price_low: float
    price_open: float
    volume: float
