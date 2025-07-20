from pydantic import BaseModel
from datetime import datetime

class VideoResponse(BaseModel):
    videoDate: str
    userName: str
    videoTitle: str
    thumbnailUrl: str
    videoDuration: int
    videoId:str
    timeWatched:int