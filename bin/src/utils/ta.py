from enums.Indicator import Indicator
from models.EnrichedCandle import EnrichedCandle
from models.IndicatorConfig import IndicatorConfig
from models.IndicatorEntry import IndicatorEntry
from numpy.typing import NDArray
from typing import List, Optional, Tuple
import numpy
import talib

def __convert_to_float(value: numpy.float64) -> Optional[float]:
    return None if numpy.isnan(value) else float(value)

def __parse_results(indicator_config: IndicatorConfig, candles: List[EnrichedCandle], results: NDArray[numpy.float64]) -> None:
    for index, candle in enumerate(candles):
        data: List[Optional[float]] = [__convert_to_float(results[index])]
        candle.indicators.append(IndicatorEntry(data=data, id=indicator_config.id, indicator=indicator_config.indicator))

def __parse_results_tuple(indicator_config: IndicatorConfig, candles: List[EnrichedCandle], results: Tuple[NDArray[numpy.float64], ...]) -> None:
    data: List[List[Optional[float]]] = [[__convert_to_float(value) for value in list(values)] for values in zip(*results)]
    for index, candle in enumerate(candles):
        candle.indicators.append(IndicatorEntry(data=data[index], id=indicator_config.id, indicator=indicator_config.indicator))

def _ema(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    args: dict = {}
    if indicator_config.period is not None:
        args["timeperiod"] = indicator_config.period

    results: NDArray[numpy.float64] = talib.EMA(numpy.array([candle.close for candle in candles]), **args)
    __parse_results(indicator_config, candles, results)

def _macd(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    args: dict = {}
    if indicator_config.period_fast is not None:
        args["fastperiod"] = indicator_config.period_fast
    if indicator_config.period_signal is not None:
        args["signalperiod"] = indicator_config.period_signal
    if indicator_config.period_slow is not None:
        args["slowperiod"] = indicator_config.period_slow

    results: Tuple[NDArray[numpy.float64], ...] = talib.MACD(numpy.array([candle.close for candle in candles]), **args)
    __parse_results_tuple(indicator_config, candles, results)

def _rsi(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    args: dict = {}
    if indicator_config.period is not None:
        args["timeperiod"] = indicator_config.period

    results: NDArray[numpy.float64] = talib.RSI(numpy.array([candle.close for candle in candles]), **args)
    __parse_results(indicator_config, candles, results)

def _sma(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    args: dict = {}
    if indicator_config.period is not None:
        args["timeperiod"] = indicator_config.period

    results: NDArray[numpy.float64] = talib.SMA(numpy.array([candle.close for candle in candles]), **args)
    __parse_results(indicator_config, candles, results)

def _stoch(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    args: dict = {} # TODO: add parameters for STOCH

    close: NDArray[numpy.float64] = numpy.array([candle.close for candle in candles])
    high: NDArray[numpy.float64] = numpy.array([candle.high for candle in candles])
    low: NDArray[numpy.float64] = numpy.array([candle.low for candle in candles])

    results: Tuple[NDArray[numpy.float64], ...] = talib.STOCH(high, low, close, **args)
    __parse_results_tuple(indicator_config, candles, results)

def apply_indicator(indicator_config: IndicatorConfig, candles: List[EnrichedCandle]) -> None:
    match indicator_config.indicator:
        case Indicator.EMA:
            _ema(indicator_config, candles)
        case Indicator.MACD:
            _macd(indicator_config, candles)
        case Indicator.RSI:
            _rsi(indicator_config, candles)
        case Indicator.SMA:
            _sma(indicator_config, candles)
        case Indicator.STOCH:
            _stoch(indicator_config, candles)
        case _:
            raise NotImplementedError
