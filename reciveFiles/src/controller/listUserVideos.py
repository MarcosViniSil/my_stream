from fastapi import APIRouter, File, UploadFile, Depends,Form,Query
from src.models.dependencies import getReceiveMetaData, getUserMetadatas, getUserVideosRepository
from src.models.metadataResponse import MetadataResponse
from uuid import UUID
from src.service.userVideosService import UserVideosService
from src.service.userMetadatasService import UserMetaDatasService

routerUserVideos = APIRouter()

@routerUserVideos.post("/user/videos")
async def get_user_videos(tokenUser = Form(...),offset: int = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideosList(tokenUser,offset)

@routerUserVideos.delete("/user/video")
async def delete_video_user(tokenUser = Form(...),videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.deleteVideo(videoId,tokenUser)

@routerUserVideos.get("/user/metadatas/{videoId}")
async def get_metadatas_video(videoId : str,userMetadatasService: UserMetaDatasService = Depends(getUserMetadatas)):
    return userMetadatasService.getVideoMetadatas(videoId)

@routerUserVideos.post("/user/videos/quantity")
async def get_total_videos_user(tokenUser = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getTotalVideosByUser(tokenUser)

@routerUserVideos.get("/user/video/status/{videoId}")
async def get_status_video(videoId : str,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideoStatus(videoId)

@routerUserVideos.get("/videos/{offset}")
async def get_videos_inital_page(offset : int,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideosInitialPage(offset=offset)

@routerUserVideos.get("/videos/query/{param}")
async def get_videos_by_query(param : str,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideosBasedOnUserQuery(param)

@routerUserVideos.get("/streaming/video/{videoId}")
async def get_datas_streaming_video(videoId : str,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getDatasVideoStreaming(videoId)

@routerUserVideos.post("/video/history")
async def insert_video_on_history(tokenUser = Form(...),videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.insertVideoOnHistory(videoId,tokenUser)

@routerUserVideos.get("/videos/history/")
async def get_history_videos(
    token: str = Query(...),
    offset: int = Query(0),
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
):
    return userVideosService.getHistoryVideosByUserId(token, offset)

@routerUserVideos.post("/video/time")
async def insert_time_watched(tokenUser = Form(...),videoId = Form(...),timeWatched:int = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.addTimeWatched(tokenUser=tokenUser,videoId=videoId,timeAtVideo=timeWatched)