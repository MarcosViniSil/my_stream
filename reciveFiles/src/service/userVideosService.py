from fastapi import HTTPException
import json
from src.repository.videoRepository import VideoRepository
import datetime

class UserVideosService:

    def __init__(self,videoRepository:VideoRepository):
        self.videoRepository = videoRepository

    def getVideosList(self,tokenUser:str, offSet: int) -> json:
        if offSet < 0:
            raise HTTPException(status_code=403,detail="Offset deve ser maior que 0")
        
        DATAS_PER_PAGE = 5
        offSet = offSet * DATAS_PER_PAGE
        datas = self.videoRepository.getListVideos(tokenUser,offSet)
        return self.convertDictToArray(datas)
    
    def convertDictToArray(self,data:dict) -> json:
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