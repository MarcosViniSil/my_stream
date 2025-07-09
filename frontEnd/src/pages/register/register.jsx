import React, { useState } from 'react';
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import RegisterComponent from '../../components/signUp/signUp'

import './register.css'

function Register() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 

  return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendVideo ${isMenuOpen ? "menu-open" : ""}`}>
        <h1 className="title">Faça seu cadastro</h1>
        <RegisterComponent />
      </div>
    </>
  );


}

export default Register;

