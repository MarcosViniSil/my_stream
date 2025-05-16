from src.exception.duplicateColumnException import DuplicateColumnException
from src.repository.metaDataRepository import MetaDataRepository
from src.service.bucket import Bucket
from fastapi import HTTPException, UploadFile
import os
import shutil
from uuid import UUID
import uuid
from PIL import Image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ReceiveMetadaService:

    def __init__(self, bucket: Bucket, metaDataRepository: MetaDataRepository):
        self.bucket = bucket
        self.metaDataRepository = metaDataRepository

    async def processMetaData(self, idVideo: str, videoTitle: str, file: UploadFile) -> dict:
        if not self.isExtensionValid(file):
            raise HTTPException(status_code=415,detail="Apenas arquivos .JPEG, .JPG, .PNG ou .svg são permitidos.",)

        if not self.isFileSizeAllowed(file.size):
            raise HTTPException(status_code=400,detail="Tamanho de arquivo inválido, no máximo 50 megabytes",)

        if not self.isValidUuid(idVideo):
            raise HTTPException(status_code=400, detail="uuid inválido")

        if videoTitle.replace(" ", "") == "":
            raise HTTPException(status_code=400, detail="titulo de vídeo vazio")

        if not self.verifyUuidDb(idVideo):
            raise HTTPException(status_code=400, detail="uuid não encontrado")

        filePath = self.copyFileLocally(file)

        self.resizeImage(700, 500, filePath)

        imageUrlOnBucket = self.saveImageRemote(filePath)

        self.removeImageLocally(imageUrlOnBucket, filePath)

        self.insertMetaDatasDb(idVideo, videoTitle, imageUrlOnBucket)

        return {"message": "Imagem recebida com sucesso", "imageUrl": imageUrlOnBucket}

    def copyFileLocally(self, file) -> str:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

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
            self.metaDataRepository.insertMetaData(idVideo, videoTitle, videoUrlOnBucket)
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

    def resizeImage(self, target_width: int, target_height: int, imagePath: str) -> None:
        img = Image.open(imagePath)

        original_width, original_height = img.size

        if original_width / original_height > target_width / target_height:
            new_width = target_width
            new_height = int(target_width * original_height / original_width)
        else:
            new_height = target_height
            new_width = int(target_height * original_width / original_height)

        imgResized = img.resize((new_width, new_height))
        imgResized.save(imagePath, quality=70)

    def isValidUuid(self, val: str):
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False

    def verifyUuidDb(self,idVideo:str) -> bool:
        try:
            return self.metaDataRepository.isUUIDExistsOnDataBase(idVideo)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao verificar id do vídeo solicitado")


    def deleteFileRemote(self, fileUrl: str) -> None:
        try:
            self.bucket.deleteFileOnBucket(fileUrl.split("/")[-1])
        except Exception as e:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao deletar imagem em nuvem")

    def isExtensionValid(self, file: UploadFile) -> bool:
        contentType = file.headers["content-type"]
        return (contentType == "image/png" or contentType == "image/svg+xml" or contentType == "image/jpeg")

    def isFileSizeAllowed(self, fileSize: int) -> bool:
        oneMegaByte = 1048576
        fileSizeInMegaBytes = fileSize / oneMegaByte
        return fileSizeInMegaBytes < 50.0
