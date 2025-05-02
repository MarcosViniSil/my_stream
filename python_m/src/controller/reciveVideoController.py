import os
import shutil
from src.db.connectionDb import ConnectionDB

from src.models.videoResponse import VideoResponse
from src.repository.videoRepository import VideoRepository
from src.service.bucket import Bucket
from src.service.reciveVideo import ReciveVideo

from fastapi import File, UploadFile,APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()
bucket = Bucket()
db = ConnectionDB()
videoRepository = VideoRepository(db)
reciveVideo = ReciveVideo(bucket,videoRepository)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/video",response_model=VideoResponse)
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        return JSONResponse(status_code=400, content={"error": "Apenas arquivos .mp4 são permitidos."})
    
    filePath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filePath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        return reciveVideo.processReceivedVideo(filePath)
    except Exception as e:
        return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})



