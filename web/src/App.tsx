import React from 'react';
import {Box, CssBaseline} from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';
import {createTheme, Theme, ThemeProvider} from '@mui/material/styles';
import darkScrollbar from '@mui/material/darkScrollbar';
import {SnackbarProvider} from 'notistack';
import NavBar from './NavBar';
import TickerView from './components/TickerView';
import './app.css';

const DarkTheme: Theme = createTheme({
  components: {
    MuiCssBaseline: {
      styleOverrides: {body: darkScrollbar()}
    }
  },
  palette: {
    // background: {default: '#201D39', paper: '#4E4868'},
    background: {default: '#161A25', paper: '#161A25'},
    mode: 'dark',
    primary: {main: '#00C899'},
    // primary: {main: '#3C63FE'},
    secondary: {main: '#F4ECFF'}
  }
});

export default function App(): React.ReactElement {
  return (
    <ThemeProvider theme={DarkTheme}>
      <CssBaseline />

      <SnackbarProvider>
        <NavBar />

        <Box sx={{m: 2}}>
          <Grid container spacing={2}>
            <Grid xs={10} xsOffset={1}>
              <TickerView />
            </Grid>
          </Grid>
        </Box>
      </SnackbarProvider>
    </ThemeProvider>
  );
}
