import {Granularity} from './enums/Granularity';

export interface Candle {
    close: number;
    granularity: Granularity;
    high: number;
    low: number;
    open: number;
    ticker: string;
    timestamp: string;
    volume: number;
}
