import {Source} from '../types/Source';
import {CandleProp} from '../types/Candle';
import {ForecastProp} from '../types/Forecast';
import {PositionProp} from '../types/Position';

export enum ChartContext {
    Forecast,
    History,
    Position
}

export enum ChartType {
    CANDLESTICK,
    LINE
}

export interface ChartConfig {
    context: ChartContext;
    features: (CandleProp | ForecastProp | PositionProp)[];
    index: number;
    source: Source;
    ticker: string;
}
