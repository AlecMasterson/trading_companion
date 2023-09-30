from keras.models import load_model, Model, Sequential
from keras.layers import concatenate, Conv1D, Dense, Input, LSTM
from models.ModelConfig import ModelConfig, TAConfig
from sklearn.preprocessing import MinMaxScaler
from ta.momentum import rsi, stoch
from ta.trend import adx, ema_indicator, macd, macd_diff
from typing import Any, List, Tuple
import json
import numpy
import pandas


def predict(modelName: str, data: pandas.DataFrame) -> numpy.ndarray:
    with open(f"data/models/configs/{modelName}.json", "r") as file:
        config: ModelConfig = ModelConfig(**json.load(file))
        model: Model = load_model(f"data/models/{modelName}.h5")

        X, _ = prepare_data(config, data)
        return model.predict(X)


def prepare_data(config: ModelConfig, df: pandas.DataFrame) -> numpy.ndarray:
    data: pandas.DataFrame = df.copy()
    globalVars: dict[str, Any] = globals()

    for modelInput in config.model_inputs:
        data.insert(len(data.columns), modelInput, [1.0] * len(data))

    # Filter DataFrame to only include pre-determine and model_input columns.
    data: pandas.DataFrame = data[config.candle_data + config.model_inputs]

    for taConfig in [TAConfig(**x) for x in config.ta]:
        params: dict = taConfig.config

        for col in taConfig.candle_data:
            params[col] = data[col]

        data[taConfig.name] = globalVars[f"ta_{taConfig.func}"](**params)

    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    assert not data.isnull().values.any()

    # Add the Y value as the last column in the DataFrame.
    data.insert(len(data.columns), "__Y__", globalVars[config.func_Y](data))

    # Scale the data and return the separated X and Y segments.
    return globalVars[config.func_S](data.values)
    # return values[:, :-1], values[:, -1:]


def add_model_inputs(config: List[dict[str, str]], data: pandas.DataFrame) -> None:
    for modelConfig in config:

        with open(f"data/models/configs/{modelConfig['model']}.json", "r") as file:
            config: ModelConfig = ModelConfig(**json.load(file))

        model: Model = load_model(modelConfig["model"])
        model.predict
        # TODO: train modelConfig["model"]


def get_model(func: str, data: pandas.DataFrame) -> Model:
    globalVars: dict[str, Any] = globals()

    shape: numpy.ndarray = numpy.empty((round(len(data[0]) * 0.7), len(data[0].columns)))
    return getattr(globalVars, func)(shape)


# ----------------------------
# Data Models
# ----------------------------


def M1(data: numpy.ndarray):
    model: Model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=10, activation="relu", input_shape=(data.shape[1], 1)))
    model.add(Dense(units=10))
    model.add(LSTM(30, activation="relu", input_shape=(data.shape[1], 1)))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model

def M2(data: numpy.ndarray):
    model: Model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=10, activation="relu", input_shape=(data.shape[1], 1)))
    model.add(Dense(units=10))
    model.add(LSTM(15, activation="relu", input_shape=(data.shape[1], 1)))
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])

    return model


# ----------------------------
# Data Scalers
# ----------------------------


def S1(data: numpy.ndarray) -> numpy.ndarray:
    scaler: MinMaxScaler = MinMaxScaler()
    return scaler.fit_transform(data)


# ----------------------------
# Y-Axis
# ----------------------------


def Y1(data: pandas.DataFrame) -> numpy.array:
    return numpy.array([1.0 if any(y > x for y in data["price_close"][i+1:i+4]) else 0.0 for i, x in enumerate(data["price_close"])])

def Y2(data: pandas.DataFrame) -> numpy.array:
    return numpy.array([1.0 if any(y / x >= 1.01 for y in data["price_close"][i+1:i+4]) else 0.0 for i, x in enumerate(data["price_close"])])

def Y3(data: pandas.DataFrame) -> numpy.array:
    return data["price_close"].shift(-1).values


# ----------------------------
# TA Indicators
# ----------------------------


def ta_adx(price_high: List[float], price_low: List[float], price_close: List[float], window: int = 14) -> List[float]:
    return adx(price_high, price_low, price_close, window=window)

def ta_ema(price_close: List[float], window: int = 12) -> List[float]:
    return ema_indicator(price_close, window=window)

def ta_ema_diff(price_close: List[float], window_fast: int = 12, window_slow: int = 26) -> List[float]:
    fast: List[float] = ema_indicator(price_close, window=window_fast)
    slow: List[float] = ema_indicator(price_close, window=window_slow)

    return fast - slow

def ta_macd(price_close: List[float], window_slow: int = 26, window_fast: int = 12) -> List[float]:
    return macd(price_close, window_slow=window_slow, window_fast=window_fast)

def ta_macd_diff(price_close: List[float], window_slow: int = 26, window_fast: int = 12, window_sign: int = 9) -> List[float]:
    return macd_diff(price_close, window_slow=window_slow, window_fast=window_fast, window_sign=window_sign)

def ta_rsi(price_close: List[float], window: int = 14) -> List[float]:
    return rsi(price_close, window=window)

def ta_stoch(price_high: List[float], price_low: List[float], price_close: List[float], window: int = 14, smooth_window: int = 3) -> List[float]:
   return stoch(price_high, price_low, price_close, window=window, smooth_window=smooth_window)
