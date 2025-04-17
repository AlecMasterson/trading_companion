from enums.Indicator import Indicator
from pydantic import BaseModel, Field
from typing import Any, Dict

class IndicatorConfig(BaseModel):
    id: str
    indicator: Indicator
    options: Dict[str, Any] = Field(default={})
