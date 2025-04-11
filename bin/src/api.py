from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.Candle import Candle
from models.EnrichedCandle import EnrichedCandle
from models.TickerHistoryRequest import TickerHistoryRequest
from sqlalchemy.sql import Select
from sqlmodel import Session, select
from typing import List, Tuple
from utils.database import get_database_session
from utils.ta import apply_indicator

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

@app.post("/api/tickers/history", response_model=List[EnrichedCandle])
def get_ticker_history(
    request: TickerHistoryRequest,
    database_session: Session = Depends(get_database_session)
) -> List[EnrichedCandle]:
    statement: Select[Tuple[Candle]] = select(Candle).where(Candle.ticker == request.ticker, Candle.granularity == request.granularity).order_by(Candle.timestamp)
    candles: List[Candle] = database_session.exec(statement).all()

    candles_enriched: List[EnrichedCandle] = [EnrichedCandle(**candle.model_dump()) for candle in candles]
    [apply_indicator(indicator_config, candles_enriched) for indicator_config in request.indicator_configs]

    return candles_enriched
