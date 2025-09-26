from typing import Optional
from fastapi import APIRouter, File, UploadFile, Depends,Form,Query,Cookie
from src.models.dependencies import getReceiveMetaData, getUserMetadatas, getUserVideosRepository
from src.models.metadataResponse import MetadataResponse
from uuid import UUID
from src.service.userVideosService import UserVideosService
from src.service.userMetadatasService import UserMetaDatasService

routerUserVideos = APIRouter()

@routerUserVideos.post("/user/videos")
async def get_user_videos(offset: int = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideosList("token",offset)

@routerUserVideos.delete("/user/video") 
async def delete_video_user(
    #access_token: str = Cookie(...), 
    videoId: str = Query(...), 
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
):
    return userVideosService.deleteVideo(videoId, "token")

@routerUserVideos.get("/user/metadatas/{videoId}") 
async def get_metadatas_video(videoId : str,userMetadatasService: UserMetaDatasService = Depends(getUserMetadatas)):
    return userMetadatasService.getVideoMetadatas(videoId)

@routerUserVideos.post("/user/videos/quantity") 
async def get_total_videos_user(userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getTotalVideosByUser("token")

@routerUserVideos.get("/user/video/status/{videoId}")
async def get_status_video(videoId : str,userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.getVideoStatus(videoId)

@routerUserVideos.get("/videos") 
async def get_videos_inital_page(    
    #access_token: Optional[str] = Cookie(None),
    offset: int = Query(0),
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
):
    #userId = None if access_token == "None" else access_token
    return userVideosService.getVideosInitialPage(offset=offset,tokenUser="token")

@routerUserVideos.get("/videos/query") 
async def get_videos_by_query( 
    #access_token: Optional[str] = Cookie(None),
    param: str = Query(0),
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
    ):
    return userVideosService.getVideosBasedOnUserQuery(param,"token")

@routerUserVideos.get("/streaming/video/") 
async def get_datas_streaming_video(
    videoId : str = Query(...),
    #access_token: Optional[str] = Cookie(None),
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
    ):
    return userVideosService.getDatasVideoStreaming(videoId,"token")

@routerUserVideos.post("/video/history") 
async def insert_video_on_history(videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.insertVideoOnHistory(videoId,"token")

@routerUserVideos.get("/videos/history/") 
async def get_history_videos(
    #access_token: str = Cookie(...),
    offset: int = Query(0),
    userVideosService: UserVideosService = Depends(getUserVideosRepository)
):
    return userVideosService.getHistoryVideosByUserId("token", offset)

@routerUserVideos.post("/video/time") 
async def insert_time_watched(videoId = Form(...),timeWatched:int = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.addTimeWatched(tokenUser="token",videoId=videoId,timeAtVideo=timeWatched)

@routerUserVideos.post("/video/like")
async def insert_time_watched(videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.addLikeToVideo("token",videoId)

@routerUserVideos.post("/video/dislike")
async def insert_time_watched(videoId = Form(...),userVideosService: UserVideosService = Depends(getUserVideosRepository)):
    return userVideosService.addDislikeToVideo("token",videoId)