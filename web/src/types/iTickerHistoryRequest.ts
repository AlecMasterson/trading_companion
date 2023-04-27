import {Granularity} from './Granularity';
import {Source} from './Source';

export interface iTickerHistoryRequest {
    endDateTime: string;
    granularity: Granularity;
    source: Source;
    startDateTime: string;
    ticker: string;
}
