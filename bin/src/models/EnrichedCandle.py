from models.CandleBase import CandleBase
from pydantic import Field
from typing import Dict, List, Optional

class EnrichedCandle(CandleBase):
    indicators: Dict[str, List[Optional[float]]] = Field(default={})
