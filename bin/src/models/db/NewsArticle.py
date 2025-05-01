from datetime import datetime
from sqlmodel import Field, SQLModel

class NewsArticle(SQLModel, table=True):

    __table_args__ = {
        "schema": "market_insights"
    }
    __tablename__ = "news_articles"

    snippet: str
    timestamp: datetime
    title: str
    url: str = Field(primary_key=True)
