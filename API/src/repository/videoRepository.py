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

    def createVideo(self, url: str, videoDuration: int,userId:bytes) -> str:

        now = datetime.now()
        formattedDate = now.strftime("%Y-%m-%d")

        videoId = uuid.uuid4().bytes

        self.Db.createConnection()

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

    def getVideosByUser(self, userId: bytes, offSet: int) -> dict:
    
        self.Db.createConnection()

        sql = """
                SELECT tbv.videoId,tbv.videoDate,tbv.videoTitle,tbv.videoStatus FROM tb_video AS tbv 
                INNER JOIN tb_user AS tbu ON tbu.userId = tbv.idAdmin
                WHERE tbv.isDeleted = FALSE AND tbv.idAdmin = %s
                ORDER BY tbv.videoDate DESC
                LIMIT 5 OFFSET %s;
              """
        try:
            self.Db.myCursor.execute(sql, (userId, offSet))
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

    def getVideoCountByUser(self, userId: bytes) -> int:

        self.Db.createConnection()

        sql = """
                SELECT COUNT(videoId) AS countVideo FROM tb_video WHERE idAdmin = %s AND isDeleted = FALSE;
              """
        try:
            self.Db.myCursor.execute(sql, (userId,))
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
            userIdBytes = userId if userId else None
            self.Db.myCursor.execute(sql, (userIdBytes, offset))
            rows = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if not rows:
                return None

            return rows

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar vídeos da página inicial")

    def searchVideosByTitle(self, param: str, userId: str) -> dict:
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
            self.Db.myCursor.execute(sql, (userId, param))
            rows = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if len(rows) == 0:
                return None

            return rows

        except Exception as e:
            print(e)
            raise ValueError("Erro ao buscar vídeos da pesquisa feita")

    def getVideoForStreaming(self, videoId: str,userId:bytes) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                SELECT tbv.videoDate,tu.userName,tbv.videoTitle,tbv.videoUrl ,tbv.videoId,tbvr.videoLikes,tbvr.videoDislikes,
                tbv.videoSubTitles,COALESCE(tbuvr.reactionType, 0) AS reaction, tbv.videoDuration
                FROM tb_video AS tbv 
                INNER JOIN tb_user AS tu ON tu.userId = tbv.idAdmin
                INNER JOIN tb_videoReaction AS tbvr ON tbvr.videoId = tbv.videoId
                LEFT JOIN tb_userVideoReaction AS tbuvr ON tbuvr.videoId = tbv.videoId AND tbuvr.userId = %s
                WHERE tbv.videoId = %s AND tbv.isDeleted = FALSE AND tbv.isVideoAvailable = TRUE 
                AND tbv.videoStatus = 'READY' AND tbv.videoTitle <> '' AND tbv.thumbnailUrl <> ''
                AND tu.userName <> '' AND tbv.isDeleted = FALSE AND tbv.videoDuration > 0 ORDER BY tbuvr.createdAt DESC LIMIT 1;

              """
        try:
            self.Db.myCursor.execute(sql, (userId,videoIdBytes))
            row = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar dados do vídeo para streaming {e}")

    def updateWatchTime(self, userId: bytes, videoId: str, timeWatched: int) -> None:

        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                UPDATE tb_videoWatchTime SET watchedSeconds = %s WHERE userID = %s AND videoID = %s;     
              """
        try:
            self.Db.myCursor.execute(sql, (timeWatched, userId, videoIdBytes))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao adicionar tempo asistido ao vídeo")

    def getWatchedSeconds(self, userId: bytes, videoId: str) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                SELECT tbv.videoDuration FROM tb_videoWatchTime AS tbvwt
                INNER JOIN tb_video AS tbv
                ON tbvwt.videoID = tbv.videoId   
                WHERE tbvwt.userID = %s AND tbvwt.videoID = %s  
              """
        try:
            self.Db.myCursor.execute(sql, (userId, videoIdBytes))

            row = self.Db.myCursor.fetchone()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar dados de tempo assistido")

    def addToHistory(self, videoId: str, userId: bytes) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes

        now = datetime.now()
        SqlDate = now.strftime("%Y-%m-%d")
        historyId = uuid.uuid4().bytes

        self.Db.createConnection()

        sql = """
               INSERT INTO tb_videoHistory (historyId,userId,videoId,DateVideo) VALUES (%s,%s,%s,%s);    
              """
        try:
            self.Db.myCursor.execute(sql, (historyId, userId, videoIdBytes, SqlDate))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao inserir video no historico {e}")

    def initializeWatchTime(self, videoId: str, userId: bytes) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
               INSERT INTO tb_videoWatchTime (userID, videoID, watchedSeconds) 
               VALUES (%s, %s, %s);
              """
        try:
            self.Db.myCursor.execute(sql, (userId, videoIdBytes, 0))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except mysql.connector.Error as err:
            self.Db.closeConnection()
            if err.errno == errorcode.ER_DUP_ENTRY:
                return None
            else:
                raise ValueError(f"Erro ao inserir vídeo no histórico: {err}")

    def getUserHistory(self, userId: str, offset: bytes) -> dict:
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
                    tbv.isDeleted = FALSE AND
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
            self.Db.myCursor.execute(sql, (userId, offset))
            row = self.Db.myCursor.fetchall()

            self.Db.myDb.commit()
            self.Db.closeConnection()

            if row is None or len(row) == 0:
                return None

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao buscar historico de vídeos {e}")
    
    def getVideoReaction(self,videoId:str,userId:bytes) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes

        self.Db.createConnection()

        sql = """
                SELECT reactionType FROM tb_userVideoReaction WHERE userId = %s AND videoId = %s ORDER BY createdAt DESC LIMIT 1;
              """
        try:
            self.Db.myCursor.execute(sql, (userId,videoIdBytes))
            row = self.Db.myCursor.fetchone()
        
            self.Db.myDb.commit()
            self.Db.closeConnection()

            return row

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao obter reação do vídeo{e}")
    
    def isVideoExists(self,videoId:str) -> dict:
        videoIdBytes = uuid.UUID(videoId).bytes
        
        self.Db.createConnection()

        sql = """
                SELECT videoId FROM tb_video WHERE videoId = %s
              """
        try:
            self.Db.myCursor.execute(sql, (videoIdBytes,))
            row = self.Db.myCursor.fetchone()
        
            self.Db.myDb.commit()
            self.Db.closeConnection()
            if row is None or row[0] is None:
                return None
            
            idVideoStr = uuid.UUID(bytes=row[0])
            return str(idVideoStr)

        except Exception as e:
            print(e)
            raise ValueError(f"Erro ao obter id do vídeo{e}")

    def addLikeAndReaction(self, videoId: str, userId: bytes, isUserChangingReaction:bool, reactionType: int = 1) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userReactionId = uuid.uuid4().bytes
        
        createdAt = datetime.now()

        try:
            self.Db.createConnection()
            conn = self.Db.myDb
            cursor = self.Db.myCursor
            conn.autocommit = False

            LIKE = self.getQueryLike(isUserChangingReaction=isUserChangingReaction)
            print("query: ",LIKE)
            cursor.execute(LIKE, (videoIdBytes,))

            REACTION = """
                INSERT INTO tb_userVideoReaction 
                    (userVideoReactionId, userId, videoId, createdAt, reactionType) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(REACTION, (userReactionId, userId, videoIdBytes, createdAt, reactionType))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print("aqui: ",e)
            raise ValueError("Erro ao adicionar like e reação do usuário")

        finally:
            self.Db.closeConnection()

    def addDislikeAndReaction(self, videoId: str, userId: bytes, isUserChangingReaction:bool,reactionType: int = -1,) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userReactionId = uuid.uuid4().bytes
        
        createdAt = datetime.now()

        try:
            self.Db.createConnection()
            conn = self.Db.myDb
            cursor = self.Db.myCursor
            conn.autocommit = False

            DISLIKE = self.getQueryDisLike(isUserChangingReaction=isUserChangingReaction)
            cursor.execute(DISLIKE, (videoIdBytes,))

            REACTION = """
                INSERT INTO tb_userVideoReaction 
                    (userVideoReactionId, userId, videoId, createdAt, reactionType) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(REACTION, (userReactionId, userId, videoIdBytes, createdAt, reactionType))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(e)
            raise ValueError("Erro ao adicionar dislike e reação do usuário")

        finally:
            self.Db.closeConnection()

    def removeLikeUser(self, videoId: str, userId: bytes) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userReactionId = uuid.uuid4().bytes
        
        createdAt = datetime.now()

        try:
            self.Db.createConnection()
            conn = self.Db.myDb
            cursor = self.Db.myCursor
            conn.autocommit = False

            LIKE = """
                    UPDATE tb_videoReaction SET videoLikes = videoLikes - 1 WHERE videoID = %s
            """
            cursor.execute(LIKE, (videoIdBytes,))

            REACTION = """
                INSERT INTO tb_userVideoReaction 
                    (userVideoReactionId, userId, videoId, createdAt, reactionType) 
                VALUES (%s, %s, %s, %s, 0)
            """
            cursor.execute(REACTION, (userReactionId, userId, videoIdBytes, createdAt))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(e)
            raise ValueError("Erro ao adicionar dislike e reação do usuário")

        finally:
            self.Db.closeConnection()

    def removeDislikeUser(self, videoId: str, userId: bytes) -> None:
        videoIdBytes = uuid.UUID(videoId).bytes
        userReactionId = uuid.uuid4().bytes
        
        createdAt = datetime.now()

        try:
            self.Db.createConnection()
            conn = self.Db.myDb
            cursor = self.Db.myCursor
            conn.autocommit = False

            DISLIKE = """
                    UPDATE tb_videoReaction SET videoDislikes = videoDislikes - 1 WHERE videoID = %s
            """
            cursor.execute(DISLIKE, (videoIdBytes,))

            REACTION = """
                INSERT INTO tb_userVideoReaction 
                    (userVideoReactionId, userId, videoId, createdAt, reactionType) 
                VALUES (%s, %s, %s, %s, 0)
            """
            cursor.execute(REACTION, (userReactionId, userId, videoIdBytes, createdAt))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(e)
            raise ValueError("Erro ao adicionar dislike e reação do usuário")

        finally:
            self.Db.closeConnection()

    def getQueryLike(self,isUserChangingReaction:bool) -> str:
        query = ""
        if isUserChangingReaction:
            query = """
                UPDATE tb_videoReaction SET videoLikes = videoLikes + 1, videoDislikes = videoDislikes - 1 WHERE videoID = %s
            """
        else:
            query = """
                UPDATE tb_videoReaction SET videoLikes = videoLikes + 1 WHERE videoID = %s
            """

        return query

    def getQueryDisLike(self,isUserChangingReaction:bool) -> str:
        query = ""
        if isUserChangingReaction:
            query = """
                UPDATE tb_videoReaction SET videoDislikes = videoDislikes + 1, videoLikes = videoLikes - 1 WHERE videoID = %s
            """
        else:
            query = """
                UPDATE tb_videoReaction SET videoDislikes = videoDislikes + 1 WHERE videoID = %s
            """

        return query