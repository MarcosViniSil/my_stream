import React, { useState } from 'react';
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import ProfileComponent from '../../components/profileComponent/profileComponent'

function Profile() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 

  return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendVideo ${isMenuOpen ? "menu-open" : ""}`}>
        <h1 className="title">Perfil</h1>
        <ProfileComponent />
      </div>
    </>
  );


}

export default Profile;

