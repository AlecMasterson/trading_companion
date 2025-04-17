import {Indicator} from './enums/Indicator';
import {ValueMap} from './ValueMap';

export interface IndicatorConfig {
  id: string;
  indicator: Indicator;
  options: ValueMap<any>;
}
