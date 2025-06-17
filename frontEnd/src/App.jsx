import { React  } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import VideoUpload from './pages/upload/videoUpload'
import MetaDataPage from './pages/metadata/videoMetadata'
import ReceiveVideo from './components/recieveVideo/ReceiveVideo'
import VideoPlayer from './components/playVideo/playVideo'
import MetaData from './components/metaDatasVideo/metaData'
import Pagination from './components/pagination/pagination'

import './App.css';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<VideoPlayer />} />
        <Route path="/perfil" element={<ReceiveVideo />} />
        <Route path="/historico" element={<ReceiveVideo />} />
        <Route path="/upload" element={<VideoUpload />} />
        <Route path="*" element={<VideoUpload />} />
        <Route path="/meta-dados" element={ <MetaDataPage/> }/> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;