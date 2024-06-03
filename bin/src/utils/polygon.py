from enums.Granularity import Granularity
from models.Candle import Candle
from utils.decorators import rate_limit
from utils.requests_util import exchange
from typing import Any, Generator, List, Optional, Union
import os


__ENDPOINT_HISTORY: str = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?adjusted=true"
__ENDPOINT_TICKERS: str = "https://api.polygon.io/v3/reference/tickers"


@rate_limit(limit=5, sec=60)
def __get(url: str, headers: dict = {}, params: dict = {}) -> Any:
    return exchange(url, "GET", headers=headers, params=params)


def get_results(base_url: str, headers: dict = {}, params: dict = {}) -> Generator[Union[dict, List[dict]], None, None]:
    apiKey: str = os.environ["POLYGON_KEY"]
    temp_params: dict = {
        **params,
        "apiKey": apiKey
    }

    url: Optional[str] = f"{base_url}"
    while url is not None:
        if "cursor" in url:
            temp_params = {}
            url = f"{url}&apiKey={apiKey}"

        response: dict = __get(url, headers=headers, params=temp_params)
        if response["status"] != "OK":
            raise Exception(f"[POLYGON] - Status not OK - {response['status']}")

        url = response["next_url"] if "next_url" in response else None
        yield response["results"]


def get_history(ticker: str, granularity: Granularity, start_date: str, end_date: str) -> List[Candle]:
    url: str = __ENDPOINT_HISTORY.replace("{ticker}", ticker).replace("{start}", start_date).replace("{end}", end_date)

    def to_candle(entry: dict) -> Candle:
        return Candle(
            granularity=granularity,
            price_close=entry["c"],
            price_high=entry["h"],
            price_low=entry["l"],
            price_open=entry["o"],
            ticker=ticker,
            timestamp=entry["t"],
            volume=entry["v"]
        )

    response: List[Candle] = []
    for results in get_results(url):
        response += [to_candle(i) for i in results]

    return response
