import {Point, PointOptionsObject, Series, SeriesCandlestickOptions, SeriesLineOptions} from 'highcharts';

function formatCaptionValue(label: string, value: number | undefined): string {
  const valueStr: string = value?.toFixed(2) ?? '-';
  return `${label}: ${valueStr}`;
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
