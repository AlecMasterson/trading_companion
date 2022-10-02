import {sortBy} from 'lodash';
import {iTickerData} from '../types/iTickerData';
import {iTickerSummary} from '../types/iTickerSummary';
import {Granularity} from '../types/Granularity';
import Data from './data.json';

const TickerSummary: iTickerSummary[] = [
    {currentPrice: 54323.12432, name: 'BTC', source: 'Coinbase'},
    {currentPrice: 54331.6533, name: 'BTC', source: 'Binance'},
    {currentPrice: 3211.9324, name: 'ETH', source: 'Binance'},
    {currentPrice: 792.744445, name: 'APPL', source: 'ETrade'},
    {currentPrice: 4222.653, name: 'TES', source: 'ETrade'},
    {currentPrice: 92.32211, name: 'UDX', source: 'Binance'}
];

export default class AppApi {

    public static async getTickerData(ticker: string): Promise<iTickerData | null> {
        return {
            candles: sortBy(JSON.parse(Data), 'candle_timestamp'),
            forecasts: {},
            granularity: Granularity.DAY_1,
            ticker
        };
    }

    public static async getTickerSummary(): Promise<iTickerSummary[]> {
        return TickerSummary;
    }

    public static async getTechIndicators(): Promise<string[]> {
        return [];
    }

    public static async getIndicatorData(indicator: string, candles: iTickerData[], options?: object): Promise<number[]> {
        console.log(indicator, candles, options);
        return [];
    }
}
