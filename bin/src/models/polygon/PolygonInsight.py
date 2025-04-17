from enums.polygon.PolygonSentiment import PolygonSentiment
from pydantic import BaseModel

class PolygonInsight(BaseModel):
    sentiment: PolygonSentiment
    sentiment_reasoning: str
    ticker: str
