import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { uploadVideo } from "../../service/videoService";
import { BsUpload } from "react-icons/bs";
import { BsSend } from "react-icons/bs";
import { Toaster, toast } from 'sonner';
import { useNavigate } from "react-router-dom";

import './receiveVideo.css';

function ReceiveVideo() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileSelected, setFileSelected] = useState("");
  const navigate = useNavigate();

  const sendSuccess = (toastId) => {
    toast.success("Vídeo enviado com sucesso!", {
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

  const timeout = (delay) => {
    return new Promise( res => setTimeout(res, delay) );
}

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      toast.info(`Vídeo selecionado: ${file.name}`)
      setFileSelected(`Vídeo selecionado: ${file.name}`)
    }
  }, []);

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
    accept: { 'video/mp4': [] },
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
      if(!result['videoId']){
        throw new Error("ocorreu um erro ao salvar o vídeo, tente novamente")
      }
      sendSuccess(toastId)
      setFileSelected(``)
      setSelectedFile(null)

      await timeout(1000);

      navigate(`/meta-dados?videoId=${result['videoId']}`);

    } catch (err) {
      console.log(err.message)
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
