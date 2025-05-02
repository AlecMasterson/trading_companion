from argparse import ArgumentParser
from datetime import datetime, timedelta
from enums.Granularity import Granularity
from models.db.Candle import Candle
from models.db.Ticker import Ticker
from services.polygon import get_ticker_candle_history
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlmodel import Session, select
from typing import List
from utils import LOGGER
from utils.database import get_database_session
from utils.date_util import get_now_eastern, to_string

_database_session: Session = next(get_database_session())

def get_tickers() -> List[str]:
    tickers: List[Ticker] = _database_session.exec(select(Ticker)).all()
    return [ticker.ticker for ticker in tickers]

def update_ticker(ticker: str, start_date: str, end_date: str) -> bool:
    try:
        update_ticker_granularity(ticker, Granularity.HOUR, start_date, end_date)
        update_ticker_granularity(ticker, Granularity.DAY, start_date, end_date)

        LOGGER.info(f"ticker={ticker} success=true")
        return True
    except:
        LOGGER.exception(f"ticker={ticker} success=false")
        return False

def update_ticker_granularity(ticker: str, granularity: Granularity, start_date: str, end_date: str) -> None:
    candles: List[Candle] = get_ticker_candle_history(ticker, granularity, start_date, end_date)
    candles_dict: List[dict] = [candle.model_dump() for candle in candles]
    LOGGER.info(f"ticker={ticker} granularity={granularity} candles.length={len(candles_dict)}")
    if len(candles_dict) == 0:
        LOGGER.warning(f"ticker={ticker} granularity={granularity} candles.length={len(candles_dict)}")
        return

    _database_session.exec(db_insert(Candle).values(candles_dict).on_conflict_do_nothing())
    _database_session.commit()

def main(total_days_in_past: int = 1) -> None:
    today: datetime = get_now_eastern()
    start_date: str = to_string(today - timedelta(days=total_days_in_past), format="%Y-%m-%d")
    # TODO: Check at 8pm+ on a weekday if this can get todays results without a delayed issue.
    end_date: str = to_string(today - timedelta(days=1), format="%Y-%m-%d")
    LOGGER.info(f"start_date={start_date} end_date={end_date}")

    tickers: List[str] = get_tickers()
    LOGGER.info(f"tickers.length={len(tickers)}")

    failed: List[str] = [ticker for ticker in tickers if not update_ticker(ticker, start_date, end_date)]
    if len(failed) > 0:
        raise Exception(f"failed={failed}")

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-d", default=1, type=int)
    total_days_in_past: int = parser.parse_args().d

    main(total_days_in_past)
