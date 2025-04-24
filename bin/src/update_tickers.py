from models.db.Ticker import Ticker
from services.polygon import get_tickers
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlalchemy.sql import Executable
from sqlmodel import Session
from typing import List
from utils import LOGGER
from utils.database import get_database_session

def main() -> None:
    database_session: Session = next(get_database_session())

    tickers: List[Ticker] = get_tickers()
    LOGGER.info(f"tickers.length={len(tickers)}")
    if len(tickers) == 0:
        return

    tickers_dict: List[dict] = [ticker.model_dump() for ticker in tickers]
    statement: Executable = db_insert(Ticker).values(tickers_dict).on_conflict_do_nothing()

    database_session.execute(statement)
    database_session.commit()

if __name__ == "__main__":
    main()
