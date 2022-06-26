import {iCandle} from './iCandle';
import {Granularity} from './Granularity';
import {ValueMap} from './ValueMap';

export interface iTickerData {
    candles: iCandle[];
    forecasts: ValueMap<iCandle[]>;
    granularity: Granularity;
    ticker: string;
}
