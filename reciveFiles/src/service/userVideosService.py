import uuid
from fastapi import HTTPException
from src.repository.videoRepository import VideoRepository
import datetime
from src.enum.statusVideoEnum import VideoStatus

class UserVideosService:

    def __init__(self,videoRepository:VideoRepository):
        self.videoRepository = videoRepository

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
            date, title, status = row
            dateFormated = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d/%m/%Y')
            result.append({
                "date": str(dateFormated),                
                "title": title if title else "",  
                "status": status
            })

        return result
    
    def deleteVideo(self,videoId:str,tokenUser:str) -> None:
        #TODO create logic to retrive userId by Token
        userId = '3f06af63-a93c-11e4-9797-00505690773f'
        
        isVideoBelongsToUser = self.videoRepository.isVideoBelongsToUser(userId,videoId)
        if not isVideoBelongsToUser:
            raise HTTPException(status_code=403,detail="O vídeo solicitado não pertence ao usuário que solicitou")
        
        statusVideo = self.videoRepository.getStatusVideo(videoId)
        if statusVideo == VideoStatus.PROCESSING.value:
            raise HTTPException(status_code=400,detail="O vídeo solicitado ainda está em processamento, aguarde ser concluído para exclusão")
        
        self.videoRepository.deleteVideoById(videoId)

        return {"message": "Vídeo deletado com sucesso"}
