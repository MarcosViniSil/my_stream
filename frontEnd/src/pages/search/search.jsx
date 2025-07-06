import React, { useState } from 'react';
import ListSearch from '../../components/listSearch/listSearch'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import './search.css'


export default function Search() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 

  return (
    <>
        <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />
        <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open" : ""}`}>
        <ListSearch/> 
        
        </div>
    </>
  );
}
