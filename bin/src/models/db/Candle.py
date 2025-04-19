from datetime import datetime
from enums.Granularity import Granularity
from enums.Source import Source
from models.CandleBase import CandleBase
from sqlmodel import Field, SQLModel

class Candle(SQLModel, CandleBase, table=True):

    __table_args__ = {
        "schema": "market_data"
    }
    __tablename__ = "candles"

    granularity: Granularity = Field(primary_key=True)
    source: Source = Field(primary_key=True)
    ticker: str = Field(primary_key=True)
    timestamp: datetime = Field(primary_key=True)
