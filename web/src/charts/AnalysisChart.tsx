import React from 'react';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import {get} from 'lodash';
import {AnalysisConfigMap, iAnalysis, iAnalysisData} from '../types/iAnalysis';
import {iCandle} from '../types/iCandle';
import TimeUtil from '../utils/TimeUtil';

const COLOR_AXIS = '#787878';
const COLOR_BACKGROUND = '#4E4868';
const COLOR_CANDLESTICK_GREEN = '#00CC66';
const COLOR_CANDLESTICK_RED = '#FF3333';
const COLOR_LABEL = '#D8D8D8';

function getAnalysisData(analysis: iAnalysis): Array<Array<number>> {
    return analysis.data.map((x: iAnalysisData): number[] => [
        x.candle_timestamp * 1000,
        get(x, AnalysisConfigMap[analysis.type].dataKey)
    ]);
}

function getCandlestickData(candles: iCandle[]): Array<Array<number>> {
    return candles.map((candle: iCandle): number[] => [
        candle.candle_timestamp * 1000,
        candle.price_open,
        candle.price_high,
        candle.price_low,
        candle.price_close
    ]);
}

interface AnalysisChartProps {
    candles: iCandle[];
    selected: iAnalysis | null;
    selectedOffset: iAnalysis | null;
}

export default function AnalysisChart(props: AnalysisChartProps): React.ReactElement {
    const series: any[] = [
        {
            data: getCandlestickData(props.candles),
            name: 'candles',
            type: 'candlestick'
        }
    ];

    const yAxis: any[] = [
        {
            crosshair: {
                dashStyle: 'LongDash'
            },
            gridLineColor: COLOR_AXIS,
            labels: {
                style: {
                    color: COLOR_LABEL
                }
            },
            title: {
                enabled: false
            }
        }
    ];

    if (props.selected) {
        series.push({
            ...AnalysisConfigMap[props.selected.type].series,
            data: getAnalysisData(props.selected)
        });

        yAxis[0].plotLines = AnalysisConfigMap[props.selected.type].plotLines || [];
    }

    if (props.selectedOffset) {
        series.push({
            ...AnalysisConfigMap[props.selectedOffset.type].series,
            data: getAnalysisData(props.selectedOffset),
            yAxis: 1
        });

        yAxis[0].height = '70%';
        yAxis.push({
            gridLineWidth: 0,
            height: '30%',
            labels: {
                offset: 0,
                style: {
                    color: COLOR_LABEL
                }
            },
            plotLines: AnalysisConfigMap[props.selectedOffset.type].plotLines || [],
            title: {
                enabled: false
            },
            top: '70%'
        });
    }

    return (
        <HighchartsReact
            containerProps={{
                style: {
                    height: '100%'
                }
            }}
            highcharts={Highcharts}
            options={{
                chart: {
                    backgroundColor: COLOR_BACKGROUND,
                    panning: true,
                    style: {
                        fontFamily: 'Roboto'
                    }
                },
                credits: {
                    enabled: false
                },
                legend: {
                    enabled: false
                },
                navigator: {
                    enabled: true
                },
                plotOptions: {
                    ...(props.selected ? AnalysisConfigMap[props.selected.type].plotOptions ?? {} : {}),
                    ...(props.selectedOffset ? AnalysisConfigMap[props.selectedOffset.type].plotOptions ?? {} : {}),
                    candlestick: {
                        color: COLOR_CANDLESTICK_RED,
                        lineColor: COLOR_CANDLESTICK_RED,
                        upColor: COLOR_CANDLESTICK_GREEN,
                        upLineColor: COLOR_CANDLESTICK_GREEN
                    },
                    line: {
                        color: '#FFFF00',
                        marker: {
                            enabled: false
                        }
                    },
                    series: {
                        states: {
                            inactive: {
                                opacity: 1
                            }
                        }
                    }
                },
                series,
                title: null,
                tooltip: {
                    enabled: false
                },
                xAxis: {
                    crosshair: {
                        dashStyle: 'LongDash',
                        label: {
                            formatter: TimeUtil.timestampToDateString
                        }
                    },
                    labels: {
                        formatter: (x: {value: number}): string => TimeUtil.timestampToDateString(x.value),
                        style: {
                            color: COLOR_LABEL
                        }
                    }
                },
                yAxis
            }}
        />
    );
}
