from fastapi import Depends
import uuid
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB

class VideoRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def insertUrlDb(self, url: str) -> str:
        VideoStatus.READY
        videoIdBytes = uuid.uuid4().bytes 
        self.Db.createConnection()

        #TODO -> change logic to recive id_user from body

        sql = """
                INSERT INTO tb_video (videoId, videoUrl, videoStatus, isVideoAvailable, idAdmin) 
                VALUES (%s, %s, %s, %s, UNHEX(REPLACE(%s, '-', '')));
        """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes, url, VideoStatus.PROCESSING.value, False, '3f06af63-a93c-11e4-9797-00505690773f'))
            self.Db.myDb.commit()
            self.Db.closeConnection()
            uuid_obj = uuid.UUID(bytes=videoIdBytes)
            return str(uuid_obj)
        except Exception as e:
            raise ValueError("Erro ao inserir dados no banco de dados",e)
        