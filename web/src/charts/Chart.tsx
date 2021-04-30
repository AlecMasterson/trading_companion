import React from 'react';
import Highcharts from 'highcharts';
import HighchartsStock from 'highcharts/modules/stock';
import HighchartsReact from 'highcharts-react-official';
import {DarkTheme} from './ChartThemes';
import {ChartOptions} from './ChartOptions';
import {ChartType} from './ChartTypes';

HighchartsStock(Highcharts);
Highcharts.setOptions(DarkTheme);

interface ChartProps {
    chartType: ChartType;
    series: Highcharts.SeriesOptionsType[];
    title: string;
}

export function Chart (props: ChartProps): React.ReactElement {
    const options: Highcharts.Options = {
        ...ChartOptions[props.chartType],
        title: {text: props.title},
        series: props.series
    };

    return (
        <HighchartsReact
            constructorType='stockChart'
            highcharts={Highcharts}
            options={options}
        />
    );
}
