import React from 'react';
import {Card, CardContent, FormControl, Grid, MenuItem, Select} from '@mui/material';
import {set} from 'lodash';
import {iTickerData} from '../types/iTickerData';
import {iTickerSummary} from '../types/iTickerSummary';
import AppApi from '../api/AppApi';
import TickerSelection from './ticker-selection/TickerSelection';
import MarketChart from '../charts/MarketChart';

type ValueMap<T> = {[key: string]: T};

interface iMarketViewState {
    selectedTicker: iTickerSummary | null;
    tickerData: ValueMap<iTickerData>;
    tickerSummaries: iTickerSummary[];
}

function getTickerKey(ticker: iTickerSummary): string {
    return ticker.source + '-' + ticker.name;
}

export default class MarketView extends React.PureComponent<Record<string, never>, iMarketViewState> {

    override state: iMarketViewState = {selectedTicker: null, tickerData: {}, tickerSummaries: []};

    public constructor(props: Record<string, never>) {
        super(props);

        this.getSelectedTickerData = this.getSelectedTickerData.bind(this);
        this.selectTicker = this.selectTicker.bind(this);
    }

    public override async componentDidMount(): Promise<void> {
        const summaries: iTickerSummary[] = await AppApi.getTickerSummary();
        this.setState({selectedTicker: null, tickerSummaries: summaries});
    }

    public getSelectedTickerData(): iTickerData | null {
        if (!this.state.selectedTicker) {
            return null;
        }

        return this.state.tickerData[getTickerKey(this.state.selectedTicker)];
    }

    public async selectTicker(ticker: iTickerSummary): Promise<void> {
        const existing: ValueMap<iTickerData> = {...this.state.tickerData};
        const key: string = getTickerKey(ticker);

        if (!(key in this.state.tickerData)) {
            const data: iTickerData | null = await AppApi.getTickerData(ticker.name);
            set(existing, key, data);
        }

        this.setState({selectedTicker: ticker, tickerData: existing});
    }

    public override render(): React.ReactElement {
        const selectedTickerData: iTickerData | null = this.getSelectedTickerData();

        return (
            <Grid container spacing={2}>
                <Grid id='ticker-selection' item xs={3}>
                    <Card variant='outlined'>
                        <CardContent>
                            <TickerSelection
                                onSelect={this.selectTicker}
                                tickers={this.state.tickerSummaries}
                            />
                        </CardContent>
                    </Card>
                </Grid>

                {selectedTickerData !== null && (
                    <Grid item xs={9}>
                        <Card variant='outlined'>
                            <CardContent>
                                <FormControl variant='standard' sx={{marginRight: '16px'}}>
                                    <Select label='Granularity' value='DAILY'>
                                        <MenuItem value='DAILY'>DAILY</MenuItem>
                                    </Select>
                                </FormControl>
                                <FormControl variant='standard'>
                                    <Select label='Granularity'>
                                        <MenuItem>DAILY</MenuItem>
                                    </Select>
                                </FormControl>

                                <MarketChart candles={selectedTickerData.candles} />
                            </CardContent>
                        </Card>
                    </Grid>
                )}
            </Grid>
        );
    }
}
