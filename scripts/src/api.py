from fastapi import FastAPI
from models.Candle import Candle
from pydantic import BaseModel
from typing import List

class Request(BaseModel):
    data: List[Candle]

app = FastAPI()

@app.post("/api/get")
async def get_indicator_momentum_RSI(request: Request):
    return {"message": "Hello World"}
