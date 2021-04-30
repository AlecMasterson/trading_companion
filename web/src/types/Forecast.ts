export interface Forecast {
    correctPrice: number;
    createdDateTime: string;
    futureTime: string;
    interval: string;
    lastUpdatedDateTime: string;
    lowerPrice: number;
    price: number;
    source: string;
    ticker: string;
    upperPrice: number;
}

export type ForecastProp =
    | 'correctPrice'
    | 'createdDateTime'
    | 'futureTime'
    | 'interval'
    | 'lastUpdatedDateTime'
    | 'lowerPrice'
    | 'price'
    | 'source'
    | 'ticker'
    | 'upperPrice';
