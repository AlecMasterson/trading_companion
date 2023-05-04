import React from 'react';
import {FormControl, InputLabel, ListSubheader, MenuItem, MenuItemProps, Select} from '@mui/material';
import {Indicator} from '../../types/enums/Indicator';
import {LearnedModel} from '../../types/enums/LearnedModel';

function GetMenuItems_Indicators(): Array<React.ReactElement<MenuItemProps>> {
    return Object.entries(Indicator).map(([key, value]): React.ReactElement<MenuItemProps> => (
        <MenuItem key={key} value={value}>{value}</MenuItem>
    ));
}

function GetMenuItems_LearnedModels(): Array<React.ReactElement<MenuItemProps>> {
    return Object.entries(LearnedModel).map(([key, value]): React.ReactElement<MenuItemProps> => (
        <MenuItem key={key} value={value}>{value}</MenuItem>
    ));
}

interface IndicatorSelectionProps {
    onChange: (selected: Indicator | LearnedModel) => void;
}

interface IndicatorSelectionState {
    selected: Indicator;
}

export default class IndicatorSelection extends React.PureComponent<IndicatorSelectionProps, IndicatorSelectionState> {

    override state: IndicatorSelectionState = {
        selected: Indicator.MACD
    };

    public constructor(props: IndicatorSelectionProps) {
        super(props);

        this.onChange = this.onChange.bind(this);
    }

    protected onChange(event: any): void {
        this.setState({selected: event.target.value});
        this.props.onChange(event.target.value);
    }

    public override render(): React.ReactElement {
        return (
            <FormControl fullWidth>
                <InputLabel id='label-analysis'>Indicators & Learned Models</InputLabel>

                <Select
                    children={([
                        <ListSubheader key='subheader-indicators'>TA Indicators</ListSubheader>,
                        GetMenuItems_Indicators(),
                        <ListSubheader key='subheader-learned-models'>Learned Models</ListSubheader>,
                        GetMenuItems_LearnedModels()
                    ])}
                    label='Indicators & Learned Models'
                    labelId='label-analysis'
                    onChange={this.onChange}
                    value={this.state.selected}
                />
            </FormControl>
        );
    }
}
