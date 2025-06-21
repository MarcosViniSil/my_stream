import React, { useState, useEffect } from 'react';
import Pagination from '../../components/pagination/pagination'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import './managerVideos.css'

export default function ManagerVideos() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 
  return (
    <>
        <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />
        <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open" : ""}`}>
        <Pagination/> 
        </div>
    </>
  );
}
