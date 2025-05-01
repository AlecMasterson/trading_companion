from argparse import ArgumentParser
from datetime import timedelta
from models.db.NewsArticle import NewsArticle
from services.polygon import get_news_articles
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlmodel import Session
from utils import LOGGER
from utils.database import get_database_session
from utils.date_util import get_now_eastern, to_string
from typing import List

_database_session: Session = next(get_database_session())

def update(date: str) -> None:
    news_articles: List[NewsArticle] = get_news_articles(date)
    news_articles_dict: List[dict] = [article.model_dump() for article in news_articles]
    LOGGER.info(f"date={date} news_articles.length={len(news_articles_dict)}")

    _database_session.exec(db_insert(NewsArticle).values(news_articles_dict).on_conflict_do_nothing())
    _database_session.commit()

def main(total_days_in_past: int) -> None:
    for days_in_past in range(0, total_days_in_past+1):
        date: str = to_string(get_now_eastern() - timedelta(days=days_in_past), format="%Y-%m-%d")
        update(date)

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-d", default=0, type=int)
    total_days_in_past: int = parser.parse_args().d

    main(total_days_in_past)
