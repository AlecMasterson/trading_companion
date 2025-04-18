import React from 'react';
import {CssBaseline} from '@mui/material';
import Grid from '@mui/material/Grid2';
import {Theme, ThemeProvider, createTheme} from '@mui/material/styles';
import darkScrollbar from '@mui/material/darkScrollbar';
import {SnackbarProvider, useSnackbar} from 'notistack';
import {setNotificationManager} from './NotificationManager';
import Navbar, {TabId} from './components/Navbar';
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
    background: {
      default: '#161A25',
      paper: '#161A25'
    },
    mode: 'dark',
    primary: {main: '#00C899'},
    // primary: {main: '#3C63FE'},
    secondary: {main: '#F4ECFF'}
  }
});

const SnackbarInitializer: React.MemoExoticComponent<() => null> = React.memo((): null => {
  const {enqueueSnackbar} = useSnackbar();

  React.useEffect((): void => {
    setNotificationManager(enqueueSnackbar);
  }, []);

  return null;
});

export default function App(): React.ReactElement {
  const [activeTabId, setActiveTabId] = React.useState<TabId>(TabId.MARKET_VIEW);

  return (
    <ThemeProvider theme={DarkTheme}>
      <CssBaseline />

      <SnackbarProvider anchorOrigin={{horizontal: 'right', vertical: 'top'}}>
        <SnackbarInitializer />
        <Navbar activeTabId={activeTabId} setActiveTabId={setActiveTabId} />

        <Grid className='fill-height' container spacing={2} sx={{m: 2}}>
          <Grid className='fill-height' offset={2} size={8}>
            {activeTabId === TabId.MARKET_VIEW ? <TickerView /> : null}
          </Grid>
        </Grid>
      </SnackbarProvider>
    </ThemeProvider>
  );
}
