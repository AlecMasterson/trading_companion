import React from 'react';
import {FormControl, List, TextField} from '@mui/material';
import {iTickerSummary} from '../../types/iTickerSummary';
import TickerItem from './TickerItem';
import SelectionUtil from './SelectionUtil';
import './selection.css';

interface iTickerSelectionProps {
    onSelect: (ticker: iTickerSummary) => void;
    tickers: iTickerSummary[];
}

interface iTickerSelectionState {
    filter: string;
    selectedTicker: iTickerSummary | null;
}

export function TickerSelectionBare (props: iTickerSelectionProps): React.ReactElement {
    const [state, setState] = React.useState<iTickerSelectionState>({filter: '', selectedTicker: null});

    function onClick(ticker: iTickerSummary): void {
        setState({...state, selectedTicker: ticker});
        props.onSelect(ticker);
    }

    function onFilterChange(event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void {
        setState({...state, filter: event.target.value});
    }

    const tickers: React.ReactElement[] = SelectionUtil.filterTickers(props.tickers, state.filter)
        .map((ticker: iTickerSummary): React.ReactElement => (
            <TickerItem
                key={ticker.source + ticker.name}
                onClick={onClick}
                selected={SelectionUtil.isTickerEqual(state.selectedTicker, ticker)}
                ticker={ticker}
            />
        ));

    return (
        <React.Fragment>
            <FormControl className='selection-form' variant='outlined'>
                <TextField onChange={onFilterChange} />
            </FormControl>

            <List>
                {tickers}
            </List>
        </React.Fragment>
    );
}

export default React.memo(TickerSelectionBare);
