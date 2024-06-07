from dataclasses import asdict
from datetime import datetime, timedelta
from models.Candle import Candle
from psycopg import Connection, Cursor
from typing import List
from utils import LOGGER
from utils.decorators import database_connection
from utils.polygon import get_history


__SQL_INSERT = """
INSERT INTO stocks.history
(ticker, timestamp, granularity, high, low, open, close, volume)
VALUES (%(ticker)s, %(timestamp)s, %(granularity)s, %(high)s, %(low)s, %(open)s, %(close)s, %(volume)s)
ON CONFLICT (ticker, timestamp, granularity) DO UPDATE SET
high = EXCLUDED.high,
low = EXCLUDED.low,
open = EXCLUDED.open,
close = EXCLUDED.close,
volume = EXCLUDED.volume;
"""

__SQL_SELECT_TICKERS = """
select ticker from stocks.ticker where active = true;
"""


@database_connection
def main(database_conn: Connection = None) -> None:
    end_date: str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    LOGGER.info(f"end_date={end_date}")

    tickers: List[tuple] = database_conn.execute(__SQL_SELECT_TICKERS).fetchall()
    tickers: List[str] = [ticker[0] for ticker in tickers]
    LOGGER.info(f"tickers.length={len(tickers)}")

    cursor: Cursor = database_conn.cursor()
    for ticker in tickers:
        history: List[Candle] = get_history(ticker, "DAY", "2020-01-01", end_date)
        LOGGER.info(f"ticker={ticker}, history.length={len(history)}")

        cursor.executemany(__SQL_INSERT, [asdict(i) for i in history])
        database_conn.commit()


if __name__ == "__main__":
    main()
