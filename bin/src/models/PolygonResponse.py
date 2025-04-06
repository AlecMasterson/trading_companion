from pydantic import BaseModel, Field
from typing import Any, List, Optional

class PolygonCandle(BaseModel):
    c: float
    h: float
    l: float
    n: float
    o: float
    t: float
    v: float
    vw: float

class PolygonResponse(BaseModel):
    next_url: Optional[str] = Field(default=None)
    results: Optional[List[Any]] = Field(default=[])
    status: str
