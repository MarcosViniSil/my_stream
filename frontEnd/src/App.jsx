import { React  } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import VideoUpload from './pages/upload/videoUpload'
import MetaDataPage from './pages/metadata/videoMetadata'

import ManagerVideos from '../src/pages/managerVideos/managerVideos'
import Search from '../src/pages/search/search'
import Home from '../src/pages/home/home'
import Watch from '../src/pages/watch/watch'
import NotFound from '../src/pages/notFound/notFound'
import History from '../src/pages/history/history'
import Register from './pages/register/register'
import LoginPage from './pages/login/login'
import Profile from './pages/profile/profile'
import RecoverPassword from './pages/recoverPassword/recoverPassword'
import { AccessibleProvider } from './context/AccessibleContext';
import { ThemeProvider } from './context/themeContext';
import './App.css';

function App() {

  return (
    <ThemeProvider>
    <AccessibleProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={ <Register/> }/> 
        <Route path="/login" element={ <LoginPage/> }/> 
        <Route path="/" element={<Home />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/busca" element={<Search />} />
        <Route path="/history" element={<History />} />
        <Route path="/uploads" element={<ManagerVideos />} />
        <Route path="/upload" element={<VideoUpload />} />
        <Route path="*" element={<NotFound />} />
        <Route path="/meta-dados" element={ <MetaDataPage/> }/> 
        <Route path="/watch" element={ <Watch/> }/> 
        <Route path="/password" element={ <RecoverPassword/> }/> 
        
      </Routes>
    </BrowserRouter>
    </AccessibleProvider>
    </ThemeProvider>
  );
}

export default App;