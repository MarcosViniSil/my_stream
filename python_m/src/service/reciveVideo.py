from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from fastapi import HTTPException
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ReciveVideo:

    def __init__(self,bucket: Bucket, videoRepository:VideoRepository):
        self.bucket = bucket
        self.videoRepository = videoRepository

    async def processReceivedVideo(self,file) -> dict:
        if not file.filename.endswith(".mp4"):
            raise HTTPException(status_code=415, detail="Apenas arquivos .mp4 são permitidos.")
    
        file_path = os.path.join(UPLOAD_DIR, file.filename)
    
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        hashVideo = ""
        try:
            hashVideo = self.saveVideo(file_path)
        except Exception as e:
            print("deu erro:", e)
            raise HTTPException(status_code=400, detail="Erro ao salvar video em bucket na nuvem")

        try:
            self.removeLocalVideo(hashVideo,file_path)
        except Exception as e:
            try:
                self.bucket.deleteVideoOnBucket(hashVideo.split("/")[-1])
            except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel deletar vídeo local e quando foi necessario deletar vídeo em nuvem ocorreu outro erro")
            
            raise HTTPException(status_code=400, detail="Erro ao deletar video localmente")
        
        videoId = ""
        try:
            videoId = self.videoRepository.insertUrlDb(hashVideo)
        except Exception as e:
            try:
                self.bucket.deleteVideoOnBucket(hashVideo.split("/")[-1])
            except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel inserir url video no banco e quando foi necessario deletar vídeo em nuvem ocorreu outro erro")
                
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")

        
        if videoId != "":
            return {"message": "Vídeo recebido com sucesso!", "videoId": videoId}
        else:
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")

    def saveVideo(self,file_path: str) -> str:
        try:
            hashVideo = self.bucket.saveVideoOnBucket(file_path)
            return hashVideo
        except Exception as e:
            raise ValueError(f"{e}")
    
    def removeLocalVideo(self,hashVideoBucket: str,file_path: str) -> None:

        if hashVideoBucket != "":
            os.remove(file_path)
        else:
            raise ValueError("Ocorreu um erro, video não foi salvo na nuvem, tente novamente")
        
    def insertUrlVideoDb(self, url: str) -> None:
        if url.replace(" ","") == "":
            raise ValueError("url vazia, valor inválido")
        
        self.videoRepository.insertUrlDb(url)
    