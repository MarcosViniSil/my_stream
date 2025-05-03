from src.db.connectionDb import ConnectionDB
from src.repository.metaDataRepository import MetaDataRepository
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from src.service.receiveMetaData import ReceiveMetadaService
from src.service.receiveVideo import ReciveVideo

bucket = Bucket()
db = ConnectionDB()
video_repository = VideoRepository(db)
metadataRepository = MetaDataRepository(db)
recive_video = ReciveVideo(bucket, video_repository)
receiveMetadata = ReceiveMetadaService(bucket,metadataRepository)

def getReciveVideo():
    return recive_video

def getReceiveMetaData():
    return receiveMetadata
