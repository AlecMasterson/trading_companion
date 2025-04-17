from pydantic import BaseModel, Field
from typing import Optional

class PolygonPublisher(BaseModel):
    favicon_url: Optional[str] = Field(default=None)
    homepage_url: str
    logo_url: str
    name: str
