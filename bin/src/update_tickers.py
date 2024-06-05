from dataclasses import asdict
from models.Ticker import Ticker
from psycopg import Connection, Cursor
from typing import List
from utils import LOGGER
from utils.decorators import database_connection
from utils.polygon import get_ticker_market_cap, get_tickers


__SQL_INSERT = """
INSERT INTO stocks.ticker
(ticker, name, exchange, type, market_cap, active, valid)
VALUES (%(ticker)s, %(name)s, %(exchange)s, %(type)s, %(market_cap)s, %(active)s, %(valid)s)
ON CONFLICT (ticker) DO UPDATE SET
name = EXCLUDED.name,
exchange = EXCLUDED.exchange,
type = EXCLUDED.type,
market_cap = EXCLUDED.market_cap,
active = EXCLUDED.active,
valid = EXCLUDED.valid;
"""

__SQL_UPDATE_MARKET_CAP = """
UPDATE stocks.ticker
SET market_cap = %(market_cap)s
WHERE ticker = %(ticker)s;
"""


@database_connection
def main(database_conn: Connection = None) -> None:
    tickers: List[Ticker] = get_tickers()
    LOGGER.info(f"Total Tickers - {len(tickers)}")

    cursor: Cursor = database_conn.cursor()
    cursor.executemany(__SQL_INSERT, [asdict(i) for i in tickers])
    database_conn.commit()

    for ticker in tickers:
        market_cap: float = get_ticker_market_cap(ticker.ticker)
        LOGGER.info(f"ticker={ticker.ticker}, market_cap={market_cap}")

        database_conn.execute(__SQL_UPDATE_MARKET_CAP, {"market_cap": market_cap, "ticker": ticker.ticker})
        database_conn.commit()


if __name__ == "__main__":
    main()
