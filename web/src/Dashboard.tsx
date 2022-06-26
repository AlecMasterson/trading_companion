import React from 'react';
import {iTickerData} from './types/iTickerData';
import AppApi from './api/AppApi';
import ForecastChart from './charts/ForecastChart';

const DefaultTicker = 'BTC';

export default function Dashboard (): React. ReactElement | null {
    const [tickerData, setTickerData] = React.useState<iTickerData | null>(null);

    const LoadData = React.useCallback(async () => {
        const data: iTickerData | null = await AppApi.getTickerData(DefaultTicker);
        setTickerData(data);
    }, []);

    React.useEffect((): void => {
        LoadData();
    }, [LoadData]);

    if (!tickerData) {
        return null;
    }

    return (
        <ForecastChart candles={tickerData.candles} />
    );
}
