import { React  } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import VideoUpload from './pages/upload/videoUpload'
import MetaDataPage from './pages/metadata/videoMetadata'
import ReceiveVideo from './components/recieveVideo/ReceiveVideo'
import ManagerVideos from '../src/pages/managerVideos/managerVideos'
import Search from '../src/pages/search/search'
import Home from '../src/pages/home/home'

import './App.css';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/perfil" element={<ReceiveVideo />} />
        <Route path="/busca" element={<Search />} />
        <Route path="/historico" element={<ReceiveVideo />} />
        <Route path="/uploads" element={<ManagerVideos />} />
         <Route path="/upload" element={<VideoUpload />} />
        <Route path="*" element={<VideoUpload />} />
        <Route path="/meta-dados" element={ <MetaDataPage/> }/> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;