
from src.repository.metaDataRepository import MetaDataRepository
from src.service.bucket import Bucket
from fastapi import HTTPException,UploadFile
import os
import shutil
from uuid import UUID
import uuid
import math

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ReceiveMetadaService:

    def __init__(self,bucket: Bucket, metaDataRepository:MetaDataRepository):
        self.bucket = bucket
        self.metaDataRepository = metaDataRepository

    async def processMetaData(self,idVideo : UUID,videoTitle : str,file : UploadFile) -> dict:
        if not self.isExtensionValid(file):
            raise HTTPException(status_code=415, detail="Apenas arquivos .JPEG, .JPG, .PNG ou .svg são permitidos.")
        
        if not self.isFileSizeAllowed(file.size):
            raise HTTPException(status_code=400, detail="Tamanho de arquivo inválido, no máximo 50 megabytes")
        
        if not self.isValidUuid(idVideo):
            raise HTTPException(status_code=400, detail="uuid inválido")
        
        if videoTitle.replace(" ", "") == "":
            raise HTTPException(status_code=400, detail="titulo de vídeo vazio")
        
        if not self.metaDataRepository.isUUIDExistsOnDataBase(idVideo):
            raise HTTPException(status_code=400, detail="uuid não encontrado")


        filePath = self.copyFileLocally(file)

        imageUrlOnBucket = self.saveImageRemote(filePath)

        self.removeImageLocally(imageUrlOnBucket,filePath)
        
        self.insertMetaDatasDb(idVideo,videoTitle,imageUrlOnBucket)

        return {"message": "Imagem recebida com sucesso", "imageUrl": imageUrlOnBucket}


    def copyFileLocally(self,file) -> str:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    def saveImageRemote(self,filePath: str) -> str:
        try:
            imageUrlOnBucket = self.bucket.saveFileOnBucket(filePath)
            return imageUrlOnBucket
        except Exception as e:
            raise HTTPException(status_code=400, detail="Erro ao salvar imagem em nuvem")
    
    def removeImageLocally(self,imageUrlOnBucket: str,filePath: str) -> None:

        try:
            os.remove(filePath)
        except Exception as e:
            try:
                self.bucket.deleteFileOnBucket(imageUrlOnBucket.split("/")[-1])
            except Exception as e:
                raise HTTPException(status_code=400, detail="Não foi possivel deletar imagem local e quando foi necessario deletar imagem em nuvem ocorreu outro erro")
            
            raise HTTPException(status_code=400, detail="Erro ao deletar imagem localmente")
        
    def insertMetaDatasDb(self,idVideo : UUID,videoTitle : str,videoUrlOnBucket : str) -> None:
        try:
            self.metaDataRepository.insertMetaData(idVideo,videoTitle,videoUrlOnBucket)
        except Exception as e:
            try:
                self.bucket.deleteFileOnBucket(videoUrlOnBucket.split("/")[-1])
            except Exception as e:
                print(e)
                raise HTTPException(status_code=400, detail="Não foi possivel inserir url imagem no banco e quando foi necessario deletar imagem em nuvem ocorreu outro erro")

            print(e)    
            raise HTTPException(status_code=400, detail=str(e))
    
    def isValidUuid(self,val: UUID):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            
            return False
    
    def isExtensionValid(self,file : UploadFile) -> bool:
        contentType = file.headers["content-type"]
        return contentType == "image/png" or contentType == "image/svg+xml" or contentType == "image/jpeg"

    def isFileSizeAllowed(self,fileSize: int) -> bool :
        fileSizeInMegaBytes = math.floor(fileSize/1048576)
        return fileSizeInMegaBytes < 50
    
    