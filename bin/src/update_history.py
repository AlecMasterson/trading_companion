from dataclasses import asdict
from datetime import datetime, timedelta
from enums.Granularity import Granularity
from models.Candle import Candle
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import Executable
from typing import List
from utils import LOGGER
from utils.date_util import get_now, to_string
from utils.polygon import get_ticker_candle_history
import json
import os


engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:5432/trading_companion")
SessionLocal = sessionmaker(bind=engine)
database_session: Session = SessionLocal()


if __name__ == "__main__":
    today: datetime = get_now()
    start_date: str = to_string(today - timedelta(days=10), format="%Y-%m-%d")
    end_date: str = to_string(today, format="%Y-%m-%d")
    LOGGER.info(f"start_date={start_date} end_date={end_date}")

    with open("./data/s&p500.json", "r") as file:
        tickers: List[str] = json.load(file)

    failed: List[str] = []
    for ticker in tickers:
        try:
            candles_hour: List[Candle] = get_ticker_candle_history(ticker, Granularity.HOUR, start_date, end_date)
            LOGGER.info(f"ticker={ticker} candles_hour={len(candles_hour)}")

            if len(candles_hour) > 0:
                statement: Executable = db_insert(Candle).values([asdict(candle) for candle in candles_hour]).on_conflict_do_nothing()
                database_session.execute(statement)
                database_session.commit()

            candles_day: List[Candle] = get_ticker_candle_history(ticker, Granularity.DAY, start_date, end_date)
            LOGGER.info(f"ticker={ticker} candles_day={len(candles_day)}")

            if len(candles_day) > 0:
                statement: Executable = db_insert(Candle).values([asdict(candle) for candle in candles_day]).on_conflict_do_nothing()
                database_session.execute(statement)
                database_session.commit()

            LOGGER.info(f"ticker={ticker} success=true")
        except:
            LOGGER.exception(f"ticker={ticker} success=false")
            failed.append(ticker)

    if len(failed) > 0:
        raise Exception(f"failed={failed}")
