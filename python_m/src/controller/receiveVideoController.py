from fastapi import APIRouter, File, UploadFile, Depends
from src.models.dependencies import getReciveVideo
from src.models.videoResponse import VideoResponse
from src.service.receiveVideo import ReciveVideo

router = APIRouter()

@router.post("/upload/video", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    recive_video: ReciveVideo = Depends(getReciveVideo)
):
    return await recive_video.processReceivedVideo(file)
