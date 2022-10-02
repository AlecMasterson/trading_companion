import {Chart, registerables} from 'chart.js';

export const OPTIONS_MarketChart = {
    plugins: {
        legend: {display: false}
    },
    responsive: true,
    scales: {
        xAxis: {
            grid: {color: '#AAA'},
            ticks: {
                autoSkip: true,
                color: '#AAA',
                maxTicksLimit: 16
            },
            time: {}
        },
        yAxis: {
            grid: {color: '#AAA'},
            ticks: {color: '#AAA'}
        }
    }
};

export default class ChartUtil {

    public static register(): void {
        Chart.register(...registerables);
    }
}
