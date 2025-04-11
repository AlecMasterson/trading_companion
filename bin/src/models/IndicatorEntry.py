from enums.Indicator import Indicator
from pydantic import BaseModel
from typing import List, Optional

class IndicatorEntry(BaseModel):
    data: List[Optional[float]]
    id: str
    indicator: Indicator
