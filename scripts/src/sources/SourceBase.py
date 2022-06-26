from abc import ABC, abstractmethod
from enums.Granularity import Granularity
from models.Candle import Candle
from models.Ticker import Ticker
from typing import List

class SourceBase(ABC):

    @abstractmethod
    def get_tickers() -> List[Ticker]:
        """
        Function for downloading the available tickers for the given source.

        Returns:
            List[Ticker] - a list of Ticker objects representing the available tickers for the given source
        """
        raise NotImplementedError


    @abstractmethod
    def download_ticker_history(self, ticker: str, granularity: Granularity) -> List[Candle]:
        """
        Function for downloading the history of a given ticker at the given granularity from the given source.

        Parameters:
            - ticker [str] - ticker to download history for
            - granularity [Granularity] - time granularity of the candles

        Returns:
            List[Candle] - a list of Candle objects representing the queried data
        """
        raise NotImplementedError
