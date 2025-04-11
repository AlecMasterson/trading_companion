import {Granularity} from './enums/Granularity';
import {Signal} from './enums/Signal';
import {IndicatorEntry} from './IndicatorEntry';

export interface Candle {
    close: number;
    granularity: Granularity;
    high: number;
    indicators: IndicatorEntry[];
    low: number;
    open: number;
    signals: Signal[];
    ticker: string;
    timestamp: string;
    volume: number;
}
