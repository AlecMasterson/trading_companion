from pydantic import BaseModel, Field
from typing import Any, List, Optional

class PolygonResponse(BaseModel):
    next_url: Optional[str] = Field(default=None)
    results: Optional[List[Any]] = Field(default=[])
    status: str
