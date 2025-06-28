from pydantic import BaseModel

class VideosHistory(BaseModel):
    videoId: str
    videoTitle: str
    thumnailUrl: str
    dateVideo: str
    lastTime: int