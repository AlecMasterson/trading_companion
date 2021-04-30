export interface Candle {
    close: number;
    closeTime: string;
    high: number;
    interval: string;
    low: number;
    open: number;
    openTime: string;
    ticker: string;
}

export type CandleProp =
    | 'close'
    | 'closeTime'
    | 'high'
    | 'interval'
    | 'low'
    | 'open'
    | 'openTime'
    | 'ticker';
