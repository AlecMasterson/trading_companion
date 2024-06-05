from dataclasses import asdict
from models.Ticker import Ticker
from psycopg import Connection, Cursor
from typing import List
from utils import LOGGER
from utils.decorators import database_connection
from utils.polygon import get_tickers
import os

os.environ["POLYGON_KEY"] = "yVhJ0Ync8LiK1p3iR2bEGJ9jZB1Rkdv53lgmQO"
os.environ["POSTGRES_DB"] = "trading_companion"
os.environ["POSTGRES_PASSWORD"] = "password123"
os.environ["POSTGRES_PORT"] = "5499"
os.environ["POSTGRES_USER"] = "ep_senex"


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

SQL_SELECT_TICKERS = """
SELECT ticker FROM stocks.ticker
"""

SQL_UPDATE_MARKET_CAP = """
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


if __name__ == "__main__":
    main()
