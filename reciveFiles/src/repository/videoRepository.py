import uuid
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB
from uuid import UUID
import mysql.connector

class VideoRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def insertUrlDb(self, url: str) -> str:
        idAdm = uuid.UUID('3f06af63-a93c-11e4-9797-00505690773f').bytes
 
        videoId = uuid.uuid4().bytes
        self.Db.createConnection()

        #TODO -> change logic to recive id_user from body

        sql = """
                INSERT INTO tb_video (videoId, videoUrl, videoStatus, isVideoAvailable, idAdmin) 
                VALUES (%s, %s, %s, %s, %s);
        """
        try:
            self.Db.myCursor.execute(sql, (videoId, url, VideoStatus.PROCESSING.value, False, idAdm))
            self.Db.myDb.commit()
            self.Db.closeConnection()
            uuid_obj = uuid.UUID(bytes=videoId)
            return str(uuid_obj)
        except Exception as e:
            raise ValueError("Erro ao inserir url do vídeo",e)
        

        