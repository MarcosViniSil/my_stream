from pydantic import BaseModel
from datetime import datetime

class VideoStreaming(BaseModel):
    videoDate: str
    userName: str
    videoTitle: str
    videoUrl: str
    videoId: str
    likes:int
    dislikes:int