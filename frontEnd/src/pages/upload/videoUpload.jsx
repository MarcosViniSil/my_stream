import React, { useState } from 'react';
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import ReceiveVideo from '../../components/recieveVideo/ReceiveVideo'

import './videoUpload.css'

function VideoUpload() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 




  return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendVideo ${isMenuOpen ? "menu-open" : ""}`}>
        <h1 className="title">Envie seu Vídeo</h1>
        <ReceiveVideo />
      </div>
    </>
  );


}

export default VideoUpload;

