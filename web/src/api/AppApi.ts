import axios, {AxiosResponse, Method} from 'axios';
import {iCandle} from '../types/iCandle';
import {iTicker} from '../types/iTicker';
import {Granularity} from '../types/enums/Granularity';
import {Indicator} from '../types/enums/Indicator';

export default class AppApi {
    public static async getHistory(ticker: string, granularity: Granularity): Promise<iCandle[]> {
        const payload: object = {
            end_date: '2024-01-01',
            granularity: granularity.toUpperCase(),
            start_date: '2023-01-01',
            ticker
        };

        return AppApi.request('POST', 'http://localhost:8081/api/history', {}, payload);
    }

    public static async getIndicator(indicator: Indicator, data: iCandle[]): Promise<any[]> {
        const payload: object = {
            data,
            indicator
        };

        return AppApi.request('POST', 'http://localhost:8081/api/indicator', {}, payload);
    }

    public static async getTickers(): Promise<iTicker[]> {
        return AppApi.request('GET', 'http://localhost:8081/api/tickers');
    }

    private static async request(method: Method, url: string, params: object = {}, payload: any = undefined): Promise<any> {
        await new Promise((resolve: (_: unknown) => void): number => setTimeout(resolve, 1500));

        const response: AxiosResponse = await axios.request({data: payload, method, params, url});
        if (response.status >= 400) {
            throw new Error(`[HTTP] - <${response.status}> - ${response.statusText}`);
        }

        return response.data;
    }
}
