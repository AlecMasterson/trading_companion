import React from 'react';
import {Card, CardContent, CardHeader, Collapse, Grid, IconButton} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {AnalysisConfigMap, iAnalysis, iAnalysisData} from '../../types/iAnalysis';
import {Granularity} from '../../types/enums/Granularity';
import {iCandle} from '../../types/iCandle';
import {Indicator} from '../../types/enums/Indicator';
import {iTickerHistoryRequest} from '../../types/iTickerHistoryRequest';
import {LearnedModel} from '../../types/enums/LearnedModel';
import {Source} from '../../types/enums/Source';
import AppApi from '../../api/AppApi';
import HistorySelection from './HistorySelection';
import IndicatorSelection from './IndicatorSelection';
import AnalysisChart from '../../charts/AnalysisChart';

interface iTickerHistoryState {
    analysisData: iAnalysisData[];
    candles: iCandle[];
    open: boolean;
    selected: iAnalysis | null;
    selectedOffset: iAnalysis | null;
}

export default class TickerHistory extends React.PureComponent<Record<string, never>, iTickerHistoryState> {

    override state: iTickerHistoryState = {
        analysisData: [],
        candles: [],
        open: false,
        selected: null,
        selectedOffset: null
    };

    public constructor(props: Record<string, never>) {
        super(props);

        this.getAnalysisIndicators = this.getAnalysisIndicators.bind(this);
        this.getTickerHistory = this.getTickerHistory.bind(this);
        this.onChangeIndicators = this.onChangeIndicators.bind(this);
    }

    public override componentDidMount(): void {
        this.getTickerHistory({
            source: Source.COINBASE,
            ticker: "BTC-USD",
            granularity: Granularity.DAY_1,
            startDateTime: "2023-01-01 00:00:00",
            endDateTime: "2023-04-10 00:00:00"
        });
    }

    public async getAnalysisIndicators(): Promise<void> {
        const analysisData: iAnalysisData[] = await AppApi.getAnalysisIndicators(this.state.candles);
        this.setState({analysisData});
    }

    public async getAnalysisLearnedModel(learnedModel: LearnedModel): Promise<Array<iAnalysisData>> {
        return await AppApi.getAnalysisLearnedModel(learnedModel, this.state.candles);
    }

    public async getTickerHistory(request: iTickerHistoryRequest): Promise<void> {
        const candles: iCandle[] = await AppApi.getTickerHistory(request.source, request.ticker, request.granularity, request.startDateTime, request.endDateTime);
        this.setState({candles}, this.getAnalysisIndicators);
    }

    protected async onChangeIndicators(selected: Indicator | LearnedModel): Promise<void> {
        let data: any;
        if (selected in Indicator) {
            data = this.state.analysisData;
        } else {
            data = await this.getAnalysisLearnedModel(selected as LearnedModel);
        }

        if (AnalysisConfigMap[selected].offset) {
            this.setState({selectedOffset: {data, type: selected}});
        } else {
            this.setState({selected: {data, type: selected}});
        }
    }

    public override render(): React.ReactElement {
        return (
            <Grid container spacing={2} style={{display: 'flex', flexGrow: '1'}}>
                <Grid item xs={8}>
                    <Card variant='outlined'>
                        <CardHeader
                            action={
                                <IconButton aria-label="settings" onClick={() => this.setState({open: !this.state.open})}>
                                    <ExpandMoreIcon />
                                </IconButton>
                            }
                            subheader='Ticker History Selection'
                        />
                        <Collapse in={this.state.open}>
                            <CardContent>
                                <HistorySelection loading={this.state.loading} onSubmit={this.getTickerHistory}/>
                            </CardContent>
                        </Collapse>
                    </Card>
                </Grid>

                <Grid item xs={4}>
                    <IndicatorSelection onChange={this.onChangeIndicators}/>
                </Grid>

                <Grid item id='test' xs={12} style={{display: 'flex', flexDirection: 'column', flexGrow: '1'}}>
                    <AnalysisChart
                        candles={this.state.candles}
                        selected={this.state.selected}
                        selectedOffset={this.state.selectedOffset}
                    />
                </Grid>
            </Grid>
        );
    }
}
