import {Granularity} from './enums/Granularity';
import {Source} from './enums/Source';

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
