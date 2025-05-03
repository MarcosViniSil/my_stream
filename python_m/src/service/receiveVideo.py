import math
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from fastapi import HTTPException,UploadFile
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ReciveVideo:

    def __init__(self,bucket: Bucket, videoRepository:VideoRepository):
        self.bucket = bucket
        self.videoRepository = videoRepository

    async def processReceivedVideo(self,file) -> dict:

        if not self.isExtensionValid(file):
            raise HTTPException(status_code=415, detail="Apenas arquivos .mp4 são permitidos.")
        
        if not self.isFileSizeAllowed(file.size):
            raise HTTPException(status_code=400, detail="Tamanho de arquivo inválido, no máximo 5 gigabytes")
        
        filePath = self.copyFileLocally(file)

        hashVideo = self.saveVideoRemote(filePath)

        self.removeLocalVideo(hashVideo,filePath)
        
        videoId = self.insertUrlVideoDb(hashVideo)

        if videoId != "":
            return {"message": "Vídeo recebido com sucesso!", "videoId": videoId}
        else:
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")

    def copyFileLocally(self,file) -> str:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    def saveVideoRemote(self,file_path: str) -> str:
        try:
            hashVideo = self.bucket.saveFileOnBucket(file_path)
            return hashVideo
        except Exception as e:
            raise HTTPException(status_code=400, detail="Erro ao salvar video em bucket na nuvem")
    
    def removeLocalVideo(self,hashVideoBucket: str,file_path: str) -> None:

        try:
            os.remove(file_path)
        except Exception as e:
            try:
                self.bucket.deleteFileOnBucket(hashVideoBucket.split("/")[-1])
            except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel deletar vídeo local e quando foi necessario deletar vídeo em nuvem ocorreu outro erro")
            
            raise HTTPException(status_code=400, detail="Erro ao deletar video localmente")
        
    def insertUrlVideoDb(self,hashVideo : str) -> str:
        try:
            videoId = self.videoRepository.insertUrlDb(hashVideo)
            return videoId
        except Exception as e:
            try:
                self.bucket.deleteFileOnBucket(hashVideo.split("/")[-1])
            except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel inserir url video no banco e quando foi necessario deletar vídeo em nuvem ocorreu outro erro")
                
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")
    
    def isExtensionValid(self,file : UploadFile) -> bool:
        contentType = file.headers["content-type"]
        return contentType == "video/mp4" 

    def isFileSizeAllowed(self,fileSize: int) -> bool :
        fileSizeInGigaBytes = math.floor(fileSize / 1073741824)
        return fileSizeInGigaBytes < 5