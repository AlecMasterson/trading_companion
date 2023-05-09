from keras.models import Model
from models.ModelConfig import ModelConfig
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import importlib
import json
import numpy
import pandas

preprocess = importlib.import_module("analysis.preprocess")


FILE_CANDLE_DATA = "COINBASE/DAY_1/BTC-USD"
FILE_MODEL_CONFIG = "chance_increasing_v1"


if __name__ == "__main__":
    with open(f"data/models/configs/{FILE_MODEL_CONFIG}.json", "r") as file:
        MODEL_CONFIG: ModelConfig = ModelConfig(**json.load(file))

    data: pandas.DataFrame = pandas.read_csv(f"data/{FILE_CANDLE_DATA}.csv")
    data: pandas.DataFrame = data[MODEL_CONFIG.candle_data]

    getattr(preprocess, "add_ta_indicators")(MODEL_CONFIG.ta, data)

    Y: numpy.ndarray = getattr(preprocess, MODEL_CONFIG.func_Y)(data)
    X: numpy.ndarray = getattr(preprocess, MODEL_CONFIG.func_S)(data.values)

    data_train_X, data_test_X, data_train_Y, data_test_Y = train_test_split(X, Y, test_size=0.3, shuffle=False)
    model: Model = getattr(preprocess, MODEL_CONFIG.func_M)(data_train_X)

    model.fit(x=data_train_X, y=data_train_Y, validation_data=(data_test_X, data_test_Y), **MODEL_CONFIG.model)
    model.save(f"data/models/{FILE_MODEL_CONFIG}.h5")

    print(classification_report(data_test_Y, model.predict(data_test_X)))
