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
  Select,
  SelectChangeEvent
} from '@mui/material';
import {Indicator} from '../../types/enums/Indicator';
import {IndicatorConfig} from '../../types/IndicatorConfig';
import {ValueMap} from '../../types/ValueMap';
import CustomInputs, {CustomInputsRef, getIndicatorId} from './CustomInputs';

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
  const refCustomInputs: React.RefObject<CustomInputsRef> = React.useRef<CustomInputsRef>(null);

  const [indicator, setIndicator] = React.useState<Indicator>(Indicator.EMA);
  const [isOpen, setIsOpen] = React.useState<boolean>(false);

  React.useImperativeHandle(ref, (): IndicatorConfiguratorRef => ({setIsOpen}));

  const onChange: (value: string) => void = React.useCallback((value: string): void => {
    setIndicator(value as Indicator);
  }, []);

  const onClose: () => void = React.useCallback((): void => {
    setIndicator(Indicator.EMA);
    setIsOpen(false);
  }, []);

  const onSubmit: () => void = React.useCallback((): void => {
    const values: ValueMap<number> = refCustomInputs.current?.values ?? {};

    props.onSubmit({
      id: getIndicatorId(indicator, values),
      indicator,
      ...values
    });

    onClose();
  }, [indicator, refCustomInputs]);

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

          <Select
            label='Indicator'
            labelId='label-indicator'
            onChange={(event: SelectChangeEvent): void => onChange(event.target.value)}
            value={indicator}
          >
            {IndicatorOptions}
          </Select>

          <CustomInputs
            indicator={indicator}
            ref={refCustomInputs}
          />
        </FormControl>
      </DialogContent>

      <DialogActions>
        <Button color='secondary' onClick={onClose} variant='outlined'>
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
