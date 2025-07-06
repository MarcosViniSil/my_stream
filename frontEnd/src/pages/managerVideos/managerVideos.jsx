import React, { useState, useEffect } from 'react';
import Pagination from '../../components/pagination/pagination'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import './managerVideos.css'
import { useNavigate } from "react-router-dom";

export default function ManagerVideos() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 
  const navigate = useNavigate();

  const redirectToSendNewVideo = () =>{
      navigate(`/upload`);
  }

  return (
    <>
        <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />
        <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open" : ""}`}>
        <Pagination/> 
        <div className='wrapButtonSendNewVideo'>
              <button onClick={redirectToSendNewVideo} id='buttonSendNewVideo'>Enviar novo vídeo</button>
        </div>
        
        </div>
    </>
  );
}
