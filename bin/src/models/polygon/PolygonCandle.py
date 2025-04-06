from pydantic import BaseModel, Field
from typing import Optional

class PolygonCandle(BaseModel):
    c: float
    h: float
    l: float
    n: Optional[int] = Field(default=None)
    o: float
    otc: Optional[bool] = Field(default=False)
    t: int
    v: float
    vw: Optional[float] = Field(default=None)
