from enums.Granularity import Granularity
from models.Candle import Candle
from models.PolygonResponse import PolygonCandle, PolygonResponse
from utils.date_util import from_timestamp
from utils.decorators import RateLimit
from utils.requests_util import exchange
from typing import Any, Generator, List, Optional
import os


__ENDPOINT_TICKER_CANDLE_HISTORY: str = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{granularity}/{start_date}/{end_date}?adjusted=true"
__GRANULARITY_POLYGON_MAP = {
    Granularity.HOUR: "hour",
    Granularity.DAY: "day"
}
__KEYS: List[str] = os.environ["POLYGON_KEYS"].split(",")

KEY_INDEX: int = 0


@RateLimit(limit=(len(__KEYS) * 5), seconds=60)
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
        url = response.next_url

        if response.status != "OK" and response.status != "DELAYED":
            raise Exception(f"Invalid Status - {response.status}")

        yield response.results


def get_ticker_candle_history(ticker: str, granularity: Granularity, start_date: str, end_date: str) -> List[Candle]:
    def to_candle(entry_raw: Any) -> Candle:
        entry: PolygonCandle = PolygonCandle(**entry_raw)

        return Candle(
            close=entry.c,
            granularity=granularity,
            high=entry.h,
            low=entry.l,
            open=entry.o,
            ticker=ticker,
            timestamp=from_timestamp(entry.t),
            volume=entry.v
        )

    path_params: dict = {
        "end_date": end_date,
        "granularity": __GRANULARITY_POLYGON_MAP[granularity],
        "start_date": start_date,
        "ticker": ticker
    }
    url: str = __ENDPOINT_TICKER_CANDLE_HISTORY.format(**path_params)

    response: List[Candle] = []
    for results in __get_results(url):
        response += [to_candle(i) for i in results]

    return response
