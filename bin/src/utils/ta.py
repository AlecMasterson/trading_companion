from enums.Indicator import Indicator
from models.Candle import Candle
from models.IndicatorCandle import IndicatorCandle
from models.IndicatorRequest import IndicatorRequest
from numpy.typing import NDArray
from typing import List, Optional, Tuple
import numpy
import talib


def __convert_to_float(value: numpy.float64) -> Optional[float]:
    return None if numpy.isnan(value) else float(value)


def __parse_results(candles: List[Candle], results: NDArray[numpy.float64]) -> List[IndicatorCandle]:
    response: List[IndicatorCandle] = []

    for index, candle in enumerate(candles):
        response.append(IndicatorCandle(timestamp=candle.timestamp, values=[__convert_to_float(results[index])]))

    return response


def __parse_results_tuple(candles: List[Candle], results: Tuple[NDArray[numpy.float64], ...]) -> List[IndicatorCandle]:
    data: List[List[float]] = [[__convert_to_float(value) for value in list(result)] for result in zip(*results)]
    response: List[IndicatorCandle] = []

    for index, candle in enumerate(candles):
        response.append(IndicatorCandle(timestamp=candle.timestamp, values=data[index]))

    return response


def _ema(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    args: dict = {}
    if request.period is not None:
        args["timeperiod"] = request.period

    results: NDArray[numpy.float64] = talib.EMA(numpy.array([candle.close for candle in candles]), **args)
    return __parse_results(candles, results)


def _macd(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    args: dict = {}
    if request.period_fast in request:
        args["fastperiod"] = request.period_fast
    if request.period_signal in request:
        args["signalperiod"] = request.period_signal
    if request.period_slow in request:
        args["slowperiod"] = request.period_slow

    results: Tuple[NDArray[numpy.float64], ...] = talib.MACD(numpy.array([candle.close for candle in candles]), **args)
    return __parse_results_tuple(candles, results)


def _rsi(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    args: dict = {}
    if request.period is not None:
        args["timeperiod"] = request.period

    results: NDArray[numpy.float64] = talib.RSI(numpy.array([candle.close for candle in candles]), **args)
    return __parse_results(candles, results)



def _sma(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    args: dict = {}
    if request.period is not None:
        args["timeperiod"] = request.period

    results: NDArray[numpy.float64] = talib.SMA(numpy.array([candle.close for candle in candles]), **args)
    return __parse_results(candles, results)


def _stoch(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    args: dict = {} # TODO: add parameters for STOCH

    close: NDArray[numpy.float64] = numpy.array([candle.close for candle in candles])
    high: NDArray[numpy.float64] = numpy.array([candle.high for candle in candles])
    low: NDArray[numpy.float64] = numpy.array([candle.low for candle in candles])

    results: Tuple[NDArray[numpy.float64], ...] = talib.STOCH(high, low, close, **args)
    return __parse_results_tuple(candles, results)


def get_indicator_values(request: IndicatorRequest, candles: List[Candle]) -> List[IndicatorCandle]:
    candles_sorted: List[Candle] = sorted(candles, key=lambda candle: candle.timestamp)

    match request.indicator:
        case Indicator.EMA:
            return _ema(request, candles_sorted)
        case Indicator.MACD:
            return _macd(request, candles_sorted)
        case Indicator.RSI:
            return _rsi(request, candles_sorted)
        case Indicator.SMA:
            return _sma(request, candles_sorted)
        case Indicator.STOCH:
            return _stoch(request, candles_sorted)
        case _:
            raise NotImplementedError
