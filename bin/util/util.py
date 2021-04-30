from model.Forecast import Forecast
from model.Interval import Interval
from model.Source import Source
from typing import Any, Callable, List
from util import API_BASE, Logger
import pandas
import requests


def get_candles(source: Source, ticker: str, interval: Interval, start: str = None) -> pandas.DataFrame:
    assert isinstance(source, Source) and isinstance(ticker, str) and isinstance(interval, Interval)

    candles = get("source/get/candles", {"source": source, "ticker": ticker, "interval": interval, "start": start})
    assert all([isinstance(i, dict) for i in candles])

    return pandas.DataFrame(candles)


def get_forecasts(source: Source, ticker: str) -> List[Forecast]:
    assert isinstance(source, Source) and isinstance(ticker, str)

    forecasts = get("forecast/get", {"source": source, "ticker": ticker})
    assert all([isinstance(i, dict) for i in forecasts])

    return [Forecast(forecast) for forecast in forecasts]


def get_tickers(source: Source) -> List[str]:
    assert isinstance(source, Source)

    tickers = get("source/get/tickers", {"source": source})
    assert all([isinstance(i, str) for i in tickers])

    return tickers


def get(endpoint: str, params: dict = None) -> List[Any]:
    response = requests.get(API_BASE + endpoint, params=params)
    if not response.ok:
        raise Exception(response.reason)

    items = response.json()
    assert isinstance(items, List)

    return items


def try_catch_loop(items: List[Any], func: Callable[[Any], None]) -> bool:
    valid = True
    for item in items:
        try:
            func(item)
        except Exception as e:
            Logger.exception(e)
            valid = False

    return valid
