from pydantic import BaseModel

class VideosHistory(BaseModel):
    videoId: str
    videoTitle: str
    thumbnailUrl: str
    dateVideo: str
    lastTime: int
    videoDuration:int
    userName:str