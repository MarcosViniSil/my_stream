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
                UPDATE tb_video SET videoStatus = %s WHERE videoId = '%s';
              """
        try:
            self.Db.myCursor.execute(sql, (VideoStatus.FAIL,idVideoBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()
        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao atualizar status para fail do vídeo {videoId} ",e)
    
    def getEmailVideoOwner(self, videoId:str) -> str:
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