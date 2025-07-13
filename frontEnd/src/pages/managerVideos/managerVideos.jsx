import React, { useState, useEffect } from 'react';
import Pagination from '../../components/pagination/pagination'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import {isCookieValid} from '../../service/videoService.js'
import './managerVideos.css'
import { useNavigate } from "react-router-dom";

export default function ManagerVideos() {
  const [isMenuOpen, setIsMenuOpen] = useState(true); 
  const [userHasLogin, setUserHasLogin] = useState(null); 
  const navigate = useNavigate();
    
  useEffect(() => {
      const getUserDatas = async () => {
        try {
          await isCookieValid();
          setUserHasLogin(true);
        } catch (err) {
          console.log(err);
          if (err.status === 422 || err.status === 401) {
            setUserHasLogin(false);
          } else {
            setUserHasLogin(false);
          }
        }
      };
  
      getUserDatas();
    }, []);
  
    const redirectToSendNewVideo = () =>{
      navigate(`/upload`);
  }
  if (userHasLogin === null) {
    return <p style={{ color: "white", textAlign: "center" }}>Carregando...</p>;
  }

  if (!userHasLogin) {
    return (
      <div className='wrapMessageLogin'>
        <h3>Realize o login para poder enviar seu vídeo</h3>
        <a href="/login">login</a>
      </div>
    );
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
