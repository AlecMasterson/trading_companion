from enums.Granularity import Granularity
from models.Candle import Candle
from models.Ticker import Ticker
from utils.decorators import rate_limit
from utils.requests_util import exchange
from typing import Any, Generator, List, Optional, Union
import os


__ENDPOINT_HISTORY: str = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?adjusted=true"
__ENDPOINT_TICKERS: str = "https://api.polygon.io/v3/reference/tickers"
__KEYS: List[str] = os.environ["POLYGON_KEYS"]


@rate_limit(limit=(len(__KEYS) * 5), sec=60)
def __get(url: str, headers: dict = {}, params: dict = {}) -> Any:
    return exchange(url, "GET", headers=headers, params=params)


def get_results(base_url: str, headers: dict = {}, params: dict = {}) -> Generator[Union[dict, List[dict]], None, None]:
    key_index: int = 0
    temp_params: dict = {
        **params,
        "apiKey": __KEYS[key_index]
    }

    url: Optional[str] = f"{base_url}"
    while url is not None:
        if "cursor" in url:
            temp_params = {}
            url = f"{url}&apiKey={__KEYS[key_index]}"

        response: dict = __get(url, headers=headers, params=temp_params)
        if response["status"] != "OK":
            raise Exception(f"[POLYGON] - Status not OK - {response['status']}")

        key_index = 0 if key_index == len(__KEYS) - 1 else key_index + 1
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


def get_ticker_market_cap(ticker: str) -> float:
    params: dict = {
        "apiKey": os.environ["POLYGON_KEY"]
    }
    url: str = __ENDPOINT_TICKERS + f"/{ticker}"

    response: List[dict] = [i for i in get_results(url, params=params)]
    assert len(response) == 1, f"More than 1 Response - ticker={ticker}, size={len(response)}"

    return response[0]["market_cap"] if "market_cap" in response[0] else 0


def get_tickers() -> List[Ticker]:
    exchanges: List[str] = ["XNAS", "XNYS"]
    params: dict = {
        "market": "stocks",
        "type": "CS"
    }
    url: str = __ENDPOINT_TICKERS

    def to_ticker(entry: dict) -> Ticker:
        return Ticker(
            active=False,
            exchange=entry["primary_exchange"],
            market_cap=0,
            name=entry["name"],
            ticker=entry["ticker"],
            type=entry["type"],
            valid=entry["active"]
        )

    response: List[Ticker] = []
    for exchange in exchanges:
        for results in get_results(url, params={**params, "exchange": exchange}):
            response += [to_ticker(i) for i in results]

    return response
