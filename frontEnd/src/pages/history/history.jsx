import React, { useState,useEffect } from 'react'
import HistoryVideos from '../../components/historyVideos/historyVideos'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import SearchBar from '../../components/searchBar/SearchBar'
import { useNavigate } from "react-router-dom";
import './history.css'

export default function History() {
    const [isMenuOpen, setIsMenuOpen] = useState(true);
      useEffect(() => {
        const handleResize = () => {
            if(window.innerWidth <= 960){
                setIsMenuOpen(false)
            }else{
                setIsMenuOpen(true)
            }
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
      }, []);
    const navigate = useNavigate();
    
    const handleSearch = (searchTerm) => {
        if (!searchTerm || searchTerm.length == 0) return

        navigate(`/busca?q=${searchTerm}`);

    }

    return (
        <>
            <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

            <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open2" : ""}`}>
                <div className='search'>
                    <SearchBar onSearch={handleSearch} />
                </div>
                <h2 className='titleHistory'>Histórico de exibição</h2>
                <HistoryVideos />
            </div>
        </>
    )
}