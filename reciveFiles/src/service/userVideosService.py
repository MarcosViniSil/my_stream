from typing import List
import uuid
from fastapi import HTTPException
from src.models.timeWatched import TimeWatched
from src.models.videoStreaming import VideoStreaming
from src.models.videosHistory import VideosHistory
from src.repository.videoRepository import VideoRepository
from datetime import datetime
from src.enum.statusVideoEnum import VideoStatus
from src.models.videoPageInitialReponse import VideoResponse
from src.service.bucket import Bucket
from collections import defaultdict

MONTHS_PT = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}

DAYS_PT = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]


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
            dateFormated = datetime.strptime(str(date), '%Y-%m-%d').strftime('%d/%m/%Y')
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
        
    def getVideosInitialPage(self,offset:int,tokenUser:str) -> VideoResponse:
        if offset < 0:
            raise HTTPException(status_code=400,detail="Offset inválido")
        userId = ""
        print(tokenUser)
        if tokenUser is None:
            print("is none")
            userId = None
        else:
            userId = '3f06af63-a93c-11e4-9797-00505690773f'

        videosPerPage = 10
        offset *= videosPerPage
        try:
            rows = self.videoRepository.getVideos(offset,userId)
            if rows is None:
                return []
            reponse = [VideoResponse(
                    videoDate=self.convertDate(str(row[0])),
                    userName=row[1],
                    videoTitle=row[2],
                    thumbnailUrl=row[3],
                    videoDuration = row[4],
                    videoId = self.convertUUID(row[5]),
                    timeWatched = row[6]
                ) for row in rows]
            return reponse
        
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao buscar os vídeos da página inicial$ {e}")
        
    def getVideosBasedOnUserQuery(self,param:str) -> VideoResponse:
            if not param or len(param) == 0 or len(param) > 100:
                raise HTTPException(status_code=400,detail="parametro inválido")

            try:
                rows = self.videoRepository.getVideosBasedString(param)
                if rows is None:
                    return []
                reponse = [VideoResponse(
                        videoDate=self.convertDate(str(row[0])),
                        userName=row[1],
                        videoTitle=row[2],
                        thumbnailUrl=row[3],
                        videoDuration = row[4],
                        videoId = self.convertUUID(row[5]),
                        timeWatched = row[6]
                    ) for row in rows]
                return reponse

            except Exception as e:
                raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao buscar os vídeos da pesquisa{e}")
    
    def getDatasVideoStreaming(self, videoId:str) -> VideoStreaming:
        if not videoId or len(videoId) == 0:
            raise HTTPException(status_code=400,detail=f"id inválido para busca")
        
        try:
                row = self.videoRepository.getVideoDatasToStreaming(videoId)
                if row is None:
                    raise HTTPException(status_code=400,detail=f"O vídeo solicitado não foi encontrado")
                reponse = VideoStreaming(
                        videoDate=self.convertDate(str(row[0])),
                        userName=row[1],
                        videoTitle=row[2],
                        videoUrl=row[3],
                        videoId = self.convertUUID(row[4]),
                        likes = row[5],
                        dislikes = row[6]
                    ) 
                reponse.videoUrl = self.bucket.generatePresignedUrl(reponse.videoUrl)
                return reponse

        except Exception as e:
                raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao buscar os vídeos da pesquisa {e}")

    def insertVideoOnHistory(self,videoId:str,tokenUser:str) -> dict:
        #TODO recover id user based on token
        userId = '3f06af63-a93c-11e4-9797-00505690773f'
        
        if not self.isUUidValid(videoId):
            raise HTTPException(status_code=400,detail=f"id de vídeo inválido")
        
        try:
            self.videoRepository.createHistoryVideo(videoId,userId)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao inserir vídeo no histórico {e}")
        
        try:
            self.videoRepository.createTimeWatched(videoId,userId)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao inserir valor inicial assistido {e}")
        
        return {"message":"sucesso"}
    
    def addTimeWatched(self,tokenUser:str,videoId:str,timeAtVideo:int) -> None:
        print("Valor que será atualizado ",timeAtVideo)
        #TODO recover id user based on token
        userId = '3f06af63-a93c-11e4-9797-00505690773f'
        try:
            datas = self.videoRepository.getHistoryWatched(userId,videoId)
            if datas is None:
                raise HTTPException(status_code=400,detail=f"Não foi possível encontrar dados de tempo assistido")
            
            if datas[0] is None:
                raise HTTPException(status_code=400,detail=f"Não foi possível encontrar dados de tempo assistido")
            
            datas = TimeWatched(videoDuration=datas[0])

            if timeAtVideo >= datas.videoDuration:
                return {"message":"sucesso"} 
            
            if timeAtVideo < 0:
                timeAtVideo = 0
            elif timeAtVideo > datas.videoDuration:
                timeAtVideo = datas.videoDuration

            self.videoRepository.insertTimeWatched(userId,videoId,timeAtVideo)
            return {"message":"sucesso"}
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao inserir tempo assistido {e}")
            
    
    def getHistoryVideosByUserId(self,tokenUser:str,offset:int) -> VideosHistory:
        #TODO recover id user based on token
        userId = '3f06af63-a93c-11e4-9797-00505690773f'
        if  offset < 0:
            raise HTTPException(status_code=400,detail=f"offset inválido")
        
        dataPerPage = 20
        offset *= dataPerPage
        
        try:
                rows = self.videoRepository.getHistoryVideosUser(userId,offset)
                if rows is None:
                    return []
                
                reponse = [VideosHistory(
                        videoId=self.convertUUID(row[0]),
                        videoTitle=str(row[1]),
                        thumbnailUrl=str(row[2]),
                        dateVideo=self.convertDate(str(row[3])),
                        lastTime = int(row[4]),
                        videoDuration = int(row[5]),
                        userName = str(row[6])
                    ) for row in rows]
                
                result = self.convertListHistoryVideos(reponse)
                print(result)
                return sorted(result, key=lambda x: x['date'], reverse=True)
        
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao buscar videos do histórico {e}")
    

    def convertListHistoryVideos(self,reponse:List[VideosHistory]) -> dict:
        grouped = defaultdict(list)
        
        for video in reponse:
            dateVideo = video.dateVideo
            del video.dateVideo
            grouped[dateVideo].append(video.model_dump())  
            
            result = [
                        {
                            "date": data,
                            "dateText":self.convertDateToText(data),
                            "videos": videos
                        }
            for data, videos in grouped.items()]  

        return result

    def convertDateToText(self, date: str) -> str:
        
        obj = datetime.strptime(date, "%d/%m/%Y")
        return self.defineMessageHistoryDays(obj)

    def defineMessageHistoryDays(self,date:datetime) -> str:
        now = datetime.now().date()
        daysDiference = (now - date.date()).days
        if daysDiference == 0:
            return "Hoje"
        elif daysDiference == 1:
            return "Ontem"
        elif daysDiference >= 2 and daysDiference <= 6:
            return DAYS_PT[date.weekday()]
        else:
            monthName = MONTHS_PT[date.month]
            dayName = DAYS_PT[date.weekday()]
            return f"{dayName}, {date.day} de {monthName}"
    
    def convertDate(self,date:str) -> str:
        dateFormated = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
        return dateFormated
    
    def convertUUID(self,id:str) -> str:
        return str(uuid.UUID(bytes=id))
    
    def isUUidValid(self, val: str):
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            return False