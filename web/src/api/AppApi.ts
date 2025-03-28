import axios, {AxiosResponse, Method} from 'axios';
import {Granularity} from '../types/enums/Granularity';
import {Candle} from '../types/Candle';
import {IndicatorCandle} from '../types/IndicatorCandle';
import {IndicatorConfig} from '../types/IndicatorConfig';

axios.defaults.baseURL = 'http://localhost:8080';

export default class AppApi {

  public static async getIndicator(ticker: string, granularity: Granularity, indicatorConfig: IndicatorConfig): Promise<IndicatorCandle[]> {
    const payload: object = {
      granularity: granularity.toUpperCase(),
      indicator: indicatorConfig.indicator,
      period: indicatorConfig.period,
      periodFast: indicatorConfig.periodFast,
      periodSignal: indicatorConfig.periodSignal,
      periodSlow: indicatorConfig.periodSlow,
      ticker
    };

    return AppApi.request<IndicatorCandle[]>('POST', '/api/tickers/indicator', {}, payload);
  }

  public static async getTickers(): Promise<string[]> {
    return AppApi.request<string[]>('GET', '/api/tickers');
  }

  public static async getTickerHistory(ticker: string, granularity: Granularity): Promise<Candle[]> {
    return AppApi.request<Candle[]>('GET', `/api/tickers/${ticker}/history/${granularity.toUpperCase()}`);
  }

  private static async request<T>(method: Method, url: string, params: object = {}, payload: any = undefined): Promise<T> {
    await new Promise((resolve: (_: unknown) => void): number => setTimeout(resolve, 1500));

    const response: AxiosResponse = await axios.request({data: payload, method, params, url});
    if (response.status >= 400) {
      throw new Error(`[HTTP] - <${response.status}> - ${response.statusText}`);
    }

    return response.data;
  }
}
