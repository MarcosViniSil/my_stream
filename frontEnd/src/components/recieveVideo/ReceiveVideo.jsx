import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { uploadVideo } from "../../service/videoService";
import { BsUpload } from "react-icons/bs";
import { BsSend } from "react-icons/bs";
import { Toaster, toast } from 'sonner';

import './receiveVideo.css';

function ReceiveVideo() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileSelected, setFileSelected] = useState("");

  const sendSuccess = (toastId) => {
    toast.success("Arquivo enviado com sucesso!", {
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

  const sendError = (message,toastId) => {
    toast.error(`${message}`, {
      style: {
        background: '#8B0000',
        color: '#fff'
      },
      id: toastId,
    });
  }

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      toast.info(`Arquivo selecionado: ${file.name}`)
      setFileSelected(`Arquivo selecionado: ${file.name}`)
    }
  }, []);

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
    accept: { 'video/*': [] },
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      sendError("Nenhum vídeo selecionado")
      return;
    }
    let toastId;
    try {
       toastId = toast.loading("Enviando vídeo para o servidor")
      
      const result = await uploadVideo(selectedFile);
      sendSuccess(toastId)
      setFileSelected(``)
      setSelectedFile(null)
      
      //TODO manipulate id video and send user to another screen

    } catch (err) {
      setSelectedFile(null)
      sendError(err.message,toastId)
      setFileSelected(``)
    }
  };

  return (

    <div className="wrapAllReceiveVideo">
      <Toaster position="top-right" />
      <div className="wrapReceiveVideo" {...getRootProps()}>
        <input {...getInputProps()} />

        <button className="buttonSelectVideo" type="button" onClick={open}>
          <div className="wrapTextButtonSend">
            <p className="wrapButtonText"><BsUpload /> <u>Selecione</u> ou arraste e solte um vídeo</p>
          </div>

        </button>

        <p className="statusVideo">{fileSelected}</p>

        <button className="buttonSendVideo" type="button" onClick={handleUpload}>
          Enviar vídeo <BsSend />
        </button>


      </div>
    </div>
  );
}

export default ReceiveVideo;
