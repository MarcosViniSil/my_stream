from src.exception.duplicateColumnException import DuplicateColumnException
from src.repository.metaDataRepository import MetaDataRepository
from src.service.bucket import Bucket
from fastapi import HTTPException, UploadFile
import os
import shutil
from uuid import UUID
import uuid
from PIL import Image

from src.service.userService import UserService

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ReceiveMetadaService:

    def __init__(self, bucket: Bucket, metaDataRepository: MetaDataRepository,userService:UserService):
        self.bucket = bucket
        self.metaDataRepository = metaDataRepository
        self.userService = userService

    async def processMetaData(self, idVideo: str, videoTitle: str, file: UploadFile,tokenUser:str) -> dict:
        
        userId = self.getUserId(tokenUser)
        
        self.isVideoBelongsToUser(userId,idVideo)
        
        self.isDataValid(idVideo,videoTitle,file,userId)
        
        filePath = self.copyFileLocally(file)

        self.resizeImage(700, 393, filePath) 

        imageUrlOnBucket = self.saveImageRemote(filePath)

        self.removeImageLocally(imageUrlOnBucket, filePath)

        self.insertMetaDatasDb(idVideo, videoTitle, imageUrlOnBucket)

        return {"message": "Imagem recebida com sucesso", "imageUrl": imageUrlOnBucket}
    
    def isVideoBelongsToUser(self,userId:bytes,videoId:str) -> None:
        if not self.metaDataRepository.isVideoBelongsToUser(userId,videoId):
            raise HTTPException(status_code=403, detail="O vídeo não pertence ao usuário que solicitou a alteração dos metadados")

    def getUserId(self,token:str) -> bytes:
        userId = None
        try:
            userId = self.userService.getUserId(token)
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))
        
        return userId

    def isDataValid(self,idVideo: str, videoTitle: str, file: UploadFile,userId:str) :
        
        if not self.isIdValid(idVideo):
            raise HTTPException(status_code=400, detail="uuid inválido")
        
        if not self.metaDataRepository.isVideoBelongsToUser(userId,idVideo):
            raise HTTPException(status_code=403,detail="O vídeo solicitado não pertence ao usuário")
        
        if not self.isExtensionValid(file):
            raise HTTPException(status_code=415,detail="Apenas arquivos .JPEG, .JPG, .PNG ou .svg são permitidos.")

        if not self.isFileSizeAllowed(file.size):
            raise HTTPException(status_code=400,detail="Tamanho de arquivo inválido, no máximo 50 megabytes")

        if not self.isTitleAllowed(videoTitle):
            raise HTTPException(status_code=400, detail="titulo de vídeo inválido")

        if not self.verifyID(idVideo):
            raise HTTPException(status_code=400, detail="uuid não encontrado")
        
    def copyFileLocally(self, file) -> str:
        try:
            filePath = os.path.join(UPLOAD_DIR, file.filename)
            with open(filePath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return filePath
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao baixar a imagem para o servidor")

    def saveImageRemote(self, filePath: str) -> str:
        try:
            imageUrlOnBucket = self.bucket.saveFileOnBucket(filePath)
            return imageUrlOnBucket
        except Exception as e:
            raise HTTPException(status_code=400, detail="Erro ao salvar imagem em nuvem")

    def removeImageLocally(self, imageUrlOnBucket: str, filePath: str) -> None:

        try:
            os.remove(filePath)
        except Exception as e:
            self.deleteFileRemote(imageUrlOnBucket.split("/")[-1])
            raise HTTPException(status_code=400, detail="Erro ao deletar imagem localmente")

    def insertMetaDatasDb(self, idVideo: UUID, videoTitle: str, videoUrlOnBucket: str) -> None:
        try:
            self.metaDataRepository.updateVideoMetadata(idVideo, videoTitle, videoUrlOnBucket)
        except ValueError as e:
            self.deleteFileRemote(videoUrlOnBucket.split("/")[-1])
        except DuplicateColumnException as e:
            self.deleteFileRemote(videoUrlOnBucket.split("/")[-1])
            message = self.handleDuplicateColumn(str(e))
            raise HTTPException(status_code=400, detail=str(message))

    def handleDuplicateColumn(self, column: str) -> str:
        if column == "videoTitle":
            return "Título de vídeo já existe"
        else:
            return "Ocorreu um erro"

    def resizeImage(self, targetWidth: int, targetHeight: int, imagePath: str) -> None:
        try:
            img = Image.open(imagePath)

            originalWidth, originalHeight = img.size
            aspectRatio = targetWidth / targetHeight

            if originalWidth / originalHeight > aspectRatio:
                newHeight = targetHeight
                newWidth = int(targetHeight * originalWidth / originalHeight)
            else:
                newWidth = targetWidth
                newHeight = int(targetWidth * originalHeight / originalWidth)

            imgResized = img.resize((newWidth, newHeight))
            imgResized.save(imagePath, quality=80)
        except Exception:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao manipular foto de capa")

    def isIdValid(self, val: str):
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False

    def verifyID(self,idVideo:str) -> bool:
        try:
            return self.metaDataRepository.doesVideoExist(idVideo)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao verificar id do vídeo solicitado")


    def deleteFileRemote(self, fileUrl: str) -> None:
        try:
            self.bucket.deleteFileOnBucket(fileUrl.split("/")[-1])
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao deletar imagem em nuvem")

    def isExtensionValid(self, file: UploadFile) -> bool:
        try:
            contentType = file.headers["content-type"]
            return (contentType == "image/png" or contentType == "image/svg+xml" or contentType == "image/jpeg")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao verificar extensão da imagem")

    def isTitleAllowed(self, title:str) -> bool:
        if len(title.replace(" ", "")) == 0:
            return False
        if len(title) > 100 :
            return False
        return True
    
    def isFileSizeAllowed(self, fileSize: int) -> bool:
        oneMegaByte = 1048576
        fileSizeInMegaBytes = fileSize / oneMegaByte
        return fileSizeInMegaBytes < 50.0
