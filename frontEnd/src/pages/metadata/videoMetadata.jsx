import { React,useState } from "react";
import MetaData from '../../components/metaDatasVideo/metaData'
import MenuResponsive from '../../layout/menuReponsive/MenuReponsive'
import './videoMetadata.css'


function MetaDataPage() {
    const [isMenuOpen, setIsMenuOpen] = useState(true); 

    return (
    <>
      <MenuResponsive isOpen={isMenuOpen} setIsOpen={setIsMenuOpen} />

      <div className={`wrapSendMetaDatas ${isMenuOpen ? "menu-open" : ""}`}>
        <h1 className="title">Adicione os metadados do vídeo</h1>
        <MetaData />
      </div>
    </>
    )
}

export default MetaDataPage;