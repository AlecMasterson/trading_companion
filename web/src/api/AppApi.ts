import BaseApi from './BaseApi';
import {Candle} from '../types/Candle';

export const SourceCandles = '/api/source/get/candles';

export default class AppApi {
    public static async GetCandles(source: string, ticker: string, interval: string): Promise<Candle[]> {
        try {
            const request = {source, ticker, interval};
            return await BaseApi.get<Candle[]>(SourceCandles, request);
        } catch (error) {
            console.error(error);
            return [];
        }
    }
}
