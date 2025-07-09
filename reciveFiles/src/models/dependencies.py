from src.repository.userRepository import UserRepository
from src.service.queueService import QueueService
from src.db.connectionDb import ConnectionDB
from src.repository.metaDataRepository import MetaDataRepository
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from src.service.receiveMetaData import ReceiveMetadaService
from src.service.receiveVideo import ReciveVideo
from src.service.userService import UserService
from src.service.userVideosService import UserVideosService
from src.service.userMetadatasService import UserMetaDatasService

db = ConnectionDB()
video_repository = VideoRepository(db)

bucket = Bucket()
queueService = QueueService()

userVideosRepository = UserVideosService(video_repository,bucket)
metadataRepository = MetaDataRepository(db)
userRepository = UserRepository(db)

userMetadatas = UserMetaDatasService(metadataRepository)
recive_video = ReciveVideo(bucket, video_repository,queueService)
receiveMetadata = ReceiveMetadaService(bucket,metadataRepository)
userService = UserService(userRepository)

def getReciveVideo():
    return recive_video

def getReceiveMetaData():
    return receiveMetadata

def getUserVideosRepository():
    return userVideosRepository

def getUserMetadatas():
    return userMetadatas

def getUserService():
    return userService