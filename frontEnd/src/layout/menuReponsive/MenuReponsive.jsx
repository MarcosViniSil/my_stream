import React, { useState, useEffect } from 'react';
import { GiHamburgerMenu } from 'react-icons/gi';
import { FaHome } from "react-icons/fa";
import { CgProfile } from "react-icons/cg";
import { FaHistory } from "react-icons/fa";
import { FaCloudUploadAlt } from "react-icons/fa";
import { Link, useLocation } from 'react-router-dom';
import styles from './MenuResponsive.module.css';

function MenuResponsive({ isOpen, setIsOpen }) {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const location = useLocation();

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (!isMobile) {
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }
  }, [isMobile]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const links = [
    { to: "/", label: "Início", icon: <FaHome /> },
    { to: "/perfil", label: "Perfil", icon: <CgProfile /> },
    { to: "/historico", label: "Histórico", icon: <FaHistory /> },
    { to: "/upload", label: "Upload", icon: <FaCloudUploadAlt /> },
  ];

  return (
    <>
      {isMobile && isOpen && (
        <div
          className={`${styles.overlay} ${isOpen ? styles.open : styles.close}`}
          onClick={toggleMenu}
        />
      )}


      <div className={styles.logo}>
        <button className={styles.menuIcon} onClick={toggleMenu}>
          <GiHamburgerMenu />
        </button>
        <p>My Stream</p>
      </div>


      <nav className={`${styles.nav} ${isOpen ? styles.open : styles.close}`}>
        <ul className={styles.menuList}>
          {links.map(({ to, label, icon }) => (
            <li key={to} className={styles.menuItem}>
              <Link
                to={to}
                className={`${styles.menuLink} ${(to === '/upload' && ['/upload', '/meta-dados'].includes(location.pathname)) ||
                    location.pathname === to
                    ? styles.active
                    : styles.desactivate
                  }`}
                onClick={() => isMobile && setIsOpen(false)}>
                {icon} {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
}

export default MenuResponsive;