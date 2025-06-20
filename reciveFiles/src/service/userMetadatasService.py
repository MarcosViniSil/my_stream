import uuid
from fastapi import HTTPException

import datetime
from src.enum.statusVideoEnum import VideoStatus
from src.repository.metaDataRepository import MetaDataRepository
from src.service.bucket import Bucket

class UserMetaDatasService:

    def __init__(self,metadataRepository:MetaDataRepository):
        self.metadataRepository = metadataRepository

    def getVideoMetadatas(self, videoId:str) -> dict:
        try:
            metadatas = self.metadataRepository.getMetadatasByVideoId(videoId)
            if metadatas is None:
                return  {
                    "thumbnailUrl": "",
                    "title": "",
                }

            return metadatas
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao buscar metadadados do vídeo")