from datetime import datetime
from enums.Granularity import Granularity
from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlmodel import Column, Field, SQLModel
from typing import List, Optional
from utils.date_util import get_now


class Candle(SQLModel, table=True):

    __table_args__ = {
        "schema": "market_data"
    }
    __tablename__ = "candles"

    close: float
    granularity: Granularity = Field(primary_key=True)
    high: float
    low: float
    open: float
    ticker: str = Field(primary_key=True)
    volume: float

    created_at: datetime = Field(default_factory=get_now)
    timestamp: datetime = Field(default_factory=get_now, primary_key=True)
    updated_at: datetime = Field(sa_column=Column(DateTime, default_factory=get_now, nullable=False, onupdate=get_now)) # TODO: Fix.


class CandleIndicator(BaseModel):
    timestamp: datetime
    value: Optional[float] = None
    values: Optional[List[Optional[float]]] = None
