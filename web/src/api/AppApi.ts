import {iTickerData} from '../types/iTickerData';
import {Granularity} from '../types/Granularity';
import {sortBy} from 'lodash';
import Data from './data.json';

export default class AppApi {

    public static async getTickerData(ticker: string): Promise<iTickerData | null> {
        return {
            candles: sortBy(JSON.parse(Data), 'candle_timestamp'),
            forecasts: {},
            granularity: Granularity.DAY_1,
            ticker
        };
    }
}
