from models.polygon.PolygonInsight import PolygonInsight
from models.polygon.PolygonPublisher import PolygonPublisher
from pydantic import BaseModel, Field
from typing import List, Optional

class PolygonNews(BaseModel):
    amp_url: Optional[str] = Field(default=None)
    article_url: Optional[str] = Field(default=None)
    author: str
    description: Optional[str] = Field(default=None)
    id: str
    image_url: Optional[str] = Field(default=None)
    insights: Optional[List[PolygonInsight]] = Field(default=None)
    keywords: Optional[List[str]] = Field(default=None)
    published_utc: str
    publisher: PolygonPublisher
    tickers: List[str]
    title: str
