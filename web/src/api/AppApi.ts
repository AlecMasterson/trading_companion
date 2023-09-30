import axios, {AxiosResponse} from 'axios';
import {iCandle} from '../types/iCandle';
import {iAnalysisData} from '../types/iAnalysis';
import {iTicker} from '../types/iTicker';
import {LearnedModel} from '../types/enums/LearnedModel';
import {Source} from '../types/enums/Source';


const URL = 'http://localhost:8000';

export default class AppApi {

    public static async getAnalysisIndicators(candles: iCandle[]): Promise<Array<iAnalysisData>> {
        const response: AxiosResponse = await axios.post(URL + '/api/analysis/indicators', {candles});
        return response.data;
    }

    public static async getAnalysisLearnedModel(model: LearnedModel, candles: iCandle[]): Promise<Array<iAnalysisData>> {
        const response: AxiosResponse = await axios.post(URL + '/api/analysis/model', {model, candles});
        return response.data;
    }

    public static async getTickerHistory(source: string, ticker: string, granularity: string, startDateTime: string, endDateTime: string): Promise<Array<iCandle>> {
        const payload: object = {source, ticker, granularity, startDateTime, endDateTime};
        const response: AxiosResponse = await axios.post(URL + '/api/ticker/history', payload);

        return response.data;
    }

    public static async getTickers(source: Source): Promise<Array<iTicker>> {
        const tickers: any = await axios.get(`http://localhost:8000/tickers?source=${source}`);
        return tickers.data;
    }
    /*

    protected static async post(url: string, payload: any): Promise<any> {
        try {
            const response: AxiosResponse = await axios.post(url, payload);
            response.su

        } catch (exception: unknown) {

        }
    }
    */
}
