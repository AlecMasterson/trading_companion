import React from 'react';
import {FormControl, InputLabel, MenuItem, MenuItemProps, Select, SelectChangeEvent} from '@mui/material';
import {Granularity} from '../types/enums/Granularity';

interface GranularitySelectProps {
  granularity: Granularity;
  isLoading: boolean;
  setGranularity: (_: Granularity) => void;
}

const GranularityOptions: React.ReactElement<MenuItemProps>[] =
  Object.entries(Granularity).map((entry: [string, Granularity]): React.ReactElement<MenuItemProps> => (
    <MenuItem key={entry[0]} value={entry[1]}>
      {entry[1]}
    </MenuItem>
  ));

export default function GranularitySelect(props: GranularitySelectProps): React.ReactElement<GranularitySelectProps> {
  const onChange: (value: string) => void = React.useCallback((value: string): void => {
    props.setGranularity(value as Granularity);
  }, [props.setGranularity]);

  return (
    <FormControl sx={{minWidth: 200}}>
      <InputLabel id='label-granularity'>
        Granularity
      </InputLabel>

      <Select
        disabled={props.isLoading}
        label='Granularity'
        labelId='label-granularity'
        onChange={(event: SelectChangeEvent): void => onChange(event.target.value)}
        value={props.granularity}
      >
        {GranularityOptions}
      </Select>
    </FormControl>
  );
}
