from datetime import datetime
import uuid
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB
from uuid import UUID

class StreamRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def updateUrlVideo(self, url: str,videoId:str) -> None:
        idVideoBytes = uuid.UUID(videoId).bytes
        self.Db.createConnection()

        sql = """
                UPDATE tb_video SET videoUrl = %s, videoStatus = %s, isVideoAvailable = %s WHERE videoId = %s;
              """
        try:
            self.Db.myCursor.execute(sql, (url, VideoStatus.READY.value, True, idVideoBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            raise ValueError(f"Erro ao atualizar dados do vídeo {videoId} ",e)
        
    def updateStatusVideoToFail(self, videoId:str) -> None:
        idVideoBytes = uuid.UUID(videoId).bytes
        self.Db.createConnection()

        sql = """
                UPDATE tb_video SET videoStatus = %s WHERE videoId = %s;
              """
        try:
            self.Db.myCursor.execute(sql, (VideoStatus.FAIL.value,idVideoBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao atualizar status para fail do vídeo {videoId} ",e)
    
    def getOwnerEmail(self, videoId:str) -> str:
        idVideoBytes = uuid.UUID(videoId).bytes
        self.Db.createConnection()

        sql = """
                SELECT tu.userEmail FROM tb_video as tbv INNER JOIN tb_user AS tu ON tbv.idAdmin = tu.userId WHERE tbv.videoId = %s;
              """
        try:
            self.Db.myCursor.execute(sql, (idVideoBytes,))
            myresult = self.Db.myCursor.fetchone()
            if len(myresult) == 0:
                raise ValueError("Email não encontrado")
            self.Db.myDb.commit()
            self.Db.closeConnection()
            return str(myresult[0])
        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao atualizar status para fail do vídeo {videoId} ",e)
        
    def getVideoByStatusFail(self) -> dict:
        self.Db.createConnection()

        sql = """
                SELECT videoId,thumbnailUrl,videoUrl,videoSubTitles FROM tb_video WHERE videoStatus = 'FAIL' LIMIT 5;
              """
        try:
            self.Db.myCursor.execute(sql,)
            myresult = self.Db.myCursor.featchAll()
            if len(myresult) == 0:
                return []
            self.Db.myDb.commit()
            self.Db.closeConnection()
            return myresult
        except Exception as e:
            print(e)
            raise ValueError(f"erro ao obter vídeo que possuem status FAIL, erro: {e}",e)
        
    def getVideoByDeleted(self) -> dict:
        self.Db.createConnection()

        sql = """
                SELECT videoId,thumbnailUrl,videoUrl,videoSubTitles FROM tb_video WHERE isDeleted = TRUE LIMIT 5;
              """
        try:
            self.Db.myCursor.execute(sql,)
            myresult = self.Db.myCursor.featchAll()
            if len(myresult) == 0:
                return []
            self.Db.myDb.commit()
            self.Db.closeConnection()
            return myresult
        except Exception as e:
            print(e)
            raise ValueError(f"erro ao obter vídeo que possuem status FAIL, erro: {e}",e)

    def deleteRowById(self,id:bytes) -> None:
        videoIdBytes = uuid.UUID(id).bytes

        self.Db.createConnection()
        
        sql = """
                DELETE FROM tb_video WHERE videoId = %s
              """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)
        
    def insertSubTitles(self, videoId:str, psthSubTitles:str) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()
        
        sql = """
                UPDATE tb_video SET videoSubTitles = %s WHERE videoId = %s
              """
        try:
            self.Db.myCursor.execute(sql, (psthSubTitles,videoIdBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)