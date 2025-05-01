from enums.TickerType import TickerType
from models.db.Ticker import Ticker
from services.polygon import get_tickers
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlmodel import Session
from typing import List
from utils import LOGGER
from utils.database import get_database_session

def update(database_session: Session) -> None:
    tickers: List[Ticker] = get_tickers()
    tickers_dict: List[dict] = [ticker.model_dump() for ticker in tickers if ticker.type != TickerType.OTHER]
    LOGGER.info(f"tickers.length={len(tickers)}")

    database_session.exec(db_insert(Ticker).values(tickers_dict).on_conflict_do_nothing())
    database_session.commit()

if __name__ == "__main__":
    database_session: Session = next(get_database_session())

    update(database_session)
