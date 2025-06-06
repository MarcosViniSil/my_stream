import { React, useCallback, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { UploadMetaDatas } from '../../service/metadataService.js'
import { useDropzone } from "react-dropzone";
import { Toaster, toast } from 'sonner';
import { BsUpload } from "react-icons/bs";
import { BsSend } from "react-icons/bs";

import './metaData.css'

function MetaData() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileSelected, setFileSelected] = useState("");
    const [title, setTitle] = useState('');

    const navigate = useNavigate();
    const location = useLocation();
    const sendSuccess = (toastId) => {
        toast.success("Imagem enviada com sucesso!", {
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

    const sendError = (message, toastId) => {
        toast.error(`${message}`, {
            style: {
                background: '#8B0000',
                color: '#fff'
            },
            id: toastId,
        });
    }

    const getVideoId = () => {
        const search = location.search;
        const id = new URLSearchParams(search).get("videoId");
        console.log(id)
        return id;
    }

    const handleChange = (event) => {
        setTitle(event.target.value);
    };


    const onDrop = useCallback((acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file) {
            setSelectedFile(file);
            toast.info(`Foto selecionada: ${file.name}`)
            setFileSelected(`Foto selecionada: ${file.name}`)
        }
    }, []);

    const { getRootProps, getInputProps, open } = useDropzone({
        onDrop,
        noClick: true,
        noKeyboard: true,
        accept: { "image/*": [] },
    });

    const timeout = (delay) => {
        return new Promise(res => setTimeout(res, delay));
    }

    const handleUpload = async () => {
        if (!selectedFile) {
            sendError("Nenhuma imagem selecionado")
            return;
        }
        let toastId;
        try {
            toastId = toast.loading("Enviando imagem para o servidor")

            const result = await UploadMetaDatas(getVideoId(), title, selectedFile);
            sendSuccess(toastId)
            setFileSelected(``)
            setSelectedFile(null)

            await timeout(1000);

            navigate("/upload");

        } catch (err) {
            console.log(err)
            setSelectedFile(null)
            sendError(err.message, toastId)
            setFileSelected(``)
        }
    };

    return (
        <>
            <div className="wrapAllMetaData">
                <Toaster position="top-right" />
                <div className="wrapElementsMetaDatas">
                    <div className="wrapSendThumbNail">
                        <h3>Envie uma foto para a capa do seu vídeo</h3>
                        <div className="wrapReceiveThumbnail" {...getRootProps()}>
                            <input {...getInputProps()} />
                            <button className="buttonSelectVideo" type="button" onClick={open}>
                                <div className="wrapTextButtonSend">
                                    <p className="wrapButtonText"><BsUpload /> <u>Selecione</u> ou arraste e solte uma imagem</p>
                                </div>
                            </button>

                        </div>
                        <p className="statusPhoto">{fileSelected}</p>
                    </div>

                    <div className="wrapReceiveTitleVideo">
                        <h3>Adicione um título para o vídeo</h3>
                        <div className="wrapInputTitle">
                            <input onChange={handleChange} id="inputTitle" name="inputTitle" placeholder="Título" maxLength={100} />
                        </div>
                    </div>
                </div>
                <button className="buttonSendMetaDatas" type="button" onClick={handleUpload}>Enviar metadados <BsSend /></button>
            </div>

        </>
    )
}

export default MetaData;