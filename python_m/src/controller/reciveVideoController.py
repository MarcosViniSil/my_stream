import os
import shutil
from src.db.connectionDb import ConnectionDB

from src.models.videoResponse import VideoResponse
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from src.service.reciveVideo import ReciveVideo
import uvicorn

from fastapi import FastAPI, File, UploadFile,APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()
bucket = Bucket()
db = ConnectionDB()
videoRepository = VideoRepository(db)
reciveVideo = ReciveVideo(bucket,videoRepository)


@router.post("/upload/video", response_model=VideoResponse)
async def upload_video(file: UploadFile = File(...)):
    return await reciveVideo.processReceivedVideo(file)



