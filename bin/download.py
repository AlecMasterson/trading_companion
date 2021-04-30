from model.Argument import Argument, get_args
from model.Interval import Interval
from util.util import get_candles
from util.util_files import to_csv
import pandas


if __name__ == "__main__":
    args = get_args([Argument.SOURCE, Argument.TICKER])

    func = lambda interval: get_candles(args.SOURCE, args.TICKER, interval)
    data = pandas.concat([func(interval) for interval in Interval])

    to_csv(str(args.SOURCE).lower(), args.TICKER, data)
