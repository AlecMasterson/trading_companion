import React from 'react';
import {Settings} from './settings';
import {Container, Theme, ThemeProvider} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';
import {NotificationProvider} from './hooks/NotificationProvider';
import {AppDrawer} from './nav/AppDrawer';
import {BrowserRouter, Route} from 'react-router-dom';
import {Charts} from './pages/Charts';
import {Positions} from './pages/Positions';
import './app.css';

const Styles: Record<string, string> = makeStyles((theme: Theme) => ({
    toolbar: theme.mixins.toolbar
}))();

export function App (): React.ReactElement {
    return (
        <ThemeProvider theme={Settings.DarkTheme}>
            <NotificationProvider>
                <AppDrawer/>

                <div className={Styles.toolbar}/>

                <Container>
                    <BrowserRouter>
                        <Route exact path='/charts' component={Charts}/>
                        <Route exact path='/positions' component={Positions}/>
                    </BrowserRouter>
                </Container>
            </NotificationProvider>
        </ThemeProvider>
    );
}
