import {Granularity} from './Granularity';
import {Source} from './Source';

export interface iCandle {
    candle_timestamp: number;
    data_source: Source;
    granularity: Granularity;
    interpolated: boolean;
    price_close: number;
    price_high: number;
    price_low: number;
    price_open: number;
    ticker: string;
    volume: number;
}
