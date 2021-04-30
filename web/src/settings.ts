import {createMuiTheme, Theme} from '@material-ui/core';

const DarkTheme: Theme = createMuiTheme({
    palette: {
        error: {main: '#f44336'},
        info: {main: '#2196f3'},
        primary: {main: '#90caf9'},
        secondary: {main: '#f48fb1'},
        success: {main: '#4caf50'},
        type: 'dark',
        warning: {main: '#ff9800'}
    },
    typography: {fontFamily: '"Unica One", sans-serif'}
});

export const Settings = {
    DarkTheme
};
