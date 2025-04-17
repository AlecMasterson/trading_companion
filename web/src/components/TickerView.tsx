import React from 'react';
import {Button, Chip, Paper} from '@mui/material';
import Grid from '@mui/material/Grid2';
import {Granularity} from '../types/enums/Granularity';
import {Candle} from '../types/Candle';
import {IndicatorConfig} from '../types/IndicatorConfig';
import AppApi from '../api/AppApi';
import CandleChart from './CandleChart';
import GranularitySelect from './GranularitySelect';
import IndicatorConfigurator, {IndicatorConfiguratorRef} from './indicator/IndicatorConfigurator';
import TickerSelect from './TickerSelect';

export default function TickerView(): React.ReactElement {
  const refIndicatorConfigurator: React.RefObject<IndicatorConfiguratorRef> = React.useRef<IndicatorConfiguratorRef>(null);

  const [candles, setCandles] = React.useState<Candle[]>([]);
  const [granularity, setGranularity] = React.useState<Granularity>(Granularity.DAY);
  const [indicatorConfigs, setIndicatorConfigs] = React.useState<IndicatorConfig[]>([]);
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [ticker, setTicker] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!ticker) {
      return;
    }

    setIsLoading(true);
    AppApi.getTickerHistory(ticker, granularity, indicatorConfigs)
      .then(setCandles)
      .finally((): void => setIsLoading(false));
  }, [granularity, indicatorConfigs, ticker]);

  const onAddIndicator: (_: IndicatorConfig) => void = React.useCallback((indicatorConfig: IndicatorConfig): void => {
    setIndicatorConfigs((temp: IndicatorConfig[]): IndicatorConfig[] => [...temp, indicatorConfig]);
  }, []);

  const onDeleteIndicator: (id: string) => void = React.useCallback((id: string): void => {
    setIndicatorConfigs((temp: IndicatorConfig[]): IndicatorConfig[] =>
      temp.filter((indicatorConfig: IndicatorConfig): boolean => indicatorConfig.id !== id));
  }, []);

  const indicatorChips: React.ReactElement[] = indicatorConfigs.map((indicatorConfig: IndicatorConfig): React.ReactElement => (
    <Chip
      disabled={isLoading}
      key={indicatorConfig.id}
      label={indicatorConfig.id}
      onDelete={(): void => onDeleteIndicator(indicatorConfig.id)}
    />
  ));

  return (
    <Paper className='fill-height' square={false} sx={{p: 2}}>
      <Grid alignItems='center' container spacing={2} sx={{pb: 2}}>
        <TickerSelect isLoading={isLoading} setTicker={setTicker} />

        <GranularitySelect granularity={granularity} isLoading={isLoading} setGranularity={setGranularity} />

        <Button disabled={isLoading} onClick={(): void => refIndicatorConfigurator.current?.setIsOpen(true)} variant='outlined'>
          Add Indicator
        </Button>

        <IndicatorConfigurator onSubmit={onAddIndicator} ref={refIndicatorConfigurator} />

        {indicatorChips}
      </Grid>

      <CandleChart candles={candles} isLoading={isLoading} />
    </Paper>
  );
}
