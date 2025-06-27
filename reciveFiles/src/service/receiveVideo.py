from uuid import UUID
from src.service.queueService import QueueService
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from fastapi import HTTPException,UploadFile
import subprocess
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ReciveVideo:

    def __init__(self,bucket: Bucket, videoRepository:VideoRepository,queueService:QueueService):
        self.bucket = bucket
        self.videoRepository = videoRepository
        self.queueService = queueService

    async def processReceivedVideo(self,file:UploadFile) -> dict:

        if not self.isExtensionValid(file):
            raise HTTPException(status_code=415, detail="Apenas arquivos .mp4 são permitidos.")
        
        if not self.isFileSizeAllowed(file.size):
            raise HTTPException(status_code=400, detail="Tamanho de arquivo inválido, no máximo 5 gigabytes")
        
        filePath = self.copyFileLocally(file)

    
        hashVideo = self.saveVideoRemote(filePath)

        videoDurationSeconds = self.getVideoDuration(file)

        self.removeLocalVideo(hashVideo,filePath)
        
        videoId = self.insertVideoDatasDb(hashVideo,videoDurationSeconds)
        
        self.createReactionVideo(videoId,hashVideo)

        if videoId != "":
            try:
                messageQueue = {"videoId":videoId,"videoUrl":hashVideo}
                self.queueService.sendMessageQueue(messageQueue)
            except Exception as e:
                self.removeRemoteFile(hashVideo.split("/")[-1])
                raise HTTPException(status_code=400, detail=str(e))
            return {"message": "Vídeo recebido com sucesso!", "videoId": videoId}
        else:
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")

    def copyFileLocally(self,file:UploadFile) -> str:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if not self.isVideoContainAudio(str(file.filename)):
             os.remove(file_path)
             raise HTTPException(status_code=400, detail="O vídeo informado não possui áudio")
       
        return file_path
    
    def isVideoContainAudio(self,fileName: str) -> bool:
        resultado = subprocess.run(["ffprobe", "-i",f"{UPLOAD_DIR}/{fileName}","-show_streams","-select_streams","a","-loglevel","error"], 
                                   capture_output=True, text=True)
        if resultado.stdout == "":
            return False
        else:
            return True

    def getVideoDuration(self, file: UploadFile) -> int:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            f"{UPLOAD_DIR}/{file.filename}"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail="Não foi possível obter a duração do vídeo")

        resultStr = result.stdout.strip()
        durationInSeconds = int(float(resultStr)) 
        
        if durationInSeconds < 10:
            raise HTTPException(status_code=400, detail="O vídeo precisa ter pelo menos 10 segundos")
        
        return durationInSeconds

    def saveVideoRemote(self,file_path: str) -> str:
        try:
            hashVideo = self.bucket.saveFileOnBucket(file_path)
            return hashVideo
        except Exception as e:
            print(e)
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Erro ao salvar video em bucket na nuvem")
    
    def removeLocalVideo(self,hashVideoBucket: str,file_path: str) -> None:

        try:
            os.remove(file_path)
        except Exception as e:
            self.removeRemoteFile(hashVideoBucket.split("/")[-1])
            raise HTTPException(status_code=400, detail="Erro ao deletar video localmente")
        
    def insertVideoDatasDb(self,hashVideo : str,videoDuration:int) -> str:
        try:
            videoId = self.videoRepository.insertDatasVideo(hashVideo,videoDuration)
            return videoId
        except Exception as e:

            self.removeRemoteFile(hashVideo.split("/")[-1])
            raise HTTPException(status_code=400, detail="Erro ao salvar url no banco")
    
    def createReactionVideo(self,videoId:str,hashVideo : str) -> None:
        try:
            self.videoRepository.createLikeAndDislikesVideo(videoId)
        except Exception as e:
            self.removeRemoteFile(hashVideo.split("/")[-1])
            raise HTTPException(status_code=400, detail="Erro ao criar likes e deslikes")
   
    def removeRemoteFile(self,nameFile :str) -> None:
         try:
                self.bucket.deleteFileOnBucket(nameFile)
         except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel deletar vídeo em nuvem quando necessário")

    def isExtensionValid(self,file : UploadFile) -> bool:
        contentType = file.headers["content-type"]
        return contentType == "video/mp4" 

    def isFileSizeAllowed(self,fileSize: int) -> bool :
        oneGigaByte = 1073741824
        fileSizeInGigaBytes = fileSize / oneGigaByte
        return fileSizeInGigaBytes < 5.0