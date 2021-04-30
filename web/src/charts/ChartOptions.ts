import Highcharts from 'highcharts';
import {ValueMap} from '../types/ValueMap';
import {ChartType} from './ChartTypes';

const RangeSelector: Highcharts.RangeSelectorOptions = {
    buttons: [
        {count: 1, text: '1H', type: 'hour'},
        {count: 6, text: '6H', type: 'hour'},
        {count: 1, text: '1D', type: 'day'},
        {count: 2, text: '2D', type: 'day'},
        {count: 1, text: 'All', type: 'all'}
    ],
    inputEnabled: false,
    selected: 0
};

export const ChartOptions: ValueMap<Highcharts.Options> = {
    [ChartType.CANDLESTICK]: {rangeSelector: RangeSelector},
    [ChartType.LINE]: {rangeSelector: RangeSelector}
};
