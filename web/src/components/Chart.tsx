import React from 'react';
import {Theme, useTheme} from '@mui/material/styles';
import Highcharts, {Options, SeriesOptionsType, YAxisOptions} from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';
import {merge, range} from 'lodash';

const ChartOptions: Options = {
  caption: {
    useHTML: true,
    verticalAlign: 'top'
  },
  chart: {
    displayErrors: true, // this is the default, consider changing to false
    // numberFormatter: undefined, // TODO: probably want to do something here
    // selectionMarkerFill: undefined, // TODO: figure out what this is
    style: { // TODO: check other styles
      fontFamily: 'Share Tech Mono, monospace'
    }
    // zooming: undefined // TODO: documentation wasn't clear on this, might not need it?
  },
  credits: {
    enabled: false
  },
  exporting: {
    enabled: false
  },
  navigator: {
    enabled: false
  },
  plotOptions: {
    series: {
      states: {
        hover: {
          enabled: false
        },
        inactive: {
          enabled: false
        },
        select: {
          enabled: false
        }
      }
    }
  },
  rangeSelector: {
    enabled: false
  },
  // responsive: undefined, // TODO: something? maybe?
  scrollbar: {
    showFull: false
  },
  sonification: {
    enabled: false
  },
  stockTools: {
    gui: {
      enabled: false
    }
  },
  // time: undefined, // TODO: something
  // tooltip: undefined, // TODO: something
  // xAxis: undefined // TODO: something
};

function getThemedChartOptions(theme: Theme): Options {
  const spacingValue: number = parseInt(theme.spacing(2).replace('px', ''));

  return {
    chart: {
      backgroundColor: theme.palette.background.default,
      borderColor: theme.palette.divider,
      borderRadius: theme.shape.borderRadius,
      spacing: [
        spacingValue,
        spacingValue,
        spacingValue,
        spacingValue
      ]
    },
    // colorAxis: undefined, // TODO: something
    colors: [
      theme.palette.primary.main,
      theme.palette.secondary.main
    ],
    plotOptions: { // TODO: review
      candlestick: {
        color: '#F23645',
        lineColor: '#F23645',
        upColor: '#089981',
        upLineColor: '#089981'
      }
    },
    scrollbar: {
      barBackgroundColor: theme.palette.text.secondary,
      barBorderColor: theme.palette.common.white,
      barBorderRadius: theme.shape.borderRadius,
      trackBackgroundColor: theme.palette.background.default,
      trackBorderColor: theme.palette.common.white,
      trackBorderRadius: theme.shape.borderRadius
    },
    xAxis: { // TODO: more
      labels: {
        style: {
          color: theme.palette.text.secondary
        }
      },
      lineColor: theme.palette.divider
    }
  };
}

function getAxisY(theme: Theme, totalRows: number, index: number): YAxisOptions {
  let height: number = 0;
  let top: number = 0;

  if (totalRows > 1) {
    height = index === 0 ? 70 : 30 / (totalRows - 1);
    top = index === 0 ? 0 : 70 + (height * index);
  } else {
    height = 100;
    top = 0;
  }

  return {
    crosshair: {
      label: {
        backgroundColor: '#fbfbfb',
        borderRadius: 0,
        enabled: true,
        padding: 3,
        style: {
          color: '#000'
        }
      }
    },
    gridLineColor: theme.palette.divider,
    height: `${height}%`,
    labels: {
      align: 'left',
      style: {
        color: theme.palette.text.secondary
      }
    },
    lineColor: theme.palette.divider,
    lineWidth: 1,
    top: `${top}%`
  };
}

export default function Chart(props: {series: SeriesOptionsType[]}): React.ReactElement {
  const options: Options = {...ChartOptions};
  const theme: Theme = useTheme();

  const optionsThemed: Options = getThemedChartOptions(theme);
  const custom: Options = {
    series: props.series,
    yAxis: range(props.series.length).map((index: number): YAxisOptions => getAxisY(theme, props.series.length, index))
  };

  merge(options, optionsThemed, custom);

  return (
    <HighchartsReact
      constructorType='stockChart'
      highcharts={Highcharts}
      options={options}
    />
  );
}
