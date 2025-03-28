from enums.Granularity import Granularity
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.Candle import Candle
from models.IndicatorCandle import IndicatorCandle
from models.IndicatorRequest import IndicatorRequest
from sqlalchemy.sql import Select
from sqlmodel import Session, select
from typing import List, Tuple
from utils.database import get_database_session
from utils.ta import get_indicator_values


app: FastAPI = FastAPI(title="Trading Companion")

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["GET", "OPTIONS", "POST"],
    allow_origins=["*"]
)


@app.get("/api/tickers", response_model=List[str])
def get_tickers(database_session: Session = Depends(get_database_session)) -> List[str]:
    statement: Select[Tuple[str]] = select(Candle.ticker).distinct().order_by(Candle.ticker)
    return database_session.exec(statement).all()


@app.get("/api/tickers/{ticker}/history/{granularity}", response_model=List[Candle])
def get_ticker_history(ticker: str, granularity: Granularity, database_session: Session = Depends(get_database_session)) -> List[Candle]:
    statement: Select[Tuple[Candle]]= select(Candle).where(Candle.ticker == ticker, Candle.granularity == granularity).order_by(Candle.timestamp)
    return database_session.exec(statement).all()


@app.post("/api/tickers/indicator", response_model=List[IndicatorCandle])
def get_indicator(request: IndicatorRequest, database_session: Session = Depends(get_database_session)) -> List[IndicatorCandle]:
    candles: List[Candle] = get_ticker_history(request.ticker, request.granularity, database_session)
    return get_indicator_values(request, candles)
