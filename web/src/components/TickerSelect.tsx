import React from 'react';
import {Autocomplete, FormControl, TextField} from '@mui/material';
import AppApi from '../api/AppApi';

interface TickerSelectProps {
  isLoading: boolean;
  setTicker: (ticker: string) => void;
}

export default function TickerSelect(props: TickerSelectProps): React.ReactElement<TickerSelectProps> {
  const [isLoading, setIsLoading] = React.useState<boolean>(true);
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  const [tickers, setTickers] = React.useState<string[]>([]);

  React.useEffect((): void => {
    AppApi.getTickers()
      .then(setTickers)
      .finally((): void => setIsLoading(false));
  }, []);

  return (
    <FormControl sx={{minWidth: 200}}>
      <Autocomplete
        disableClearable
        disabled={props.isLoading}
        loading={isLoading}
        noOptionsText='No Tickers Found'
        onChange={(_: any, ticker: string): void => props.setTicker(ticker)}
        onClose={(): void => setIsOpen(false)}
        onOpen={(): void => setIsOpen(true)}
        open={isOpen}
        options={tickers}
        renderInput={(params: any): React.ReactElement => (
          <TextField {...params} label='Ticker' />
        )}
      />
    </FormControl>
  );
}
