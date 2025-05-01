from models.db.NewsArticle import NewsArticle
from services.polygon import get_news_articles
from sqlalchemy.dialects.postgresql import insert as db_insert
from sqlmodel import Session
from utils import LOGGER
from utils.database import get_database_session
from utils.date_util import get_now_eastern, to_string
from typing import List

def update(database_session: Session, date: str) -> None:
    news_articles: List[NewsArticle] = get_news_articles(date)
    news_articles_dict: List[dict] = [article.model_dump() for article in news_articles]
    LOGGER.info(f"news_articles.length={len(news_articles_dict)}")

    database_session.exec(db_insert(NewsArticle).values(news_articles_dict).on_conflict_do_nothing())
    database_session.commit()

if __name__ == "__main__":
    database_session: Session = next(get_database_session())
    date: str = to_string(get_now_eastern(), format="%Y-%m-%d")

    update(database_session, date)
