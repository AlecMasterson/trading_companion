from dataclasses import dataclass

@dataclass
class Candle:
    data_source: str
    ticker: str
    granularity: int
    candle_timestamp: int
    interpolated: bool
    price_close: float
    price_high: float
    price_low: float
    price_open: float
    volume: float
