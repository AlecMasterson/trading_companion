from dataclasses import dataclass


@dataclass
class Ticker:
    id: str
    label: str
    currencyAlt: str
    currencyBase: str
