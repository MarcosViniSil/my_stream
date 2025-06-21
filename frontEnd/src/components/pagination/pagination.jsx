import React, { useState, useEffect } from 'react';
import ReactPaginate from 'react-paginate';
import VideoList from '../../components/videoList/videoList';

import './pagination.css'

export default function VideoPagination() {
  const itemsPerPage = 5;

  const videos = [
    {
      videoId: "a1f10016-b464-4a1d-8f6d-47fffaf20e86",
      date: "21/06/2025",
      title: "teste de título",
      status: "PROCESSING"
    },
    {
      videoId: "a9df5176-db69-4ae8-8db3-43f5b6a58b38",
      date: "21/06/2025",
      title: "",
      status: "FAIL"
    },
    {
      videoId: "b1234567-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      date: "22/06/2025",
      title: "Outro vídeo",
      status: "READY"
    },
    {
      videoId: "b1234567-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      date: "22/06/2025",
      title: "Outro vídeo",
      status: "READY"
    },
    {
      videoId: "b1234567-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      date: "22/06/2025",
      title: "Outro vídeo",
      status: "READY"
    }
    // ... pode ter mais vídeos
  ];

  const [currentItems, setCurrentItems] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [itemOffset, setItemOffset] = useState(0);

  useEffect(() => {
    const endOffset = itemOffset + itemsPerPage;
    setCurrentItems(videos.slice(itemOffset, endOffset));
    setPageCount(Math.ceil(50 / itemsPerPage));
  }, [itemOffset, itemsPerPage]);

  const handlePageClick = (event) => {
    const newOffset = (event.selected * itemsPerPage) % videos.length;
    setItemOffset(newOffset);
  };

  const handleDelete = (id) => {
    alert(`Excluir vídeo com id: ${id}`);
    // Aqui você faria a exclusão via API ou setando novo estado
  };

  const handleEdit = (id) => {
    alert(`Editar vídeo com id: ${id}`);
    // Aqui você pode abrir um formulário de edição
  };

  return (
    <div>
      <h1>Lista de Vídeos</h1>

      <VideoList videos={currentItems} onDelete={handleDelete} onEdit={handleEdit} /> 

      <ReactPaginate
        breakLabel="..."
        nextLabel="Próximo"
        onPageChange={handlePageClick}
        pageRangeDisplayed={3}
        marginPagesDisplayed={2}
        pageCount={pageCount}
        previousLabel="Anterior"
        containerClassName="pagination"
        pageClassName="page-item"
        pageLinkClassName="page-link"
        previousClassName="page-item"
        previousLinkClassName="page-link"
        nextClassName="page-item"
        nextLinkClassName="page-link"
        breakClassName="page-item"
        breakLinkClassName="page-link"
        activeClassName="active"
        disabledClassName="disabled"
      />
    </div>
  );
}
