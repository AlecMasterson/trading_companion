from dataclasses import asdict
from datetime import datetime, timedelta
from models.Candle import Candle
from psycopg import Connection, Cursor
from typing import List
from utils import LOGGER
from utils.date_util import get_time_et, to_string
from utils.decorators import database_connection
from utils.polygon import get_history


__START_DATE: str = "2020-01-01"

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

__SQL_SELECT_HISTORY = """
SELECT ticker, timestamp FROM stocks.history
WHERE ticker = %(ticker)s AND granularity = %(granularity)s;
"""

__SQL_SELECT_TICKERS = """
SELECT ticker FROM stocks.ticker WHERE active = true;
"""


@database_connection
def main(database_conn: Connection = None) -> None:
    end_date: str = to_string(get_time_et(add_days=-1))
    LOGGER.info(f"end_date={end_date}")

    tickers: List[tuple] = database_conn.execute(__SQL_SELECT_TICKERS).fetchall()
    tickers: List[str] = [ticker[0] for ticker in tickers]
    LOGGER.info(f"tickers.length={len(tickers)}")

    cursor: Cursor = database_conn.cursor()
    for ticker in tickers:
        candles: List[tuple] = cursor.execute(__SQL_SELECT_HISTORY, {"ticker": ticker, "granularity": "DAY"}).fetchall()
        candles: List[tuple] = sorted(candles, key=lambda candle: candle[1], reverse=True)
        if len(candles) > 0 and to_string(candles[0][1]) == end_date:
            print(f"ticker={ticker}, DB Already Up-To-Date, Skipping")
            continue

        history: List[Candle] = get_history(ticker, "DAY", __START_DATE, end_date)
        LOGGER.info(f"ticker={ticker}, history.length={len(history)}")

        cursor.executemany(__SQL_INSERT, [asdict(i) for i in history])
        database_conn.commit()


if __name__ == "__main__":
    main()
