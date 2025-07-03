import { React, useCallback, useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { UploadMetaDatas, getVideoMetadatas, getStatusVideo } from '../../service/metadataService.js'
import { useDropzone } from "react-dropzone";
import { Toaster, toast } from 'sonner';
import { BsUpload } from "react-icons/bs";
import { BsSend } from "react-icons/bs";

import './metaData.css'

function MetaData() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [title, setTitle] = useState('');
    const [countTitle, setCountTitle] = useState(0);
    const [previewUrl, setPreviewUrl] = useState(null);

    const navigate = useNavigate();
    const location = useLocation();

    const videoStatusIsValid = async (videoId) => {
        try {
            if (!videoId) {
                return false
            }
            const status = await getStatusVideo(videoId);
            if (!status) {
                return false;
            }

            if (status['status'] == 'FAIL') {
                return false
            }

            return true
        } catch (error) {
            console.error("Erro ao carregar metadados:", error);
            toast.error("Falha ao carregar os metadados do vídeo.");
            return false
        }
    }

    useEffect(() => {
        const fetchMetaData = async () => {

            const videoId = getVideoId();
            if (!videoId) return;

            if (!await videoStatusIsValid(videoId)) {
                navigate("/uploads");
            }
            try {
                const metaData = await getVideoMetadatas(videoId);
                if (!metaData) {
                    return;
                }

                setTitle(metaData['title']);
                setCountTitle(metaData['title'].length);

                if (metaData['thumbnailUrl']) {
                    setPreviewUrl(metaData['thumbnailUrl']);
                }

            } catch (error) {
                console.error("Erro ao carregar metadados:", error);
                toast.error("Falha ao carregar os metadados do vídeo.");
            }
        };

        fetchMetaData();
    }, []);

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
        return id;
    }

    const handleChange = (event) => {
        setTitle(event.target.value);
        setCountTitle(event.target.value.length)
    };


    const onDrop = useCallback((acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file) {
            const file = acceptedFiles[0];
            setSelectedFile(file);
            setPreviewUrl(URL.createObjectURL(file));
            toast.info(`Foto selecionada: ${file.name}`)
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
        if (!isFieldsValid(getVideoId(), title, selectedFile)) {
            return;
        }
        let toastId;
        try {
            toastId = toast.loading("Enviando imagem para o servidor")

            await UploadMetaDatas(getVideoId(), title, selectedFile);
            sendSuccess(toastId)
            setSelectedFile(null)

            await timeout(1000);

            navigate("/uploads");

        } catch (err) {
            console.log(err)
            sendError(err.message, toastId)
        }
    };

    const isFieldsValid = (id, title, file) => {
        if (!id) {
            sendError("Ocoreru um erro ao localizar vídeo associado aos metadados, tente novamente")
            return false;
        } else if (!file) {
            sendError("Arquivo não foi selecionado")
            return false;
        } else if (!title || String(title).replace(/\s+/g, "").length == 0) {
            sendError("Título de vídeo vazio")
            return false;
        } else if (String(title).replace(/\s+/g, "").length > 100) {
            sendError("O tamanho máximo de título é 100 caracteres")
            return false;
        }

        return true;
    }

    return (
        <>
            <div className="wrapAllMetaData">
                <Toaster position="top-right" />
                <div className="wrapElementsMetaDatas">
                    <div className="wrapSendThumbNail">
                        <div className="wrapTitleReceiveThumbnail">
                            <h3>Envie uma foto para a capa do seu vídeo</h3>
                        </div>
                        <div className="wrapReceiveThumbnail" {...getRootProps()}
                            style={{
                                backgroundImage: previewUrl ? `url(${previewUrl})` : 'none',
                                backgroundSize: 'cover',
                                backgroundPosition: 'center',
                                opacity: 0.5,
                            }}>
                            <input {...getInputProps()} />
                            <button className="buttonSelectVideo" type="button" onClick={open}>
                                <div className="wrapTextButtonSend">
                                    <p className="wrapButtonText"><BsUpload /> <u>Selecione</u> ou arraste e solte uma imagem</p>
                                </div>
                            </button>
                        </div>
                    </div>

                    <div className="wrapReceiveTitleVideo">
                        <div className="wrapTitleReciveTitle">
                            <h3>Adicione um título para o vídeo</h3>
                        </div>
                        <div className="wrapInputTitle">
                            <input value={title} onChange={handleChange} id="inputTitle" name="inputTitle" placeholder="Título do vídeo" maxLength={100} />
                            <p className="countCaractersTitle">{countTitle}/100</p>
                        </div>
                    </div>
                </div>
                <div className="wrapButtonSendMetaDatas">
                    <button className="buttonSendMetaDatas" type="button" onClick={handleUpload}>Enviar metadados <BsSend /></button>
                </div>

                <p className="detailsImage">*A imagem que aparece é como será visualizada pelos usuários</p>
            </div>

        </>
    )
}

export default MetaData;