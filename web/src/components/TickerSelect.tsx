import React from 'react';
import {Autocomplete, FormControl, TextField} from '@mui/material';
import {iTicker} from '../types/iTicker';
import AppApi from '../api/AppApi';

interface TickerSelectProps {
  setTicker: (_: iTicker | null) => void;
}

function getSelected(tickers: iTicker[], symbol: string): iTicker | null {
    return tickers.find((ticker: iTicker): boolean => ticker.symbol === symbol) ?? null;
}

export default function TickerSelect(props: TickerSelectProps): React.ReactElement<TickerSelectProps> {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  const [tickers, setTickers] = React.useState<iTicker[]>([]);

  React.useEffect((): void => {
    if (!isOpen || tickers.length > 0) {
      return;
    }

    setIsLoading(true);

    AppApi.getTickers()
      .then(setTickers)
      .finally((): void => setIsLoading(false));
  }, [isOpen]);

  return (
    <FormControl sx={{minWidth: 200}}>
      <Autocomplete
        disableClearable
        loading={isLoading}
        noOptionsText='No Tickers Found'
        onChange={(_: any, symbol: string): void => props.setTicker(getSelected(tickers, symbol))}
        onClose={(): void => setIsOpen(false)}
        onOpen={(): void => setIsOpen(true)}
        open={isOpen}
        options={tickers.map((ticker: iTicker): string => ticker.symbol)}
        renderInput={(params: any): any => (
          <TextField
            {...params}
            label='Ticker'
          />
        )}
      />
    </FormControl>
  );
}
