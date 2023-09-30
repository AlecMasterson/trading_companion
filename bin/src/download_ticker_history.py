from argparse import ArgumentParser
from enums.Granularity import Granularity
from enums.Source import Source
from models.Candle import Candle
from sources.Coinbase import Coinbase
from typing import List
from utils import LOGGER
import os
import pandas

SOURCE_MAP = {
    Source.COINBASE: Coinbase
}

def export(source: Source, granularity: Granularity, ticker: str, history: List[Candle]) -> None:
    path = f"data/history/{source.name}/{granularity.name}"
    os.makedirs(path, exist_ok=True)

    pandas.DataFrame(history).to_csv(f"{path}/{ticker}.csv", index=False)


def main(source: Source, granularity: Granularity) -> None:
    LOGGER.info(f"source: {source}, granularity: {granularity}")

    ticker: str = "ADA-USD"
    history: List[Candle] = SOURCE_MAP[source].get_ticker_history(ticker, granularity, "2020-01-01 00:00:00", "2023-04-01 00:00:00")
    export(source, granularity, ticker, history)


if __name__ == "__main__":
    parser = ArgumentParser(description="for downloading historical data from the given data source at a given granularity")
    parser.add_argument("-s", dest="SOURCE", help="data source to download from", choices=list(Source), type=Source, required=True)
    parser.add_argument("-g", dest="GRANULARITY", help="time granularity of the candles", choices=list(Granularity), type=Granularity, required=True)
    args = parser.parse_args()

    main(args.SOURCE, args.GRANULARITY)
