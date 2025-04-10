from datetime import datetime
from enums.Granularity import Granularity
from models.CandleBase import CandleBase
from sqlmodel import Field, SQLModel
from utils.date_util import get_now

class Candle(SQLModel, CandleBase, table=True):

    __table_args__ = {
        "schema": "market_data"
    }
    __tablename__ = "candles"

    granularity: Granularity = Field(primary_key=True)
    ticker: str = Field(primary_key=True)

    created_at: datetime = Field(default_factory=get_now)
    timestamp: datetime = Field(primary_key=True)
    updated_at: datetime = Field(default_factory=get_now) # TODO: Implement an actual update capability if new data comes in.
