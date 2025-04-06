from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class IndicatorCandle(BaseModel):
    timestamp: datetime
    values: List[Optional[float]]
