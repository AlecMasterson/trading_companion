from enums.polygon.PolygonLocale import PolygonLocale
from enums.polygon.PolygonMarket import PolygonMarket
from pydantic import BaseModel, Field
from typing import Optional

class PolygonTicker(BaseModel):
    active: Optional[bool] = Field(default=None)
    cik: Optional[str] = Field(default=None)
    composite_figi: Optional[str] = Field(default=None)
    currency_name: Optional[str] = Field(default=None)
    delisted_utc: Optional[str] = Field(default=None)
    last_updated_utc: Optional[str] = Field(default=None)
    locale: PolygonLocale
    market: PolygonMarket
    name: str
    primary_exchange: Optional[str] = Field(default=None)
    share_class_figi: Optional[str] = Field(default=None)
    ticker: str
    type: Optional[str] = Field(default=None)
