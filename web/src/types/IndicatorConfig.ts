import {Indicator} from './enums/Indicator';
import {IndicatorCandle} from './IndicatorCandle';

export interface IndicatorConfig {
    data: IndicatorCandle[];
    id: string;
    indicator: Indicator;
    period?: number;
    periodFast?: number;
    periodSignal?: number;
    periodSlow?: number;
}
