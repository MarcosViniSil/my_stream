import React, { useState,useContext } from 'react'
import WatchVideo from '../../components/watchVideo/watchVideo'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import SearchBar from '../../components/searchBar/SearchBar'
import { useNavigate } from "react-router-dom";
import { ThemeContext } from '../../context/themeContext';
import './watch.css'

export default function Watch() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { theme } = useContext(ThemeContext);
    const navigate = useNavigate();
    
    const handleSearch = (searchTerm) => {
        if (!searchTerm || searchTerm.length == 0) return

        navigate(`/busca?q=${searchTerm}`);

    }
    
    return (
        <>
            <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} defaultOpen={false} />
            <div className={`wrapWatchVideo ${isMenuOpen ? "menu-open" : ""} ${theme ? "dark" : "light"}`}>
                <div className={`search ${theme ? "dark" : "light"}`}>
                    <SearchBar onSearch={handleSearch} />
                </div>
                <WatchVideo />
            </div>
        </>
    )
}