from analysis.preprocess import add_model_inputs, get_model, prepare_data
from keras.models import Model
from models.ModelConfig import ModelConfig
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from typing import List, Tuple
import importlib
import json
import numpy
import pandas

preprocess = importlib.import_module("analysis.preprocess")


DATASETS = [
    "COINBASE/DAY_1/ADA-USD",
    "COINBASE/DAY_1/BTC-USD",
    "COINBASE/DAY_1/DOGE-USD",
    "COINBASE/DAY_1/ETH-USD",
    "COINBASE/DAY_1/LTC-USD"
]
FILE_MODEL_CONFIG = "next_price_v1"


with open(f"data/models/configs/{FILE_MODEL_CONFIG}.json", "r") as file:
    MODEL_CONFIG: ModelConfig = ModelConfig(**json.load(file))


def get_datasets() -> List[numpy.ndarray]:
    data: List[numpy.ndarray] = []

    for dataset in DATASETS:
        df: pandas.DataFrame = pandas.read_csv(f"data/history/{dataset}.csv")
        data.append(prepare_data(MODEL_CONFIG, df))

    minSize: int = min([df.shape[0] for df in data])
    data: List[numpy.ndarray] = [df[(-1 * minSize):, :] for df in data]

    lengths: List[Tuple[int. int]] = [df.shape for df in data]
    assert all(length[0] == lengths[0][0] and length[1] == lengths[0][1] for length in lengths)

    return data


def get_XY(data: pandas.DataFrame) -> Tuple[numpy.ndarray, numpy.ndarray]:
    X: numpy.ndarray = getattr(preprocess, MODEL_CONFIG.func_S)(data.values)
    Y: numpy.ndarray = getattr(preprocess, MODEL_CONFIG.func_Y)(data)

    return X, Y


def train_model(model: Model, data: pandas.DataFrame) -> None:
    X, Y = get_XY(data)

    data_train_X, data_test_X, data_train_Y, data_test_Y = train_test_split(X, Y, test_size=0.3, shuffle=False)

    model.fit(x=data_train_X, y=data_train_Y, validation_data=(data_test_X, data_test_Y), verbose=1, **MODEL_CONFIG.model)


if __name__ == "__main__":
    data: List[Tuple[numpy.ndarray, numpy.ndarray]] = get_datasets()
    model: Model = get_model(MODEL_CONFIG.func_M, data[0])

    for df in data[:-1]:
        train_model(model, df)

    model.save(f"data/models/{FILE_MODEL_CONFIG}.h5")

    X, Y = get_XY(data[-1])
    pred = model.predict(X)

    # print(classification_report(Y, numpy.round(pred)))
    print(mean_absolute_error(Y, pred))
    print(mean_squared_error(Y, pred))
