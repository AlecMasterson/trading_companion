import React from 'react';
import {ListItem, ListItemButton, Stack, Typography} from '@mui/material';
import {iTickerSummary} from '../../types/iTickerSummary';
import NumberUtil from '../../utils/NumberUtil';

interface iTickerItemProps {
    key: string;
    onClick: (ticker: iTickerSummary) => void;
    selected: boolean;
    ticker: iTickerSummary;
}

export function TickerItemBare (props: iTickerItemProps): React.ReactElement {
    const {onClick, selected, ticker} = props;

    const value: string = NumberUtil.formatDollar(ticker.currentPrice);

    return (
        <ListItem disablePadding>
            <ListItemButton onClick={(): void => onClick(ticker)} selected={selected}>
                <Stack>
                    <Typography component='div' variant='h5'>{ticker.name}</Typography>
                    <Typography color='text.secondary'component='div' variant='subtitle1'>{ticker.source}</Typography>
                </Stack>

                <Typography color='text.secondary' component='div' variant='subtitle1'>{value}</Typography>
            </ListItemButton>
        </ListItem>
    );
}

export default React.memo(TickerItemBare);
