import React from 'react';
import {AppBar, Tab, Tabs, Toolbar, Typography} from '@mui/material';

export enum TabId {
  MARKET_VIEW = 'Market View',
  SCREENER = 'Screener'
}

interface NavbarProps {
  activeTabId: TabId;
  setActiveTabId: (_: TabId) => void;
}

const TabIdOrder: TabId[] = [TabId.MARKET_VIEW, TabId.SCREENER];

export default function Navbar(props: NavbarProps): React.ReactElement<NavbarProps> {
  const onChangeTabId: (event: any, index: number) => void = React.useCallback((_: any, index: number): void => {
    props.setActiveTabId(TabIdOrder[index]);
  }, []);

  return (
    <React.Fragment>
      <AppBar>
        <Toolbar>
          <Typography sx={{flexGrow: 1}} variant='h6'>
            Trading Companion
          </Typography>

          <Tabs onChange={onChangeTabId} value={TabIdOrder.indexOf(props.activeTabId)}>
            <Tab label='Market View' />
            <Tab label='Screener' />
          </Tabs>
        </Toolbar>
      </AppBar>

      <Toolbar />
    </React.Fragment>
  );
}
