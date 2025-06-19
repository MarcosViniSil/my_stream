from fastapi import APIRouter, File, UploadFile, Depends,Form
from src.models.dependencies import getReceiveMetaData, getUserVideosRepository

from src.models.metadataResponse import MetadataResponse
from uuid import UUID
from src.service.userVideosService import UserVideosService

routerUserVideos = APIRouter()

@routerUserVideos.post("/user/videos")
async def get_user_videos(tokenUser = Form(...),offset: int = 0,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideosList(tokenUser,offset)

@routerUserVideos.delete("/user/video")
async def delete_video_user(tokenUser = Form(...),videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.deleteVideo(videoId,tokenUser)