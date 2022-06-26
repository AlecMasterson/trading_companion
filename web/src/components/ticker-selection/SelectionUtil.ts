import {iTickerSummary} from '../../types/iTickerSummary';

export default class SelectionUtil {
    public static filterTickers(tickers: iTickerSummary[], value: string): iTickerSummary[] {
        return tickers.filter((ticker: iTickerSummary): boolean => {
            const matchSource: boolean = ticker.source.toLowerCase().includes(value.toLowerCase());
            const matchName: boolean = ticker.name.toLowerCase().includes(value.toLowerCase());

            return value === '' || matchSource || matchName;
        });
    }

    public static isTickerEqual(ticker1: iTickerSummary | null, ticker2: iTickerSummary | null): boolean {
        return ticker1?.source === ticker2?.source && ticker1?.name === ticker2?.name;
    }
}
