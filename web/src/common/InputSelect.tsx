import React from 'react';
import {FormControl, InputLabel, Select} from '@material-ui/core';

export interface InputSelectProps {
    label: string;
    onChange: (value: any) => void;
    options: any[];
    value: any;
}

export function InputSelect (props: InputSelectProps) {
    const labelId: string = `label-${props.label}`;
    const options = props.options.map((option: any) => <option key={option} value={option}>{option}</option>);

    return (
        <FormControl variant='outlined'>
            <InputLabel children={props.label} id={labelId}/>

            <Select
                children={options}
                label={props.label}
                labelId={labelId}
                native
                onChange={(event) => props.onChange(event.target.value)}
                value={props.value}
            />
        </FormControl>
    );
}
