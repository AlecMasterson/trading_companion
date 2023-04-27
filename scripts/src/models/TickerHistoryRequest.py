from dataclasses import dataclass
from enums.Granularity import Granularity
from enums.Source import Source


@dataclass
class TickerHistoryRequest:
    source: Source
    ticker: str
    granularity: Granularity
    startDateTime: str
    endDateTime: str
