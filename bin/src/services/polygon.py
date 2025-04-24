from enums.Granularity import Granularity
from enums.Source import Source
from enums.TickerType import TickerType
from enums.polygon.PolygonTickerType import PolygonTickerType
from models.db.Candle import Candle
from models.db.Ticker import Ticker
from models.polygon.PolygonCandle import PolygonCandle
from models.polygon.PolygonResponse import PolygonResponse
from models.polygon.PolygonTicker import PolygonTicker
from utils import LOGGER
from utils.date_util import from_timestamp
from utils.decorators import RateLimit
from utils.requests_util import exchange
from typing import Any, Generator, List, Optional
import os
import re

__GRANULARITY_POLYGON_MAP = {
    Granularity.HOUR: "hour",
    Granularity.DAY: "day"
}
__KEYS: List[str] = [os.environ[key] for key in os.environ if re.compile(r"^POLYGON_KEY_(\d+)$").match(key)]
__VALID_TICKER_TYPES: List[PolygonTickerType] = [PolygonTickerType.CS, PolygonTickerType.ETF]

KEY_INDEX: int = 0

@RateLimit(limit=(len(__KEYS) * 5), seconds=65)
def __get(base_url: str) -> PolygonResponse:
    global KEY_INDEX

    url: str = f"{base_url}"
    if "cursor" in url:
        params = {}
        url += f"&apiKey={__KEYS[KEY_INDEX]}"
    else:
        params = {"apiKey": __KEYS[KEY_INDEX]}

    response: Any = exchange(url, "GET", params=params)
    KEY_INDEX = 0 if KEY_INDEX == len(__KEYS) - 1 else KEY_INDEX + 1

    return PolygonResponse(**response)

def __get_results(base_url: str) -> Generator[List[Any], None, None]:
    url: Optional[str] = f"{base_url}"

    while url is not None:
        response: PolygonResponse = __get(url)
        url: Optional[str] = response.next_url

        if response.status == "OK":
            yield response.results
        else:
            LOGGER.warning(f"Invalid Status - {response.status}")
            yield []

def get_ticker_candle_history(ticker: str, granularity: Granularity, start_date: str, end_date: str) -> List[Candle]:
    def to_candle(entry_raw: Any) -> Candle:
        entry: PolygonCandle = PolygonCandle(**entry_raw)

        return Candle(
            close=entry.c,
            granularity=granularity,
            high=entry.h,
            low=entry.l,
            open=entry.o,
            source=Source.POLYGON,
            ticker=ticker,
            timestamp=from_timestamp(entry.t),
            volume=entry.v
        )

    url: str = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{__GRANULARITY_POLYGON_MAP[granularity]}/{start_date}/{end_date}?adjusted=true"

    response: List[Candle] = []
    for results in __get_results(url):
        response += [to_candle(i) for i in results]

    return response

def get_tickers() -> List[Ticker]:
    def to_ticker(entry_raw: Any) -> Optional[Ticker]:
        entry: PolygonTicker = PolygonTicker(**entry_raw)

        try:
            if entry.type is None:
                return None

            ticker_type_polygon: PolygonTickerType = PolygonTickerType(entry.type)
            if ticker_type_polygon not in __VALID_TICKER_TYPES:
                return None

            ticker_type: TickerType = TickerType(ticker_type_polygon.value)
        except ValueError:
            LOGGER.warning(f"Invalid TickerType={entry.type}")
            return None

        return Ticker(
            name=entry.name,
            ticker=entry.ticker,
            type=ticker_type
        )

    url: str = "https://api.polygon.io/v3/reference/tickers?active=true&market=stocks"

    response: List[Optional[Ticker]] = []
    for results in __get_results(url):
        response += [to_ticker(i) for i in results]

    response: List[Ticker] = [ticker for ticker in response if ticker is not None]
    return list({getattr(ticker, "ticker"): ticker for ticker in response}.values())
