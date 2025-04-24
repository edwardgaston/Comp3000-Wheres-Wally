import React from 'react';
import { Box, CssBaseline, Toolbar, AppBar, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import UploadForm from './components/UploadForm'; // Import the UploadForm component

const theme = createTheme(); // Default Material-UI theme

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
        <CssBaseline />
        {/* Top AppBar */}
        <AppBar
          position="fixed"
          sx={{
            zIndex: (theme) => theme.zIndex.drawer + 1,
            backgroundColor: '#FF8C00', // Dark orange color
          }}
        >
          <Toolbar>
            <Typography variant="h6" noWrap>
              Where's Wally Detector
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, padding: 3 }}>
          <Toolbar />
          {/* Add UploadForm Component */}
          <UploadForm />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;