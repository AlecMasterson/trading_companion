from dataclasses import dataclass


@dataclass
class Ticker:
    active: bool
    exchange: str
    market_cap: str
    name: str
    ticker: str
    type: str
    valid: bool
