import React from 'react';
import {AppBar, Box, IconButton, Tab, Tabs, Toolbar, Typography} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

export default function Navbar(): React.ReactElement {
  const [tabActive, setTabActive] = React.useState<number>(0);

  function onChangeTab(_: React.SyntheticEvent, tabNew: number): void {
    setTabActive(tabNew);
  }

  return (
    <React.Fragment>
      <AppBar>
        <Toolbar>
          <IconButton sx={{display: {md: 'none'}}}>
            <MenuIcon />
          </IconButton>

          <Typography sx={{display: {xs: 'none', md: 'block'}, flexGrow: 1}} variant='h6'>
            Trading Companion
          </Typography>

          <Box sx={{display: {xs: 'none', md: 'block'}}}>
            <Tabs onChange={onChangeTab} value={tabActive}>
              <Tab label='Market View' />
              <Tab label='Research Portal' />
              <Tab label='About' />
            </Tabs>
          </Box>
        </Toolbar>
      </AppBar>

      <Toolbar />
    </React.Fragment>
  );
}
