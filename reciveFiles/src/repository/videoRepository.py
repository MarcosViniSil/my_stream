import uuid
from uuid import UUID
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB
from uuid import UUID
import mysql.connector
from datetime import datetime

class VideoRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def insertDatasVideo(self, url: str,videoDuration:int) -> str:
       
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d')

        idAdm = uuid.UUID('3f06af63-a93c-11e4-9797-00505690773f').bytes
 
        videoId = uuid.uuid4().bytes
        self.Db.createConnection()

        #TODO -> change logic to recive id_user from body

        sql = """
                INSERT INTO tb_video (videoId, videoUrl, videoStatus,videoDuration, isVideoAvailable,videoDate, idAdmin) 
                VALUES (%s, %s, %s,%s, %s, %s, %s);
        """
        try:
            self.Db.myCursor.execute(sql, (videoId, url, VideoStatus.PROCESSING.value,videoDuration, False, formatted_date, idAdm))
            self.Db.myDb.commit()
            self.Db.closeConnection()
            uuid_obj = uuid.UUID(bytes=videoId)
            return str(uuid_obj)
        except Exception as e:
            print(e)
            raise ValueError("Erro ao inserir url do vídeo",e)
        
    def getListVideos(self,idUser:str, offSet: int) -> dict :
        idAdm = uuid.UUID('3f06af63-a93c-11e4-9797-00505690773f').bytes
 
        self.Db.createConnection()

        #TODO -> change logic to recive id_user from body

        sql = """
                SELECT tbv.videoDate,tbv.videoTitle,tbv.videoStatus FROM tb_video AS tbv 
                INNER JOIN tb_user AS tbu ON tbu.userId = tbv.idAdmin
                ORDER BY tbv.videoDate DESC
                LIMIT 5 OFFSET %s;
        """
        try:
            self.Db.myCursor.execute(sql, (offSet,))
            myresult = self.Db.myCursor.fetchall()
            self.Db.myDb.commit()
            self.Db.closeConnection()
            return myresult
        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar videos na base de dados",e)
        

        