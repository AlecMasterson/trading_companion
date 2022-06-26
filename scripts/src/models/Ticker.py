from dataclasses import dataclass

@dataclass
class Ticker:
    id: str
    currencyAlt: str
    currencyBase: str
    label: str
