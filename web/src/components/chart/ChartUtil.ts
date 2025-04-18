import {Theme} from '@mui/material/styles';
import {Options, Point, PointOptionsObject, Series, SeriesCandlestickOptions, SeriesLineOptions} from 'highcharts';

function formatCaptionValue(label: string, value: number | undefined): string {
  const valueStr: string = value?.toFixed(2) ?? '-';
  return `${label}: ${valueStr}`;
}

export function getThemedChartOptions(theme: Theme): Options {
  const spacingValue: number = parseInt(theme.spacing(2).replace('px', ''));

  return {
    caption: {
      style: {
        color: theme.palette.text.secondary
      }
    },
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
      lineColor: theme.palette.divider,
      minRange: 20 * 24 * 3600 * 1000,
      type: 'datetime'
    }
  };
}

export function setCaptionText(this: Point): void {
  const caption: string[] = [];
  const captionExtra: string[] = [];

  this.series.chart.series.forEach((series: Series): void => {
    const options: SeriesCandlestickOptions | SeriesLineOptions =
      series.options as SeriesCandlestickOptions | SeriesLineOptions;
    const point: PointOptionsObject | undefined = (options.data as PointOptionsObject[])
      .find((temp: PointOptionsObject): boolean => temp.x === this.x);
    if (point === undefined) {
      return;
    }

    if (series.options.type === 'candlestick') {
      caption.push([
        point.id,
        formatCaptionValue('O', point.open),
        formatCaptionValue('H', point.high),
        formatCaptionValue('L', point.low),
        formatCaptionValue('C', point.close)
      ].join(' '));
    } else {
      captionExtra.push(formatCaptionValue(series.options.id!, point.y!));
    }
  });

  if (!caption.length) {
    return;
  }

  this.series.chart.setCaption({text: [...caption, captionExtra.join(' ')].join('<br/>')});
}
