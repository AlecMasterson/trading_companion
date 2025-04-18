import axios, {AxiosRequestConfig, AxiosResponse} from 'axios';
import {Granularity} from '../types/enums/Granularity';
import {Candle} from '../types/Candle';
import {IndicatorConfig} from '../types/IndicatorConfig';
import {NotificationManager} from '../NotificationManager';

interface ExchangeProps extends AxiosRequestConfig {
  errorMessage: string;
}

export default class AppApi {

  public static async getTickerHistory(ticker: string, granularity: Granularity, indicatorConfigs: IndicatorConfig[]): Promise<Candle[]> {
    const props: ExchangeProps = {
      data: {
        granularity: granularity.toUpperCase(),
        indicatorConfigs,
        ticker
      },
      errorMessage: 'getting the ticker history',
      method: 'POST',
      url: '/api/tickers/history'
    };

    return await AppApi.exchange<Candle[]>(props);
  }

  public static async getTickers(): Promise<string[]> {
    const props: ExchangeProps = {
      errorMessage: 'getting the available tickers',
      method: 'GET',
      url: '/api/tickers'
    };

    return await AppApi.exchange<string[]>(props);
  }

  private static async exchange<T>(props: ExchangeProps): Promise<T> {
    try {
      const response: AxiosResponse<T> = await axios.request<T>(props);
      return response.data;
    } catch (error: unknown) {
      const message: string = `Unexpected error while ${props.errorMessage}`;
      NotificationManager(message, {hideIconVariant: true, variant: 'error'});
      throw new Error(message);
    }
  }
}
