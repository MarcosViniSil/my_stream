import React, { useState, useEffect, useRef } from 'react';
import ReactPaginate from 'react-paginate';
import VideoList from '../../components/videoList/videoList';
import { getQuantityVideos, getVideosUser, deleteVideo } from '../../service/videoService.js';
import { Spinner } from '@chakra-ui/react';
import { useNavigate } from "react-router-dom";
import { AlertDialog, AlertDialogBody, AlertDialogFooter, AlertDialogHeader, AlertDialogContent, AlertDialogOverlay, Button, } from '@chakra-ui/react';
import './pagination.css';
import { Toaster, toast } from 'sonner';

export default function VideoPagination() {
  const itemsPerPage = 5;

  const [videos, setVideos] = useState([]);
  const [currentItems, setCurrentItems] = useState([]);
  const [pageCount, setPageCount] = useState(0);
  const [itemOffset, setItemOffset] = useState(0);
  const [offSet, setOffset] = useState(0)
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const cancelRef = useRef();
  const [videoToDelete, setVideoToDelete] = useState(null);
  const [currentPage, setCurrentPage] = useState(0);

  const navigate = useNavigate();

  const fetchQuantityVideos = async () => {
    setLoading(true);
    try {
      const quantityVideos = await getQuantityVideos();

      if (!quantityVideos || quantityVideos.videosQuantity === 0) {
        setVideos([]);
        setCurrentItems([]);
        setPageCount(0);
      } else {
        const videosUser = await getVideosUser(offSet);
        setVideos(videosUser);

        const endOffset = itemOffset + itemsPerPage;
        setCurrentItems(videosUser.slice(itemOffset, endOffset));
        setPageCount(Math.ceil(quantityVideos.videosQuantity / itemsPerPage));
      }
    } catch (error) {
      console.error("Erro ao carregar vídeos:", error);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {

    fetchQuantityVideos();
    const intervalId = setInterval(fetchQuantityVideos, 60000);
    return () => clearInterval(intervalId);

  }, [itemOffset, itemsPerPage, offSet]);

  const sendError = (message, toastId) => {
    toast.error(`${message}`, {
      style: {
        background: '#8B0000',
        color: '#fff'
      },
      id: toastId,
    });
  }

  const sendSuccess = (toastId) => {
    toast.success("Vídeo excluído com sucesso", {
      style: {
        background: '#346E62',
        color: '#fff'
      },
      iconTheme: {
        primary: '#A7D1C9',
        secondary: '#fff'
      },
      id: toastId,
    });
  }

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
    setOffset(event.selected);
    const newOffset = (event.selected * itemsPerPage) % videos.length;
    setItemOffset(newOffset);
  };

  const handleDeleteClick = (id) => {
    if (isVideoProcessing(id)) {
      sendError("Error: O vídeo solicitado ainda está em processamento, aguarde ser concluído para exclusão")
      return
    }
    setVideoToDelete(id);
    setIsOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!videoToDelete) return;

    try {
      await deleteVideo(videoToDelete);
      sendSuccess();
      fetchQuantityVideos()

    } catch (error) {
      sendError(error);
    } finally {
      setIsOpen(false);
      setVideoToDelete(null);
    }
  };

  const isVideoProcessing = (idVideo) => {
    let found = false

    videos.forEach(e => {
      if (e.videoId == idVideo && e.status == 'PROCESSING') {
        found = true
      }
    })

    return found
  }

  const handleView = (id) => {
    //TODO redirect user to page video visualization 
  }

  const handleEdit = (id) => {
    if (!id) {
      return
    }
    navigate(`/meta-dados?videoId=${id}`);
  }

  return (
    <div>
      <Toaster position="top-right" />
      <AlertDialog
        isOpen={isOpen}
        leastDestructiveRef={cancelRef}
        onClose={() => setIsOpen(false)}
      >
        <AlertDialogOverlay>
          <AlertDialogContent bg="#222" color="white">
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Confirmar exclusão
            </AlertDialogHeader>

            <AlertDialogBody>
              Tem certeza que deseja excluir este vídeo? Essa ação não pode ser desfeita.
            </AlertDialogBody>

            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={() => setIsOpen(false)}>
                Cancelar
              </Button>
              <Button colorScheme="red" onClick={handleConfirmDelete} ml={3}>
                Excluir
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
      <h1 id='titlePagination'>Lista de Vídeos</h1>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="gray.200"
            color="#419181"
            size="xl"
          />
        </div>
      ) : videos.length === 0 ? (
        <p style={{ color: 'white', textAlign: 'center' }}>Nenhum vídeo cadastrado.</p>
      ) : (
        <>
          <VideoList videos={currentItems} onDelete={handleDeleteClick} onEdit={handleEdit} onView={handleView} />

          <ReactPaginate
            breakLabel="..."
            nextLabel="Próximo"
            onPageChange={handlePageClick}
            pageRangeDisplayed={3}
            marginPagesDisplayed={2}
            pageCount={pageCount}
            previousLabel="Anterior"
            forcePage={currentPage}
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
        </>
      )}
    </div>
  );
}
