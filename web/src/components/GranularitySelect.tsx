import React from 'react';
import {FormControl, InputLabel, MenuItem, MenuItemProps, Select} from '@mui/material';
import {get} from 'lodash';
import {Granularity} from '../types/enums/Granularity';

interface GranularitySelectProps {
  granularity: Granularity;
  setGranularity: (_: Granularity) => void;
}

const Options: React.ReactElement<MenuItemProps>[] =
  Object.entries(Granularity).map((entry: [string, Granularity]): React.ReactElement<MenuItemProps> => (
    <MenuItem key={entry[0]} value={entry[1]}>
      {entry[1]}
    </MenuItem>
  ));

export default function GranularitySelect(props: GranularitySelectProps): React.ReactElement<GranularitySelectProps> {
  function onChange(event: any): void {
    props.setGranularity(get(event, 'target.value', Granularity.DAY) as Granularity);
  }

  return (
    <FormControl sx={{minWidth: 200}}>
      <InputLabel id='label-granularity'>
        Granularity
      </InputLabel>

      <Select
          label='Granularity'
          labelId='label-granularity'
          onChange={onChange}
          value={props.granularity}
      >
        {Options}
      </Select>
    </FormControl>
  );
}
