import React, { useState } from 'react';
import { Drawer, IconButton, Box, CssBaseline, Toolbar, AppBar, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import UploadForm from './components/UploadForm'; // Import the UploadForm component

const theme = createTheme(); // Default Material-UI theme

function App() {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

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
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={toggleSidebar}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap>
              Where's Wally Detector
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Sidebar */}
        <Drawer
          variant="persistent"
          open={isSidebarOpen}
          sx={{
            '& .MuiDrawer-paper': {
              width: isSidebarOpen ? 240 : 60, // Adjust width based on state
              transition: 'width 0.3s',
              backgroundColor: '#ffffff',
              overflowX: 'hidden',
            },
          }}
        >
          <Toolbar>
            <IconButton onClick={toggleSidebar}>
              {isSidebarOpen ? <ChevronLeftIcon /> : <MenuIcon />}
            </IconButton>
          </Toolbar>
          <Box sx={{ padding: 2 }}>
            {isSidebarOpen && (
              <>
                <Typography variant="h6">Sidebar Content</Typography>
                <Typography variant="body1">Add your navigation or options here.</Typography>
              </>
            )}
          </Box>
        </Drawer>

        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, padding: 3 }}>
          <Toolbar />
          <Typography variant="h4" gutterBottom>
            Welcome to Where's Wally Detector
          </Typography>
          {/* Add UploadForm Component */}
          <UploadForm />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;