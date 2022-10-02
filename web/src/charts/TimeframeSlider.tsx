import React from 'react';
import {Slider} from '@mui/material';
import {isEqual} from 'lodash';
import {iCandle} from '../types/iCandle';
import TimeUtil from '../utils/TimeUtil';

interface iTimeframeSliderProps {
    activity: iCandle[];
    minDistance: number;
    setFilteredActivity: (activity: iCandle[]) => void;
}

function filterTimeframe(activity: iCandle[], timeframe: number[]): iCandle[] {
    return activity.filter((candle: iCandle): boolean => {
        return candle.candle_timestamp >= timeframe[0] && candle.candle_timestamp <= timeframe[1];
    });
}

function getTimeframe(activity: iCandle[], minDistance: number): number[] {
    if (activity.length === 0) {
        return [];
    }

    const minIndex: number = Math.max(0, activity.length - minDistance);
    return [activity[minIndex].candle_timestamp, activity[activity.length - 1].candle_timestamp];
}

const MaxDistance: number = 86400 * 1000;

function TimeframeSlider (props: iTimeframeSliderProps): React.ReactElement {
    const {activity, minDistance, setFilteredActivity} = props;
    const [timeframe, setTimeframe] = React.useState<number[]>(getTimeframe(props.activity, props.minDistance));

    const updateTimeframe = React.useCallback((newTimeframe: number[]): void => {
        if (isEqual(timeframe, newTimeframe)) {
            return;
        }

        setTimeframe(newTimeframe);
        setFilteredActivity(filterTimeframe(activity, newTimeframe));
    }, [activity, setFilteredActivity, timeframe]);

    React.useEffect((): void => {
        updateTimeframe(getTimeframe(activity, minDistance));
    }, [activity, minDistance, updateTimeframe]);

    function onChangeSlider(_: Event, newValue: number | number[], activeThumb: number): void {
        if (!Array.isArray(newValue)) {
            return;
        }

        let newTimeframe: number[] = [...timeframe];
        if (activeThumb === 0) {
            newTimeframe = [Math.min(newValue[0], timeframe[1] - (MaxDistance * props.minDistance)), timeframe[1]];
        } else {
            newTimeframe = [timeframe[0], Math.max(newValue[1], timeframe[0] + (MaxDistance * props.minDistance))];
        }

        updateTimeframe(newTimeframe);
    }

    return (
        <Slider
            disableSwap
            max={props.activity.length && props.activity[props.activity.length - 1].candle_timestamp}
            min={props.activity.length && props.activity[0].candle_timestamp}
            name='Timeframe Selection'
            onChange={onChangeSlider}
            value={timeframe}
            valueLabelDisplay='auto'
            valueLabelFormat={TimeUtil.timestampToDateString}
        />
    );
}

export default React.memo(TimeframeSlider);
