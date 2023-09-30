import React from 'react';
import {
    Button,
    FormControl,
    Grid,
    InputLabel,
    MenuItem,
    MenuItemProps,
    Select,
    SelectChangeEvent,
    TextField
} from '@mui/material';
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {DateTimePicker} from '@mui/x-date-pickers/DateTimePicker';
import {LocalizationProvider} from '@mui/x-date-pickers/LocalizationProvider';
import {Granularity} from '../../types/enums/Granularity';
import {iTickerHistoryRequest} from '../../types/iTickerHistoryRequest';
import {Source} from '../../types/enums/Source';

const FORMAT_DATE = 'YYYY-MM-DD HH:mm:ss';

type DateChangeEvent = {format: (format: string) => string} | null;

interface iHistorySelectionProps {
    loading: boolean;
    onSubmit: (request: iTickerHistoryRequest) => void;
}

function GetMenuItems_Granularity(): Array<React.ReactElement<MenuItemProps>> {
    return Object.entries(Granularity).map(([key, value]): React.ReactElement<MenuItemProps> => (
        <MenuItem key={key} value={value}>{value}</MenuItem>
    ));
}

function GetMenuItems_Source(): Array<React.ReactElement<MenuItemProps>> {
    return Object.entries(Source).map(([key, value]): React.ReactElement<MenuItemProps> => (
        <MenuItem key={key} value={key}>{value}</MenuItem>
    ));
}

export default class HistorySelection extends React.PureComponent<iHistorySelectionProps, iTickerHistoryRequest> {

    override state: iTickerHistoryRequest = {
        endDateTime: '',
        granularity: Granularity.DAY_1,
        source: Source.COINBASE,
        startDateTime: '',
        ticker: ''
    };

    public constructor(props: iHistorySelectionProps) {
        super(props);

        this.onChange_DateEnd = this.onChange_DateEnd.bind(this);
        this.onChange_DateStart = this.onChange_DateStart.bind(this);
        this.onChange_Granularity = this.onChange_Granularity.bind(this);
        this.onChange_Source = this.onChange_Source.bind(this);
        this.onChange_Ticker = this.onChange_Ticker.bind(this);

        this.onSubmit = this.onSubmit.bind(this);
    }

    protected isInvalid(): boolean {
        return this.state.ticker === '' || this.state.startDateTime === '' || this.state.endDateTime === '';
    }

    protected onChange_DateEnd(event: DateChangeEvent): void {
        const date: string = event ? event.format(FORMAT_DATE) : '';

        this.setState({endDateTime: date !== 'Invalid Date' ? date : ''});
    }

    protected onChange_DateStart(event: DateChangeEvent): void {
        const date: string = event ? event.format(FORMAT_DATE) : '';

        this.setState({startDateTime: date !== 'Invalid Date' ? date : ''});
    }

    protected onChange_Granularity(event: SelectChangeEvent): void {
        this.setState({granularity: event.target.value as Granularity});
    }

    protected onChange_Source(event: SelectChangeEvent): void {
        this.setState({source: event.target.value as Source});
    }

    protected onChange_Ticker(event: {target: {value: string}}): void {
        this.setState({ticker: event.target.value});
    }

    protected onSubmit(): void {
        this.props.onSubmit(this.state);
    }

    public override render(): React.ReactElement {
        return (
            <Grid container spacing={2}>
                <Grid item xs={4}>
                    <FormControl fullWidth>
                        <InputLabel id='label-source'>Source</InputLabel>

                        <Select
                            children={GetMenuItems_Source()}
                            label='Source'
                            labelId='label-source'
                            onChange={this.onChange_Source}
                            value={this.state.source}
                        />
                    </FormControl>
                </Grid>

                <Grid item xs={4}>
                    <FormControl fullWidth>
                        <TextField
                            label='Ticker'
                            onChange={this.onChange_Ticker}
                            value={this.state.ticker}
                            variant='outlined'
                        />
                    </FormControl>
                </Grid>

                <Grid item xs={4}>
                    <FormControl fullWidth>
                        <InputLabel id='label-granularity'>Granularity</InputLabel>

                        <Select
                            children={GetMenuItems_Granularity()}
                            label='Granularity'
                            labelId='label-granularity'
                            onChange={this.onChange_Granularity}
                            value={this.state.granularity}
                        />
                    </FormControl>
                </Grid>

                <Grid item xs={4}>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DateTimePicker
                            label='Start Date Time'
                            onChange={this.onChange_DateStart}
                            sx={{width: '100%'}}
                        />
                    </LocalizationProvider>
                </Grid>

                <Grid item xs={4}>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DateTimePicker
                            label='End Date Time'
                            onChange={this.onChange_DateEnd}
                            sx={{width: '100%'}}
                        />
                    </LocalizationProvider>
                </Grid>

                <Grid item xs={4}>
                    <Button
                        children='Submit'
                        disabled={this.isInvalid()}
                        fullWidth
                        onClick={this.onSubmit}
                        sx={{height: '100%'}}
                        variant='contained'
                    />
                </Grid>
            </Grid>
        );
    }
}
