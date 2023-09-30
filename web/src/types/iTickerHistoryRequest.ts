import {Granularity} from './enums/Granularity';
import {Source} from './enums/Source';

export interface iTickerHistoryRequest {
    endDateTime: string;
    granularity: Granularity;
    source: Source;
    startDateTime: string;
    ticker: string;
}
