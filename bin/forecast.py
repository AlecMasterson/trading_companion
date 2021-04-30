from model.Argument import Argument, get_args
from model.Forecast import Forecast
from model.Interval import Interval, get_seconds
from model.Source import Source
from util import get_db_session, Logger
from util.util import get_candles, get_tickers, try_catch_loop
import datetime
import pandas


def forecast(source: Source, ticker: str, interval: Interval) -> Forecast:
    candles = get_candles(source, ticker, interval)
    candles.sort_values(by=["TIMESTAMP"], ascending=True, inplace=True)

    time_delta = datetime.timedelta(0, get_seconds(interval))
    forecast_timestamp = candles["TIMESTAMP"].iloc[-1] + time_delta

    # TODO: Make Complex Prediction
    price = candles["CLOSE"].iloc[0]

    Logger.info(f"Forecast for {ticker} on Interval {interval} = {price}")
    return Forecast(
        ticker=ticker,
        interval=interval,
        timestamp=forecast_timestamp,
        lower_price=price * 0.98,
        price=price,
        upper_price=price * 1.02,
    )


if __name__ == "__main__":
    args = require_args([Argument.SOURCE, Argument.INTERVAL])
    session = get_db_session()

    valid = True
    for ticker in get_tickers(args.SOURCE):
        try:
            session.add(forecast(args.SOURCE, ticker, args.INTERVAL))
        except Exception:
            valid = False

    session.commit()
    assert valid
