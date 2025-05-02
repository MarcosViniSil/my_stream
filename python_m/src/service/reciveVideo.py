from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from fastapi.responses import JSONResponse
import os


class ReciveVideo:

    def __init__(self,bucket: Bucket, videoRepository:VideoRepository):
        self.bucket = bucket
        self.videoRepository = videoRepository

    def processReceivedVideo(self,filePath: str) -> dict:
        hashVideo = self.saveVideo(filePath)
        try:
            self.removeLocalVideo(hashVideo,filePath)
        except Exception as e:
            try:
                self.bucket.deleteVideoOnBucket(hashVideo.split("/")[-1])
            except Exception as e:
                return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})
        
            return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})
    
        videoId = ""
        try:
            videoId = self.videoRepository.insertUrlDb(hashVideo)
        except Exception as e:
            try:
                self.bucket.deleteVideoOnBucket(hashVideo.split("/")[-1])
            except Exception as e:
                return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})
            return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})
        
        if videoId != "":
            return {"message": "Vídeo recebido com sucesso!", "videoId": videoId}
        else:
            return JSONResponse(status_code=400, content={"erro": "Ocorreu um erro ao salvar url do vídeo no banco de dados"})

    def saveVideo(self,file_path: str) -> str:
        try:
            hashVideo = self.bucket.saveVideoOnBucket(file_path)
            return hashVideo
        except Exception as e:
            return ""
    
    def removeLocalVideo(self,hashVideoBucket: str,file_path: str) -> None:
        print("hashVideoBucket ",hashVideoBucket)
        if hashVideoBucket != "":
            os.remove(file_path)
        else:
            raise ValueError("Ocorreu um erro, video não foi salvo na nuvem, tente novamente")
        
    def insertUrlVideoDb(self, url: str) -> None:
        if url.replace(" ","") == "":
            raise ValueError("url vazia, valor inválido")
        
        self.videoRepository.insertUrlDb(url)
    