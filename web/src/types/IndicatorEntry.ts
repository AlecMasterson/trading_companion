import {Indicator} from './enums/Indicator';

export interface IndicatorEntry {
    data: (number | null)[];
    id: string;
    indicator: Indicator;
}
