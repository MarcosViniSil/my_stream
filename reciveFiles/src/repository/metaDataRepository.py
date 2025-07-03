import uuid
from fastapi import Depends
import mysql.connector
from uuid import UUID
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB
from src.exception.duplicateColumnException import DuplicateColumnException

class MetaDataRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def updateVideoMetadata(self, uuidVideo: str, videoTitle: str, urlThumbnail:str) -> None:
        
        #TODO get id admin to make relashionship between metadata and video

        try:
            videoIdBytes = uuid.UUID(uuidVideo).bytes
            self.Db.createConnection()
            sql = """
                UPDATE tb_video SET videoTitle = %s, thumbnailUrl = %s WHERE videoId = %s;
              """
            self.Db.myCursor.execute(sql, (videoTitle,urlThumbnail,videoIdBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except mysql.connector.errors.IntegrityError as e:
            error_msg = str(e)
            duplicate_column = None

            if "for key" in error_msg:
                duplicate_column = error_msg.split("for key ")[-1].strip(" '").split(".")[-1]

            raise DuplicateColumnException(f"{duplicate_column}")

        except Exception as e:
            raise ValueError("Erro ao inserir metadados no banco de dados ",e)
        
    def doesVideoExist(self, uuidVideo: str) -> bool:

        try:
            videoIdBytes = uuid.UUID(uuidVideo).bytes
            self.Db.createConnection()
            sql = """
                SELECT videoId FROM tb_video WHERE videoID = %s
              """
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            myresult = self.Db.myCursor.fetchall()
            self.Db.closeConnection()
            return len(myresult) == 1 and videoIdBytes == myresult[0][0]
        except Exception as e:
            raise ValueError("Erro ao verificar UUID",e)
        
    def isVideoBelongsToUser(self, idUser:str,uuidVideo: str) -> bool:
        
        try:
            idVideoBytes = uuid.UUID(uuidVideo).bytes
            userIdBytes  = uuid.UUID(idUser).bytes
            self.Db.createConnection()
            sql = """
                SELECT videoId FROM tb_video WHERE idAdmin = %s AND videoId = %s
              """
            self.Db.myCursor.execute(sql, (userIdBytes,idVideoBytes))
            myresult = self.Db.myCursor.fetchall()
            self.Db.closeConnection()
            print(myresult)
            return len(myresult) == 1 and idVideoBytes == myresult[0][0]
        except Exception as e:
            raise ValueError("Erro ao verificar UUID",e)
        
    def getVideoMetadata(self, uuidVideo: str) -> dict:
        try:
            videoIdBytes = uuid.UUID(uuidVideo).bytes
            self.Db.createConnection()
            sql = """
                SELECT thumbnailUrl,videoTitle FROM tb_video WHERE videoId = %s
              """
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            result = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()
            self.Db.closeConnection()

            if result:
                thumbnailUrl = ""
                title = ""
                if result[0] is None:
                    thumbnailUrl = ""
                else:
                    thumbnailUrl = str(result[0])
                
                if result[1] is None:
                    title = ""
                else:
                    title = str(result[1])
                
                data = {
                    "thumbnailUrl": thumbnailUrl,
                    "title": title,
                }
                return data
            else:
                return None
        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar metadados do vídeo")