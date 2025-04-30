from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional

class News(SQLModel, table=True):

    __table_args__ = {
        "schema": "market_data"
    }
    __tablename__ = "news"

    id: Optional[int] = Field(default=None, primary_key=True)
    snippet: str
    timestamp: datetime
    title: str
    url: str
