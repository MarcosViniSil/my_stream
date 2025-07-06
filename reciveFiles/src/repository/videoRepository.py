from typing import Optional
import uuid
from uuid import UUID
from src.enum.statusVideoEnum import VideoStatus
from src.db.connectionDb import ConnectionDB
from uuid import UUID
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

class VideoRepository:

    def __init__(self, db: ConnectionDB):
        self.Db = db

    def createVideo(self, url: str, videoDuration: int) -> str:

        now = datetime.now()
        formattedDate = now.strftime("%Y-%m-%d")

        userId = uuid.UUID("3f06af63-a93c-11e4-9797-00505690773f").bytes

        videoId = uuid.uuid4().bytes

        self.Db.createConnection()

        # TODO -> change logic to receive user id from body

        sql = """
                INSERT INTO tb_video (videoId, videoUrl, videoStatus,videoDuration, isVideoAvailable,videoDate,isDeleted, idAdmin) 
                VALUES (%s, %s, %s,%s, %s, %s,%s,%s);
        """
        try:
            self.Db.myCursor.execute(
                sql,
                (
                    videoId,
                    url,
                    VideoStatus.PROCESSING.value,
                    videoDuration,
                    False,
                    formattedDate,
                    False,
                    userId,
                ),
            )
            self.Db.myDb.commit()
            self.Db.closeConnection()

            uuidObj = uuid.UUID(bytes=videoId)

            return str(uuidObj)

        except Exception as e:
            print(e)
            raise ValueError("Erro ao inserir url do vídeo", e)

    def initializeVideoReactions(self, videoId: str) -> None:

        videoId = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                INSERT INTO tb_videoReaction (videoId,videoLikes,videoDislikes) VALUES (%s,0,0);
        """
        try:
            self.Db.myCursor.execute(sql, (videoId,))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError("Erro ao criar likes e deslikes iniciais", e)

    def getVideosByUser(self, userId: str, offSet: int) -> dict:
        userIdBytes = uuid.UUID("3f06af63-a93c-11e4-9797-00505690773f").bytes

        self.Db.createConnection()

        sql = """
                SELECT tbv.videoId,tbv.videoDate,tbv.videoTitle,tbv.videoStatus FROM tb_video AS tbv 
                INNER JOIN tb_user AS tbu ON tbu.userId = tbv.idAdmin
                WHERE tbv.isDeleted = FALSE AND tbv.idAdmin = %s
                ORDER BY tbv.videoDate DESC
                LIMIT 5 OFFSET %s;
              """
        try:
            self.Db.myCursor.execute(sql, (userIdBytes, offSet))
            myresult = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            return myresult

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar videos na base de dados", e)

    def getVideoDetails(self, videoId: str) -> dict:
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

    def markVideoAsDeleted(self, videoId: str) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                UPDATE tb_video SET isDeleted = TRUE WHERE videoId = %s
        """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError("Erro ao deletar vídeo, tente novamente")

    def permanentlyDeleteVideo(self, videoId: str) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                DELETE FROM tb_video WHERE videoId = %s;
        """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError("Erro ao deletar vídeo, tente novamente")

    def getVideoCountByUser(self, userId: str) -> int:
        userIdBytes = uuid.UUID("3f06af63-a93c-11e4-9797-00505690773f").bytes

        self.Db.createConnection()

        sql = """
                SELECT COUNT(videoId) AS countVideo FROM tb_video WHERE idAdmin = %s AND isDeleted = FALSE;
              """
        try:
            self.Db.myCursor.execute(sql, (userIdBytes,))
            myresult = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            return myresult[0] if myresult[0] is not None else 0

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar quantidade de vídeos do usuário", e)

    def getVideoStatus(self, videoId: str) -> VideoStatus:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                SELECT videoStatus FROM tb_video WHERE videoId = %s;
        """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            result = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            return result

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar status do vídeo solicitado")

    def getVideoFeed(self, offset: int, userId: Optional[str]) -> dict:

        self.Db.createConnection()

        sql = """
            SELECT tbv.videoDate, tu.userName, tbv.videoTitle, tbv.thumbnailUrl, tbv.videoDuration, tbv.videoId,
                   COALESCE(tbwt.watchedSeconds, 0) AS watchedSeconds
            FROM tb_video AS tbv
            INNER JOIN tb_user AS tu ON tu.userId = tbv.idAdmin
            LEFT JOIN tb_videoWatchTime AS tbwt 
             ON tbwt.videoID = tbv.videoId AND tbwt.userID = %s
            WHERE tbv.isDeleted = FALSE AND tbv.isVideoAvailable = TRUE 
             AND tbv.videoStatus = 'READY' AND tbv.videoTitle <> '' AND tbv.thumbnailUrl <> ''
             AND tu.userName <> '' AND tbv.videoDuration > 0
            ORDER BY tbv.videoDate DESC, tbv.videoId DESC
            LIMIT 10 OFFSET %s;
        """

        try:
            userIdBytes = uuid.UUID(userId).bytes if userId else None
            self.Db.myCursor.execute(sql, (userIdBytes, offset))
            rows = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if not rows:
                return None

            return rows

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar vídeos da página inicial")

    def searchVideosByTitle(self, param: str, userId: str) -> dict:
        userIdBytes = uuid.UUID(userId).bytes

        self.Db.createConnection()

        sql = """
               SELECT tbv.videoDate,tu.userName,tbv.videoTitle,tbv.thumbnailUrl,tbv.videoDuration,tbv.videoId,
               COALESCE(tbwt.watchedSeconds, 0) AS watchedSeconds FROM tb_video AS tbv 
               INNER JOIN tb_user AS tu ON tu.userId = tbv.idAdmin
               LEFT JOIN tb_videoWatchTime AS tbwt ON tbwt.videoID = tbv.videoId AND tbwt.userID = %s
               WHERE tbv.isDeleted = FALSE AND tbv.isVideoAvailable = TRUE 
               AND tbv.videoStatus = 'READY' AND tbv.videoTitle <> '' AND tbv.thumbnailUrl <> ''
               AND tu.userName <> '' AND tbv.videoDuration > 0  AND tbv.videoTitle LIKE %s
               ORDER BY tbv.videoDate DESC, tbv.videoId DESC

              """
        param = f"%{param}%"
        try:
            self.Db.myCursor.execute(sql, (userIdBytes, param))
            rows = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if len(rows) == 0:
                return None

            return rows

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar vídeos da pesquisa feita")

    def getVideoForStreaming(self, videoId: str) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes
        self.Db.createConnection()

        sql = """
               SELECT tbv.videoDate,tu.userName,tbv.videoTitle,tbv.videoUrl ,tbv.videoId,tbvr.videoLikes,tbvr.videoDislikes,
               tbv.videoSubTitles
               FROM tb_video AS tbv 
               INNER JOIN tb_user AS tu ON tu.userId = tbv.idAdmin
               INNER JOIN tb_videoReaction AS tbvr ON tbvr.videoId = tbv.videoId
               WHERE tbv.videoId = %s AND tbv.isDeleted = FALSE AND tbv.isVideoAvailable = TRUE 
               AND tbv.videoStatus = 'READY' AND tbv.videoTitle <> '' AND tbv.thumbnailUrl <> ''
               AND tu.userName <> '' AND tbv.videoDuration > 0;

              """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            row = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar dados do vídeo para streaming {e}")

    def updateWatchTime(self, userId: str, videoId: str, timeWatched: int) -> None:

        videoIdBytes = uuid.UUID(videoId).bytes
        userIdBytes = uuid.UUID(userId).bytes

        self.Db.createConnection()

        sql = """
                UPDATE tb_videoWatchTime SET watchedSeconds = %s WHERE userID = %s AND videoID = %s;     
              """
        try:
            self.Db.myCursor.execute(sql, (timeWatched, userIdBytes, videoIdBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao adicionar tempo asistido ao vídeo")

    def getWatchedSeconds(self, userId: str, videoId: str) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes
        userIdBytes = uuid.UUID(userId).bytes

        self.Db.createConnection()

        sql = """
                SELECT tbv.videoDuration FROM tb_videoWatchTime AS tbvwt
                INNER JOIN tb_video AS tbv
                ON tbvwt.videoID = tbv.videoId   
                WHERE tbvwt.userID = %s AND tbvwt.videoID = %s  
              """
        try:
            self.Db.myCursor.execute(sql, (userIdBytes, videoIdBytes))

            row = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar dados de tempo assistido")

    def addToHistory(self, videoId: str, userId: str) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userIdBytes = uuid.UUID(userId).bytes

        now = datetime.now()
        SqlDate = now.strftime("%Y-%m-%d")
        historyId = uuid.uuid4().bytes

        self.Db.createConnection()

        sql = """
               INSERT INTO tb_videoHistory (historyId,userId,videoId,DateVideo) VALUES (%s,%s,%s,%s);    
              """
        try:
            self.Db.myCursor.execute(sql, (historyId, userIdBytes, videoIdBytes, SqlDate))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao inserir video no historico {e}")

    def initializeWatchTime(self, videoId: str, userId: str) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userIdBytes = uuid.UUID(userId).bytes

        self.Db.createConnection()

        sql = """
               INSERT INTO tb_videoWatchTime (userID, videoID, watchedSeconds) 
               VALUES (%s, %s, %s);
              """
        try:
            self.Db.myCursor.execute(sql, (userIdBytes, videoIdBytes, 0))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except mysql.connector.Error as err:
            self.Db.closeConnection()
            if err.errno == errorcode.ER_DUP_ENTRY:
                return None
            else:
                raise ValueError(f"Erro ao inserir vídeo no histórico: {err}")

    def getUserHistory(self, userId: str, offset: int) -> dict:
        userIdBytes = uuid.UUID(userId).bytes
        self.Db.createConnection()

        sql = """
               WITH ranked_videos AS (
			        SELECT tbvh.videoId,tbv.videoTitle,tbv.thumbnailUrl,tbvh.DateVideo,
                    tbwt.watchedSeconds,tbv.videoDuration,tbu.userName,ROW_NUMBER() 
			        OVER (PARTITION BY DATE(tbvh.DateVideo), tbvh.videoId 
			        ORDER BY tbvh.DateVideo DESC, tbvh.historyId DESC
		        ) as rn
                    FROM tb_videoHistory AS tbvh
                    INNER JOIN tb_video AS tbv 
                    ON tbv.videoId = tbvh.videoId
                    INNER JOIN tb_user AS tbu
                    ON tbu.userId = tbvh.userId
                    INNER JOIN tb_videoWatchTime AS tbwt
                    ON tbwt.userID = tbvh.userId AND tbwt.videoID = tbvh.videoId
                    WHERE 
                    tbv.videoStatus = 'READY' AND 
                    tbv.videoTitle <> '' AND 
                    tbv.thumbnailUrl <> '' AND 
                    tbv.videoDuration > 0 AND tbvh.userId = %s AND tbu.userName <> ''
                )
                SELECT 
                videoId, videoTitle, thumbnailUrl, DateVideo, watchedSeconds,videoDuration,userName
                FROM ranked_videos
                WHERE rn = 1 
                ORDER BY DateVideo DESC, videoId DESC
                LIMIT 20 OFFSET %s;

              """
        try:
            self.Db.myCursor.execute(sql, (userIdBytes, offset))
            row = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar historico de vídeos {e}")
