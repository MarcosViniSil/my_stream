import React, { useState } from 'react';
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import Login from '../../components/login/login'

function LoginPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 

  return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendVideo ${isMenuOpen ? "menu-open" : ""}`}>
        <h1 className="title">Faça seu Login</h1>
        <Login />
      </div>
    </>
  );


}

export default LoginPage;

