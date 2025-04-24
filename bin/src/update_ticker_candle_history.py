from datetime import datetime, timedelta
from enums.Granularity import Granularity
from models.db.Candle import Candle
from models.db.Ticker import Ticker
from services.polygon import get_ticker_candle_history
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlalchemy.sql import Executable
from sqlmodel import Session, select
from typing import List
from utils import LOGGER
from utils.database import get_database_session
from utils.date_util import get_now_eastern, to_string

def insert_candles(database_session: Session, candles: List[Candle]) -> None:
    if len(candles) == 0:
        return

    candles_dict: List[dict] = [candle.model_dump() for candle in candles]
    statement: Executable = db_insert(Candle).values(candles_dict).on_conflict_do_nothing()

    database_session.execute(statement)
    database_session.commit()

def update_granularity(
        database_session: Session, ticker: str, granularity: Granularity, start_date: str, end_date: str) -> None:
    candles: List[Candle] = get_ticker_candle_history(ticker, granularity, start_date, end_date)
    LOGGER.info(f"ticker={ticker} granularity={granularity} candles.length={len(candles)}")
    insert_candles(database_session, candles)
    LOGGER.info(f"ticker={ticker} granularity={granularity} success=true")

def main() -> None:
    database_session: Session = next(get_database_session())

    today: datetime = get_now_eastern()
    start_date: str = to_string(today - timedelta(days=5), format="%Y-%m-%d")
    # TODO: Check at 8pm+ on a weekday if this can get todays results without a delayed issue.
    end_date: str = to_string(today - timedelta(days=1), format="%Y-%m-%d")
    LOGGER.info(f"start_date={start_date} end_date={end_date}")

    tickers: List[Ticker] = database_session.exec(select(Ticker)).all()
    tickers: List[str] = [ticker.ticker for ticker in tickers]
    LOGGER.info(f"tickers.length={len(tickers)}")

    failed: List[str] = []
    for ticker in tickers:
        try:
            update_granularity(database_session, ticker, Granularity.HOUR, start_date, end_date)
            update_granularity(database_session, ticker, Granularity.DAY, start_date, end_date)
            LOGGER.info(f"ticker={ticker} success=true")
        except:
            LOGGER.exception(f"ticker={ticker} success=false")
            failed.append(ticker)

    if len(failed) > 0:
        raise Exception(f"failed={failed}")

if __name__ == "__main__":
    main()
