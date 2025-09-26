import React, { useState, useEffect, useContext } from 'react';
import { GiHamburgerMenu } from 'react-icons/gi';
import { FaHome } from "react-icons/fa";
import { CgProfile } from "react-icons/cg";
import { FaHistory } from "react-icons/fa";
import { FaCloudUploadAlt } from "react-icons/fa";
import { Link, useLocation } from 'react-router-dom';
import styles from './MenuResponsive.module.css';
import { AccessibleContext } from "../../context/AccessibleContext";
import { MdOutlineWbSunny } from "react-icons/md";
import { MdOutlineDarkMode } from "react-icons/md";
import { ThemeContext } from '../../context/themeContext';

function MenuResponsive({ isOpen, setIsOpen, defaultOpen = null }) {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const location = useLocation();
  const { accessible } = useContext(AccessibleContext);
  const { theme, toggleTheme } = useContext(ThemeContext);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (defaultOpen !== null) {
      setIsOpen(defaultOpen);
    } else {
      setIsOpen(!isMobile);
    }
  }, [isMobile, defaultOpen]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const links = [
    { to: "/", label: "Início", icon: <FaHome /> },
    { to: "/profile", label: "Perfil", icon: <CgProfile /> },
    { to: "/history", label: "Histórico", icon: <FaHistory /> },
    { to: "/uploads", label: "Uploads", icon: <FaCloudUploadAlt /> },
  ];

// MenuResponsive.jsx (trechos relevantes)
return (
  <div className={`${styles.menuWrapper} ${accessible ? styles.accessible : ''} ${theme ? styles.darkTheme : styles.lightTheme}`}>
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
    </div>

    <nav className={`${styles.nav} ${isOpen ? styles.open : styles.close}`}>
      <ul className={styles.menuList}>
        {links.map(({ to, label, icon }) => {
          const isActive = (to === '/uploads' && ['/upload', '/meta-dados', '/uploads'].includes(location.pathname)) ||
                            location.pathname === to;
          return (
            <li key={to} className={styles.menuItem}>
              <Link
                to={to}
                className={`${styles.menuLink} ${isActive ? styles.active : styles.desactivate}`}
                onClick={() => isMobile && setIsOpen(false)}
              >
                {icon} {label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  </div>
);

}

export default MenuResponsive;