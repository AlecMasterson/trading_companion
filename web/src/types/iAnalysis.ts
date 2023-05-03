import {PlotOptions, Series, YAxisPlotLinesOptions} from 'highcharts';
import {Indicator} from './enums/Indicator';
import {LearnedModel} from './enums/LearnedModel';

export interface iAnalysisData {
    candle_timestamp: number;
    [key: string]: number;
}

export interface iAnalysis {
    data: iAnalysisData[];
    type: Indicator | LearnedModel;
}

interface iAnalysisConfig {
    dataKey: string;
    offset: boolean;
    plotLines?: Array<Partial<YAxisPlotLinesOptions>>;
    plotOptions?: Partial<PlotOptions>;
    series: Partial<Series>;
}

export const AnalysisConfigMap: {[key in (Indicator | LearnedModel)]: iAnalysisConfig} = {
    [Indicator.ADX]: {
        dataKey: Indicator.ADX,
        offset: true,
        series: {
            name: Indicator.ADX,
            type: 'line'
        }
    },
    [Indicator.EMA_12]: {
        dataKey: Indicator.EMA_12,
        offset: false,
        series: {
            name: Indicator.EMA_12,
            type: 'line'
        }
    },
    [Indicator.EMA_26]: {
        dataKey: Indicator.EMA_26,
        offset: false,
        series: {
            name: Indicator.EMA_26,
            type: 'line'
        }
    },
    [Indicator.MACD]: {
        dataKey: Indicator.MACD,
        offset: true,
        series: {
            name: Indicator.MACD,
            type: 'column'
        }
    },
    [Indicator.MACD_DIFF]: {
        dataKey: Indicator.MACD_DIFF,
        offset: true,
        series: {
            name: Indicator.MACD_DIFF,
            type: 'column'
        }
    },
    [Indicator.RSI]: {
        dataKey: Indicator.RSI,
        offset: true,
        series: {
            name: Indicator.RSI,
            type: 'line'
        }
    },
    [Indicator.STOCH]: {
        dataKey: Indicator.STOCH,
        offset: true,
        series: {
            name: Indicator.STOCH,
            type: 'line'
        }
    },
    [LearnedModel.CHANCE_INCREASING]: {
        dataKey: 'value',
        offset: true,
        plotLines: [
            {
                dashStyle: 'LongDash',
                value: 0
            }
        ],
        series: {
            name: LearnedModel.CHANCE_INCREASING,
            type: 'column'
        }
    }
};
