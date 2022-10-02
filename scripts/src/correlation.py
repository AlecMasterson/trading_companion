from ta import momentum, trend, volatility
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy
import os
import pandas

NUM_DAYS = 4

def prepare_data(data: pandas.DataFrame) -> numpy.array:
    data.sort_values(by="candle_timestamp", inplace=True)
    data.drop(["data_source", "ticker", "granularity", "candle_timestamp", "interpolated"], axis=1, inplace=True)

    data: numpy.array = data.to_numpy()[0::NUM_DAYS]
    data: numpy.array = numpy.append(data, [[i] for i in numpy.append(data[:,0][1:] - data[:,0][:-1], 0)], axis=1)

    data["momentum_RSI"] = momentum.RSIIndicator(close=data[:,0]).rsi()
    data["momentum_TSI"] = momentum.TSIIndicator(close=data[:,0]).tsi()
    data["trend_EMA"] = trend.EMAIndicator(close=data[:,0]).ema_indicator()

    trendMACD = trend.MACD(close=data[:,0])
    data["trend_MACD"] = trendMACD.macd()
    data["trend_MACD_diff"] = trendMACD.macd_diff()

    data["volatility_BBands"] = volatility.BollingerBands(close=data[:,0]).bollinger_mavg()

    return data.to_numpy()[37:]


def read_file(fileName: str) -> pandas.DataFrame:
    return pandas.read_csv(f"data/COINBASE/DAY_1/{fileName}")


if __name__ == "__main__":
    data = [prepare_data(read_file(file)) for file in os.listdir("data/COINBASE/DAY_1")]
    data = numpy.concatenate(data, axis=0)
    numpy.random.shuffle(data)

    model = Sequential()
    model.add(Dense(11, input_shape=(11,), activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(8, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    print("Fitting Model...")
    print(data.shape)
    X = data[:,0:11]
    Y = data[:,11]

    model.fit(X, Y, epochs=50, batch_size=20)
    _, accuracy = model.evaluate(X, Y)
    print(f"Accuracy: {accuracy * 100}")
