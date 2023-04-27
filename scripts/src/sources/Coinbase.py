from datetime import datetime, timedelta
from enums.Granularity import Granularity
from enums.Source import Source
from models.Candle import Candle
from models.Ticker import Ticker
from sources.SourceBase import SourceBase
from typing import Any, List
from utils.decorators import rate_limit
from utils.requests_util import get


class Coinbase(SourceBase):

    _SOURCE = Source.COINBASE

    __ENDPOINT_HISTORY = "/products/{ticker}/candles"
    __ENDPOINT_TICKERS = "/products"
    __URL = "https://api.exchange.coinbase.com"


    @staticmethod
    @rate_limit(limit=10, sec=2)
    def get_tickers() -> List[Ticker]:
        def map_to_ticker(raw: dict) -> Ticker:
            return Ticker(id=raw["id"], currencyAlt=raw["quote_currency"], currencyBase=raw["base_currency"], label=raw["display_name"])

        data: List[dict] = get(Coinbase.__URL + Coinbase.__ENDPOINT_TICKERS)

        return [map_to_ticker(raw) for raw in data]


    @staticmethod
    @rate_limit(limit=10, sec=2)
    def get_ticker_history(ticker: str, granularity: Granularity, startDateTime: str, endDateTime: str) -> List[Candle]:
        candles: List[Candle] = []
        defaultCandleInfo: dict = {"data_source": Coinbase._SOURCE.name, "ticker": ticker, "granularity": granularity, "interpolated": False}
        url: str = Coinbase.__URL + Coinbase.__ENDPOINT_HISTORY.replace("{ticker}", ticker)

        def map_to_candle(raw: Any) -> Candle:
            candle: dict = dict(zip(["candle_timestamp", "price_low", "price_high", "price_open", "price_close", "volume"], raw))
            return Candle(**(defaultCandleInfo | candle))

        start: datetime = datetime.strptime(startDateTime, "%Y-%m-%d %H:%M:%S")
        end: datetime = datetime.strptime(endDateTime, "%Y-%m-%d %H:%M:%S")

        # Coinbase API limits each response to 300 candles, batching the requests avoids this issue.
        batches: int = int((end - start).total_seconds() // (granularity.get_seconds() * 300)) + 1
        startDateTimes: List[datetime] = [start + timedelta(seconds=(granularity.get_seconds() * 300 * i)) for i in range(batches)]

        for batchStart in startDateTimes:
            batchEnd: datetime = min(end, batchStart + timedelta(seconds=(granularity.get_seconds() * 300)))

            data: List[Any] = get(url, params={"granularity": granularity.get_seconds(), "start": str(batchStart), "end": str(batchEnd)})
            data: List[Candle] = [map_to_candle(raw) for raw in data][::-1]

            candles.extend(data)

        return candles
