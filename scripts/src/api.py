from analysis.ML import fit_model, get_indicator
from enums.Source import Source
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.Candle import Candle
from models.IndicatorRequest import IndicatorRequest
from models.ModelRequest import ModelRequest
from models.Ticker import Ticker
from models.TickerHistoryRequest import TickerHistoryRequest
from sources.Coinbase import Coinbase
from typing import List
from utils import LOGGER


__SOURCE_MAP = {
    Source.COINBASE: Coinbase
}


App: FastAPI = FastAPI(
    title="Trading Companion"
)

RouterAnalysis: APIRouter = APIRouter()
RouterTicker: APIRouter = APIRouter()

# TODO: Determine optimal networking solution.
App.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)


@RouterAnalysis.post("/indicator")
async def analysis_indicator(request: IndicatorRequest) -> List[dict]:
    LOGGER.info(f"indicator={request.indicator}, candles.size={len(request.candles)}")

    return get_indicator(request.indicator, request.candles)


@RouterAnalysis.post("/model")
async def analysis_get(request: ModelRequest) -> List[dict]:
    LOGGER.info(f"model={request.model}, candles.size={len(request.candles)}")

    return fit_model(request.model, request.candles)


@RouterTicker.get("/all")
async def ticker_all(source: Source) -> List[Ticker]:
    LOGGER.info(source)

    return __SOURCE_MAP[source].get_tickers()


@RouterTicker.post("/history")
async def ticker_history(request: TickerHistoryRequest) -> List[Candle]:
    LOGGER.info(request)

    return __SOURCE_MAP[request.source].get_ticker_history(request.ticker, request.granularity, request.startDateTime, request.endDateTime)


App.include_router(router=RouterAnalysis, prefix="/api/analysis")
App.include_router(router=RouterTicker, prefix="/api/ticker")
