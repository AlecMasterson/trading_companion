from dataclasses import dataclass


@dataclass
class Candle:
    close: float
    granularity: str
    high: float
    low: float
    open: float
    ticker: str
    timestamp: str
    volume: float
