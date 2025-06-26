import uuid
from fastapi import HTTPException
from src.repository.videoRepository import VideoRepository
import datetime
from src.enum.statusVideoEnum import VideoStatus
from src.service.bucket import Bucket

class UserVideosService:

    def __init__(self,videoRepository:VideoRepository,bucket: Bucket):
        self.videoRepository = videoRepository
        self.bucket = bucket

    def getVideosList(self,tokenUser:str, offSet: int) -> dict:
        if offSet < 0:
            raise HTTPException(status_code=403,detail="Offset deve ser maior que 0")
        
        DATAS_PER_PAGE = 5
        offSet = offSet * DATAS_PER_PAGE
        datas = self.videoRepository.getListVideos(tokenUser,offSet)
        return self.convertDictToArray(datas)
    
    def convertDictToArray(self,data:dict) -> dict:
        result = []
        for row in data:
            videoId,date, title, status = row
            videoIdString = str(uuid.UUID(bytes=videoId))
            dateFormated = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d/%m/%Y')
            result.append({
                "videoId":videoIdString,
                "date": str(dateFormated),                
                "title": title if title else "",  
                "status": status
            })

        return result
    
    def deleteVideo(self,videoId:str,tokenUser:str) -> None:
        #TODO create logic to retrive userId by Token
        userId = '3f06af63-a93c-11e4-9797-00505690773f'
        
        videoDatas = ""
        try:
            videoDatas = self.videoRepository.getDatasToDeleteVideo(videoId)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao buscar os dados do vídeo para exclusão")
        
        if videoDatas is None:
            raise HTTPException(status_code=400,detail="Não foi possível buscar os dados do vídeo solicitado para exclusão")
        
        if not self.isVideoBelongsToUser(userId,videoDatas["userId"]):
            raise HTTPException(status_code=403,detail="O vídeo não pertence ao usuário")

        statusVideo = videoDatas["videoStatus"]
        if statusVideo == VideoStatus.PROCESSING.value:
            raise HTTPException(status_code=400,detail="O vídeo solicitado ainda está em processamento, aguarde ser concluído para exclusão")

        try:
            self.videoRepository.changeVideoToDeleted(videoId)
        except Exception as e:
             raise HTTPException(status_code=400,detail="Ocorreu um erro ao atualizar a base de dados, tente novamente")

        return {"message": "Vídeo deletado com sucesso"}

    def isVideoBelongsToUser(self,userIdRequest:str,userIdDB:str) -> bool:
        userIdBytes = uuid.UUID(userIdRequest).bytes
        if userIdBytes != userIdDB:
            return False

        return True

    def getTotalVideosByUser(self,tokenUser:str) -> dict:
        #TODO get id user by token
        try:
            videosQuantity = self.videoRepository.getNumberOfVideosByUser(tokenUser)
            if videosQuantity:
                return {"videosQuantity":videosQuantity}
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao verificar a quantidade de vídeos do usuário")
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao verificar a quantidade de vídeos do usuário")

    def getVideoStatus(self,videoId:str) -> dict:
        if not videoId:
            raise HTTPException(status_code=400,detail="Id do vídeo não foi informado")
        
        status = self.videoRepository.getVideoStatusById(videoId)
        if status:
            return {"status":status[0]}
        else:
            raise HTTPException(status_code=404,detail="status do vídeo não foi encontrado")