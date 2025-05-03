import uuid
from fastapi import Depends
from uuid import UUID
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB

class MetaDataRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def insertMetaData(self, uuidVideo: UUID, videoTitle: str, urlThumbnail:str) -> None:
        
        #TODO get id admin to make relashionship between metadata and video
        videoIdBytes = uuidVideo.bytes
        self.Db.createConnection()
        sql = """
                UPDATE tb_video SET videoTitle = %s, thumbnailUrl = %s WHERE videoId = %s;
              """
        try:
            self.Db.myCursor.execute(sql, (videoTitle,urlThumbnail,videoIdBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print("a",e)
            raise ValueError("Erro ao inserir metadados no banco de dados",e)
        
    def isUUIDExistsOnDataBase(self, uuidVideo: UUID) -> bool:
        videoIdBytes = uuidVideo.bytes
        self.Db.createConnection()
        sql = """
                SELECT videoId FROM tb_video WHERE videoID = %s
              """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            myresult = self.Db.myCursor.fetchall()
            return len(myresult) == 1 and videoIdBytes == myresult[0][0]
        except Exception as e:
            print("a",e)
            raise ValueError("Erro ao inserir metadados no banco de dados",e)
        