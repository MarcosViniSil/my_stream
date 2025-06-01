import { useState } from 'react';
import VideoUpload from './pages/upload/videoUpload'
import ReceiveVideo from './components/recieveVideo/ReceiveVideo'
import { BrowserRouter, Routes, Route } from "react-router-dom";

import './App.css';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ReceiveVideo />} />
        <Route path="/perfil" element={<ReceiveVideo />} />
        <Route path="/historico" element={<ReceiveVideo />} />
        <Route path="/upload" element={<VideoUpload />} />
        <Route path="*" element={<VideoUpload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;