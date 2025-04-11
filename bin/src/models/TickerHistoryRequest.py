from enums.Granularity import Granularity
from models.IndicatorConfig import IndicatorConfig
from pydantic import BaseModel, Field
from typing import List

class TickerHistoryRequest(BaseModel):
    indicator_configs: List[IndicatorConfig] = Field(alias="indicatorConfigs", default=[])
    granularity: Granularity
    ticker: str
