import {Indicator} from './enums/Indicator';

export interface IndicatorConfig {
    id: string;
    indicator: Indicator;
    period?: number;
    periodFast?: number;
    periodSignal?: number;
    periodSlow?: number;
}
