import React from 'react';
import {Line} from 'react-chartjs-2';
import type {ChartData} from 'chart.js';
import 'chartjs-adapter-moment';
import {iCandle} from '../types/iCandle';
import ChartUtil, {OPTIONS_MarketChart} from './ChartUtil';
import TimeUtil from '../utils/TimeUtil';

interface iMarketChartProps {
    candles: iCandle[]
}

interface iMarketChartState {
    registered: boolean;
}

export default class MarketChart extends React.Component<iMarketChartProps, iMarketChartState> {

    override state: iMarketChartState = {registered: false};

    public constructor(props: iMarketChartProps) {
        super(props);

        this.getLabels = this.getLabels.bind(this);
    }

    public override componentDidMount(): void {
        ChartUtil.register();
        this.setState({registered: true});
    }

    public getLabels(candles: iCandle[]): string[] {
        return candles.map((candle: iCandle): string => TimeUtil.timestampToDateString(candle.candle_timestamp));
    }

    public override render(): React.ReactElement | null {
        if (!this.state.registered) {
            return null;
        }

        const data: ChartData<'line'> = {
            datasets: [{
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgb(255, 99, 132)',
                data: this.props.candles.map((candle: iCandle): number => candle.price_close),
                label: 'Price',
                pointRadius: 0
            }],
            labels: this.getLabels(this.props.candles)
        };

        return <Line data={data} options={OPTIONS_MarketChart} />;
    }
}
