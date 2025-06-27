import { React  } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import VideoUpload from './pages/upload/videoUpload'
import MetaDataPage from './pages/metadata/videoMetadata'
import ReceiveVideo from './components/recieveVideo/ReceiveVideo'
import ManagerVideos from '../src/pages/managerVideos/managerVideos'
import Search from '../src/pages/search/search'
import Home from '../src/pages/home/home'
import Watch from '../src/pages/watch/watch'
import NotFound from '../src/pages/notFound/notFound'

import './App.css';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/profile" element={<ReceiveVideo />} />
        <Route path="/busca" element={<Search />} />
        <Route path="/history" element={<ReceiveVideo />} />
        <Route path="/uploads" element={<ManagerVideos />} />
         <Route path="/upload" element={<VideoUpload />} />
        <Route path="*" element={<NotFound />} />
        <Route path="/meta-dados" element={ <MetaDataPage/> }/> 
        <Route path="/watch" element={ <Watch/> }/> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;