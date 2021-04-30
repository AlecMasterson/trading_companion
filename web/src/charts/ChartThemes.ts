import Highcharts from 'highcharts';

export const DarkTheme: Highcharts.Options = {
    chart: {
        backgroundColor: {
            linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
            stops: [[0, '#2a2a2b'], [1, '#3e3e40']]
        },
        plotBorderColor: '#606063',
        style: {fontFamily: '\'Unica One\', sans-serif'}
    },
    colors: ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066',
        '#eeaaee', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
    credits: {style: {color: '#666'}},
    drilldown: {
        activeAxisLabelStyle: {color: '#F0F0F3'},
        activeDataLabelStyle: {color: '#F0F0F3'}
    },
    legend: {
        itemHiddenStyle: {color: '#606063'},
        itemHoverStyle: {color: '#FFF'},
        itemStyle: {color: '#E0E0E3'}
    },
    navigation: {
        buttonOptions: {
            symbolStroke: '#DDDDDD',
            theme: {fill: '#505053'}
        }
    },
    navigator: {
        handles: {
            backgroundColor: '#666',
            borderColor: '#AAA'
        },
        outlineColor: '#CCC',
        maskFill: 'rgba(255,255,255,0.1)',
        series: {
            color: '#7798BF',
            lineColor: '#A6C7ED'
        },
        xAxis: {gridLineColor: '#505053'}
    },
    plotOptions: {
        boxplot: {fillColor: '#505053'},
        candlestick: {lineColor: 'white'},
        errorbar: {color: 'white'},
        series: {
            dataLabels: {color: '#B0B0B3'},
            marker: {lineColor: '#333'}
        }
    },
    rangeSelector: {
        buttonTheme: {
            fill: '#505053',
            states: {
                hover: {
                    fill: '#707073',
                    stroke: '#000000',
                    style: {color: 'white'}
                },
                select: {
                    fill: '#000003',
                    stroke: '#000000',
                    style: {color: 'white'}
                }
            },
            stroke: '#000000',
            style: {color: '#CCC'}
        },
        inputBoxBorderColor: '#505053',
        inputStyle: {
            backgroundColor: '#333',
            color: 'silver'
        },
        labelStyle: {color: 'silver'}
    },
    scrollbar: {
        barBackgroundColor: '#808083',
        barBorderColor: '#808083',
        buttonArrowColor: '#CCC',
        buttonBackgroundColor: '#606063',
        buttonBorderColor: '#606063',
        rifleColor: '#FFF',
        trackBackgroundColor: '#404043',
        trackBorderColor: '#404043'
    },
    subtitle: {
        style: {
            color: '#E0E0E3',
            textTransform: 'uppercase'
        }
    },
    title: {
        style: {
            color: '#E0E0E3',
            fontSize: '20px',
            textTransform: 'uppercase'
        }
    },
    tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        style: {color: '#F0F0F0'}
    },
    xAxis: {
        gridLineColor: '#707073',
        labels: {style: {color: '#E0E0E3'}},
        lineColor: '#707073',
        minorGridLineColor: '#505053',
        tickColor: '#707073',
        title: {style: {color: '#A0A0A3'}}
    },
    yAxis: {
        gridLineColor: '#707073',
        labels: {style: {color: '#E0E0E3'}},
        lineColor: '#707073',
        minorGridLineColor: '#505053',
        tickColor: '#707073',
        tickWidth: 1,
        title: {style: {color: '#A0A0A3'}}
    },
    /*
    labels: {
        style: {
            color: '#707073'
        }
    },
     */
};
