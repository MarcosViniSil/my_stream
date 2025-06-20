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
                INSERT INTO tb_video (videoId, videoUrl, videoStatus,videoDuration, isVideoAvailable,videoDate,isDeleted, idAdmin) 
                VALUES (%s, %s, %s,%s, %s, %s,%s,%s);
        """
        try:
            self.Db.myCursor.execute(sql, (videoId, url, VideoStatus.PROCESSING.value,videoDuration, False, formatted_date,False, idAdm))
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

        sql = """
                SELECT tbv.videoId,tbv.videoDate,tbv.videoTitle,tbv.videoStatus FROM tb_video AS tbv 
                INNER JOIN tb_user AS tbu ON tbu.userId = tbv.idAdmin
                WHERE tbv.isDeleted = FALSE AND tbv.idAdmin = %s
                ORDER BY tbv.videoDate DESC
                LIMIT 5 OFFSET %s;
        """
        try:
            self.Db.myCursor.execute(sql, (idAdm,offSet))
            myresult = self.Db.myCursor.fetchall()
            self.Db.myDb.commit()
            self.Db.closeConnection()
            return myresult
        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar videos na base de dados",e)
    
    def getDatasToDeleteVideo(self,videoId:str) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                SELECT tu.userId,tbv.videoStatus,tbv.videoUrl FROM tb_video as tbv INNER JOIN tb_user as tu ON tbv.idAdmin = tu.userId WHERE tbv.videoId = %s;
        """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            result = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()
            self.Db.closeConnection()
            
            if result:
                data = {
                    "userId": result[0],
                    "videoStatus": result[1],
                    "videoUrl": result[2],
                }
                return data
            else:
                return None
        except Exception as e:
            print(e)
            raise ValueError("Erro ao verificar dados do vídeo para exclusão")
    
    def changeVideoToDeleted(self, idVideo:str) -> None:
        idVideoBytes = uuid.UUID(idVideo).bytes
        self.Db.createConnection()

        sql = """
                UPDATE tb_video SET isDeleted = TRUE WHERE videoId = %s
        """
        try:
            self.Db.myCursor.execute(sql, (idVideoBytes,))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)
            raise ValueError("Erro ao deletar vídeo, tente novamente")

    def deleteVideoById(self,idVideo:str) -> None :
        idVideoBytes = uuid.UUID(idVideo).bytes
 
        self.Db.createConnection()

        sql = """
                DELETE FROM tb_video WHERE videoId = %s;
        """
        try:
            self.Db.myCursor.execute(sql, (idVideoBytes,))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)
            raise ValueError("Erro ao deletar vídeo, tente novamente")
        

        