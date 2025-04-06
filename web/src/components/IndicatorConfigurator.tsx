import React from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  MenuItemProps,
  Select
} from '@mui/material';
import {Indicator} from '../types/enums/Indicator';
import {IndicatorConfig} from '../types/IndicatorConfig';

interface IndicatorConfiguratorProps {
  onSubmit: (_: IndicatorConfig) => void;
}

export interface IndicatorConfiguratorRef {
  setIsOpen: (isOpen: boolean) => void;
}

const IndicatorOptions: React.ReactElement<MenuItemProps>[] =
  Object.entries(Indicator).map((entry: [string, Indicator]): React.ReactElement<MenuItemProps> => (
    <MenuItem key={entry[0]} value={entry[1]}>
      {entry[1]}
    </MenuItem>
  ));

const IndicatorConfigurator = React.forwardRef((props: IndicatorConfiguratorProps, ref: any): React.ReactElement<IndicatorConfiguratorProps> => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  const [selectedIndicator, setSelectedIndicator] = React.useState<Indicator>(Indicator.EMA);

  React.useImperativeHandle(ref, (): IndicatorConfiguratorRef => ({
    setIsOpen
  }));

  const onChangeIndicator: (event: {target: {value: string}}) => void =
    React.useCallback((event: {target: {value: string}}): void => {
      setSelectedIndicator(event.target.value as Indicator);
    }, [setSelectedIndicator]);

  const onClose: () => void =
    React.useCallback((): void => {
      setIsOpen(false);
    }, [setIsOpen]);

  const onSubmit: () => void = React.useCallback((): void => {
    props.onSubmit({
      data: [],
      id: selectedIndicator,
      indicator: selectedIndicator
    });

    onClose();
  }, [props.onSubmit, onClose, selectedIndicator]);

  return (
    <Dialog fullWidth onClose={onClose} open={isOpen}>
      <DialogTitle>
        Add Indicator
      </DialogTitle>

      <DialogContent>
        <FormControl fullWidth sx={{mt: 2}}>
          <InputLabel id='label-indicator'>
            Indicator
          </InputLabel>

          <Select label='Indicator' labelId='label-indicator' onChange={onChangeIndicator} value={selectedIndicator}>
            {IndicatorOptions}
          </Select>
        </FormControl>
      </DialogContent>

      <DialogActions>
        <Button color='secondary' onClick={onClose}>
          Cancel
        </Button>

        <Button color='primary' onClick={onSubmit} variant='contained'>
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
});

export default IndicatorConfigurator;
