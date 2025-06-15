import React, { useState,useEffect } from 'react';
import ReactPaginate from 'react-paginate';
import { Button, HStack } from '@chakra-ui/react';
import './pagination.css'; 

export default function Pagination() {
  const itemsPerPage = 5;
  const items = Array.from({ length: 50 }, (_, index) => `Item ${index + 1}`);
  const [currentItems, setCurrentItems] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [itemOffset, setItemOffset] = useState(0);

  useEffect(() => {
    const endOffset = itemOffset + itemsPerPage;
    setCurrentItems(items.slice(itemOffset, endOffset));
    setPageCount(Math.ceil(items.length / itemsPerPage));
  }, [itemOffset, itemsPerPage]);

  const handlePageClick = (event) => {
    const newOffset = (event.selected * itemsPerPage) % items.length;
    setItemOffset(newOffset);
  };

  return (
    <div>
      <h1>Paginação com React Paginate + Chakra UI</h1>
      <ul>
        {currentItems.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>

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
        previousClassName="page-item"
        nextClassName="page-item"
        breakClassName="page-item"
        activeClassName="active"             
      />
    </div>
  );
}
