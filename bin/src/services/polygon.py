from enums.Granularity import Granularity
from enums.Source import Source
from enums.TickerType import TickerType
from enums.polygon.PolygonTickerType import PolygonTickerType
from models.db.Candle import Candle
from models.db.News import News
from models.db.Ticker import Ticker
from models.polygon.PolygonCandle import PolygonCandle
from models.polygon.PolygonNews import PolygonNews
from models.polygon.PolygonResponse import PolygonResponse
from models.polygon.PolygonTicker import PolygonTicker
from utils import LOGGER
from utils.date_util import from_datetime_str, from_timestamp
from utils.decorators import RateLimit
from utils.requests_util import exchange
from typing import Any, Callable, List, Optional
import os
import re

_BASE_URL = "https://api.polygon.io"
_GRANULARITY_POLYGON_MAP = {
    Granularity.HOUR: "hour",
    Granularity.DAY: "day"
}
_KEYS: List[str] = [os.environ[key] for key in os.environ if re.compile(r"^POLYGON_KEY_(\d+)$").match(key)]
_VALID_TICKER_TYPES: List[PolygonTickerType] = [PolygonTickerType.CS, PolygonTickerType.ETF]

KEY_INDEX: int = 0

@RateLimit(limit=(len(_KEYS) * 5), seconds=65)
def _get(base_url: str) -> PolygonResponse:
    global KEY_INDEX

    url: str = f"{base_url}"
    if "cursor" in url:
        params = {}
        url += f"&apiKey={_KEYS[KEY_INDEX]}"
    else:
        params = {"apiKey": _KEYS[KEY_INDEX]}

    response: Any = exchange(url, "GET", params=params)
    KEY_INDEX = 0 if KEY_INDEX == len(_KEYS) - 1 else KEY_INDEX + 1

    return PolygonResponse(**response)

def _get_results(path: str, mapping_func: Callable[..., Any], *args: Any) -> List[Any]:
    results: List[Any] = []
    url: Optional[str] = f"{_BASE_URL}{path}"

    while url is not None:
        response: PolygonResponse = _get(url)
        url: Optional[str] = response.next_url

        if response.status == "OK":
            results += [mapping_func(item, *args) for item in response.results]
        else:
            LOGGER.warning(f"Invalid Status - {response.status}")

    return results

def _to_candle(entry_raw: Any, ticker: str, granularity: Granularity) -> Candle:
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

def _to_news(entry_raw: Any) -> News:
    entry: PolygonNews = PolygonNews(**entry_raw)

    return News(
        snippet=entry.description,
        timestamp=from_datetime_str(entry.published_utc, "%Y-%m-%dT%H:%M:%SZ"),
        title=entry.title,
        url=entry.article_url
    )

def _to_ticker(entry_raw: Any) -> Ticker:
    entry: PolygonTicker = PolygonTicker(**entry_raw)

    ticker_type_polygon: PolygonTickerType = PolygonTickerType(entry.type)
    ticker_type: TickerType = TickerType(ticker_type_polygon.value)

    return Ticker(
        name=entry.name,
        ticker=entry.ticker,
        type=ticker_type
    )

def get_news(date: str) -> List[News]:
    return _get_results(f"/v2/reference/news?published_utc={date}", _to_news)

def get_ticker_candle_history(ticker: str, granularity: Granularity, start_date: str, end_date: str) -> List[Candle]:
    granularity_str: str = _GRANULARITY_POLYGON_MAP[granularity]
    return _get_results(
        f"/v2/aggs/ticker/{ticker}/range/1/{granularity_str}/{start_date}/{end_date}?adjusted=true",
        _to_candle,
        ticker,
        granularity
    )

def get_tickers() -> List[Ticker]:
    response: List[Ticker] = _get_results("/v3/reference/tickers?active=true&market=stocks", _to_ticker)
    return list({getattr(ticker, "ticker"): ticker for ticker in response}.values())
