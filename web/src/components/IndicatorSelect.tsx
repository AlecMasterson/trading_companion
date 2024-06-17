import React from 'react';
import {FormControl, FormControlProps, InputLabel, MenuItem, MenuItemProps, Select} from '@mui/material';
import {get} from 'lodash';
import {Indicator} from '../types/enums/Indicator';

interface IndicatorSelectProps {
  indicators: Indicator[];
  setIndicators: (_: Indicator[]) => void;
}

const Options: React.ReactElement<MenuItemProps>[] =
  Object.entries(Indicator).map((entry: [string, Indicator]): React.ReactElement<MenuItemProps> => (
    <MenuItem key={entry[0]} value={entry[1]}>
      {entry[1]}
    </MenuItem>
  ));

export default function IndicatorSelect(props: IndicatorSelectProps): React.ReactElement<FormControlProps> {
  function onChange(event: any): void {
    props.setIndicators(get(event, 'target.value', []));
  }

  return (
    <FormControl sx={{minWidth: 200}}>
      <InputLabel id='label-indicator'>
        Indicator
      </InputLabel>

      <Select
          label='Indicator'
          labelId='label-indicator'
          multiple
          onChange={onChange}
          value={props.indicators}
      >
        {Options}
      </Select>
    </FormControl>
  );
}
