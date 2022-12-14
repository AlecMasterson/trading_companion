import React from 'react';
import {Container, Grid, Tab, Tabs} from '@mui/material';
import {createTheme, Theme, ThemeProvider} from '@mui/material/styles';
import darkScrollbar from '@mui/material/darkScrollbar';
import {SnackbarProvider} from 'notistack';
import MarketView from './components/MarketView';
import './app.css';

const DarkTheme: Theme = createTheme({
    components: {
        MuiCssBaseline: {
            styleOverrides: {body: darkScrollbar()}
        }
    },
    palette: {
        background: {default: '#201D39', paper: '#4E4868'},
        mode: 'dark',
        primary: {main: '#00C899'},
        secondary: {main: '#F4ECFF'}
    }
});

export default function App (): React.ReactElement {
    const [tab, setTab] = React.useState<number>(0);

    function onTabChange(_: React.SyntheticEvent, newTab: number): void {
        setTab(newTab);
    }

    return (
        <ThemeProvider theme={DarkTheme}>
            <SnackbarProvider>
                <Container>
                    <Grid item>
                        <Tabs className='main-tabs' centered={true} onChange={onTabChange} value={tab}>
                            <Tab label='Market View' />
                            <Tab label='Positions' />
                            <Tab label='Model Analysis' />
                            <Tab label='Admin Portal' />
                        </Tabs>
                    </Grid>

                    {tab === 0 && <MarketView />}
                </Container>
            </SnackbarProvider>
        </ThemeProvider>
    );
}
