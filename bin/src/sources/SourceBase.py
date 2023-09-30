from abc import ABC, abstractproperty, abstractstaticmethod
from enums.Granularity import Granularity
from enums.Source import Source
from models.Candle import Candle
from models.Ticker import Ticker
from typing import List


class SourceBase(ABC):


    @abstractproperty
    def _SOURCE(self) -> Source:
        """
        Unique identifier for the class, associating it with the Source enum.
        """
        raise NotImplementedError


    @abstractstaticmethod
    def get_tickers() -> List[Ticker]:
        """
        Function for downloading the available tickers for the given source.

        Returns
        -------
        List[Ticker] - a list of Ticker objects representing the available tickers for the given source
        """
        raise NotImplementedError


    @abstractstaticmethod
    def get_ticker_history(self, ticker: str, granularity: Granularity, startDateTime: str, endDateTime: str) -> List[Candle]:
        """
        Function for downloading the desired history of a given ticker at the given granularity for the given source.

        Parameters
        ----------
        ticker : str
            Ticker to download history for.
        granularity : Granularity
            Time granularity of the candles.
        startDateTime : str
            Start of the timeframe in which the candles will be within.
        endDateTime : str
            End (exclusive) of the timeframe in which the candles will be within.

        Returns
        -------
        List[Candle] - a list of Candle objects representing the queried data
        """
        raise NotImplementedError
