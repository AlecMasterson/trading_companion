from analysis.preprocess import preprocess, _apply_technical_indicators
from enums.Indicator import Indicator
from enums.Model import Model
from models.Candle import Candle
from tensorflow.keras.models import load_model
from typing import Any, List
from utils import LOGGER
import numpy
import pandas


__MODEL_MAP = {
    Model.CHANCE_INCREASING: load_model("src/analysis/models/increasing_v1.h5")
}


def fit_model(model: Model, candles: List[Candle]) -> List[dict]:
    data: numpy.ndarray = preprocess(candles)
    result: numpy.ndarray = __MODEL_MAP[model].predict(data)

    values: List[float] = [float(x[1]) for x in result]
    timestampValues: List[int] = [candle.candle_timestamp for candle in candles[(-1 * len(values)):]]

    return [{"candle_timestamp": timestamp, "value": value} for timestamp, value in zip(timestampValues, values)]



def get_indicators(candles: List[Candle]) -> List[dict]:
    data: pandas.DataFrame = _apply_technical_indicators(candles)
    data: List[dict] = data.to_dict("records")

    timestampValues: List[int] = [candle.candle_timestamp for candle in candles[(-1 * len(data)):]]

    return [{**row, "candle_timestamp": timestamp} for row, timestamp in zip(data, timestampValues)]
