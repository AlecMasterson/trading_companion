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
__GRANULARITY_POLYGON_MAP = {
    Granularity.HOUR: "hour",
    Granularity.DAY: "day"
}
__KEYS: List[str] = [os.environ[key] for key in os.environ if re.compile(r"^POLYGON_KEY_(\d+)$").match(key)]
__VALID_TICKER_TYPES: List[PolygonTickerType] = [PolygonTickerType.CS, PolygonTickerType.ETF]

KEY_INDEX: int = 0

@RateLimit(limit=(len(__KEYS) * 5), seconds=65)
def _get(base_url: str) -> PolygonResponse:
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

def _get_results(path: str, mapping_func: Callable[[Any], Optional[Any]]) -> List[Any]:
    results: List[Any] = []
    url: Optional[str] = f"{_BASE_URL}{path}"

    while url is not None:
        response: PolygonResponse = _get(url)
        url: Optional[str] = response.next_url

        if response.status == "OK":
            results_opt: List[Optional[Any]] = [mapping_func(item) for item in response.results]
            results += [result for result in results_opt if result is not None]
        else:
            LOGGER.warning(f"Invalid Status - {response.status}")

    return results

def get_news(date: str) -> List[News]:
    def to_news(entry_raw: Any) -> Optional[News]:
        entry: PolygonNews = PolygonNews(**entry_raw)

        return News(
            snippet=entry.description,
            timestamp=from_datetime_str(entry.published_utc, "%Y-%m-%dT%H:%M:%SZ"),
            title=entry.title,
            url=entry.article_url
        )

    url: str = f"https://api.polygon.io/v2/reference/news?published_utc={date}"
    return _get_results(url, to_news)

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

    granularity_str: str = __GRANULARITY_POLYGON_MAP[granularity]
    return _get_results(f"/v2/aggs/ticker/{ticker}/range/1/{granularity_str}/{start_date}/{end_date}?adjusted=true", to_candle)

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

    response: List[Ticker] = _get_results("/v3/reference/tickers?active=true&market=stocks", to_ticker)
    return list({getattr(ticker, "ticker"): ticker for ticker in response}.values())
