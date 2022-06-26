from enums.Granularity import Granularity
from enums.Source import Source
from models.Candle import Candle
from models.Ticker import Ticker
from sources.SourceBase import SourceBase
from typing import Any, List, Optional
from utils.decorators import rate_limit
from utils.requests_util import get

class Coinbase(SourceBase):

    _SOURCE = Source.COINBASE

    @staticmethod
    @rate_limit(limit=10, sec=2)
    def get_tickers() -> List[Ticker]:
        def map_to_ticker(raw: dict) -> Ticker:
            return Ticker(id=raw["id"], currencyAlt=raw["quote_currency"], currencyBase=raw["base_currency"], label=raw["display_name"])

        data: Optional[List[Ticker]] = get("https://api.exchange.coinbase.com/products")
        tickers: List[Ticker] = [map_to_ticker(raw) for raw in data] if data is not None else []

        return [ticker for ticker in tickers if ticker.currencyAlt == "USD"]


    @staticmethod
    @rate_limit(limit=10, sec=2)
    def download_ticker_history(ticker: str, granularity: Granularity) -> List[Candle]:
        defaultCandleInfo: dict = {"data_source": Coinbase._SOURCE.name, "ticker": ticker, "granularity": Granularity.get_seconds(granularity), "interpolated": False}

        def map_to_candle(raw: Any) -> Candle:
            candle: dict = dict(zip(["candle_timestamp", "price_low", "price_high", "price_open", "price_close", "volume"], raw))
            return Candle(**(defaultCandleInfo | candle))

        data: Optional[List[Any]] = get(f"https://api.exchange.coinbase.com/products/{ticker}/candles?granularity={Granularity.get_seconds(granularity)}")
        return [map_to_candle(raw) for raw in data] if data is not None else []
