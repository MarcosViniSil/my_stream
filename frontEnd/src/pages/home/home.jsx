import React, { useState } from 'react';
import VideosInitialPage from '../../components/videosInitialPage/videosInitialPage'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import './home.css'


export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 

  return (
    <>
        <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />
        <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open" : ""}`}>
        <VideosInitialPage/> 
        
        </div>
    </>
  );
}
