import React from 'react';
import {TextField} from '@mui/material';
import {get} from 'lodash';
import {Indicator} from '../../types/enums/Indicator';
import {ValueMap} from '../../types/ValueMap';

interface CustomInputsProps {
  indicator: Indicator;
}

export interface CustomInputsRef {
  values: ValueMap<number>;
}

interface InputConfig {
  default: number;
  field: string;
  label: string;
}

const InputConfigMap: {[key in Indicator]: InputConfig[]} = {
  [Indicator.EMA]: [
    {default: 30, field: 'period', label: 'Period'}
  ],
  [Indicator.MACD]: [
    {default: 12, field: 'periodFast', label: 'Period Fast'},
    {default: 26, field: 'periodSlow', label: 'Period Slow'},
    {default: 9, field: 'periodSignal', label: 'Period Signal'}
  ],
  [Indicator.RSI]: [
    {default: 14, field: 'period', label: 'Period'}
  ],
  [Indicator.SMA]: [
    {default: 30, field: 'period', label: 'Period'}
  ],
  [Indicator.STOCH]: []
};

export function getIndicatorId(indicator: Indicator, values: ValueMap<number>): string {
  const formatted: string = InputConfigMap[indicator].map((config: InputConfig): number | string => get(values, config.field, '')).join(',');
  return indicator + `(${formatted})`;
}

const CustomInputs = React.memo(React.forwardRef((props: CustomInputsProps, ref: any): React.ReactElement<CustomInputsProps>[] => {
  const [values, setValues] = React.useState<ValueMap<number>>({});

  React.useImperativeHandle(ref, (): CustomInputsRef => ({values}), [values]);

  React.useEffect((): void => {
    setValues(InputConfigMap[props.indicator].reduce((temp: ValueMap<number>, config: InputConfig): ValueMap<number> => ({
      ...temp,
      [config.field]: config.default
    }), {}));
  }, [props.indicator]);

  const onChange: (_: InputConfig, valueStr: string) => void = React.useCallback((config: InputConfig, valueStr: string): void => {
    const value: number = valueStr === '' ? 0 : parseInt(valueStr);
    if (isNaN(value)) {
      return;
    }

    setValues((temp: ValueMap<number>): ValueMap<number> => ({...temp, [config.field]: value}));
  }, []);

  return InputConfigMap[props.indicator].map((config: InputConfig): React.ReactElement => (
    <TextField
      key={config.field}
      label={config.label}
      onChange={(event: React.ChangeEvent<HTMLInputElement>): void => onChange(config, event.target.value)}
      sx={{mt: 2}}
      value={get(values, config.field, 0).toString()}
    />
  ));
}));

export default CustomInputs;
